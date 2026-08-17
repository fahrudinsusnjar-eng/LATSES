"""Live dimensioned drafting layer for the LAT-CES Building Model editor."""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk

from lat_ces.building.floor_plan import Opening, Point2D, Segment2D, Wall
from lat_ces.gui_enhanced import EnhancedLATCESApp


class DraftingLATCESApp(EnhancedLATCESApp):
    """Dimension-first drafting: create, preview, place and measure elements."""

    def __init__(self) -> None:
        self.wall_length_var = tk.StringVar(value="3.00")
        self.wall_thickness_var = tk.StringVar(value="0.20")
        self.wall_drafting = False
        self.wall_preview_id: int | None = None
        self.wall_draft_length = 3.0
        self.wall_draft_thickness = 0.20
        self.wall_draft_start: Point2D | None = None
        super().__init__()
        # Replace only the click handler; move/drag/release handlers from the base GUI remain active.
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self._draft_click)
        self.canvas.bind("<Motion>", self._draft_motion, add="+")

    def _build_side_panel(self, side: ttk.Frame) -> None:
        super()._build_side_panel(side)
        box = ttk.LabelFrame(side, text="Dodaj novi zid", padding=8)
        box.pack(fill="x", pady=(10, 0))
        self.wall_editor = ttk.Frame(box)
        self.wall_editor.pack(fill="x")
        ttk.Button(box, text="＋ Dodaj novi zid", command=self._open_wall_editor).pack(fill="x")
        self.wall_fields = ttk.Frame(box)
        self.wall_fields.pack(fill="x", pady=(6, 0))
        self._field(self.wall_fields, "Dužina (m)", self.wall_length_var, 0)
        self._field(self.wall_fields, "Debljina (m)", self.wall_thickness_var, 1)
        ttk.Button(self.wall_fields, text="Kreiraj zid", command=self._create_wall_preview).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        ttk.Label(box, text="Nakon 'Kreiraj zid' linija prati miš. Klikom je postavljaš na željeno mjesto.", wraplength=315).pack(anchor="w", pady=(6, 0))
        self.wall_fields.pack_forget()

    def _open_wall_editor(self) -> None:
        self.wall_fields.pack(fill="x", pady=(6, 0))
        self.status_var.set("Unesi dužinu i debljinu, zatim klikni 'Kreiraj zid'.")
        self.view_step.set(3)
        self.goto_step()

    def _create_wall_preview(self) -> None:
        try:
            length = float(self.wall_length_var.get())
            thickness = float(self.wall_thickness_var.get())
            if length <= 0 or thickness <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("LAT-CES — Zid", "Dužina i debljina zida moraju biti pozitivne.", parent=self)
            return
        self.wall_draft_length = length
        self.wall_draft_thickness = thickness
        self.wall_drafting = True
        self.wall_draft_start = None
        self.editor.set_tool("select")
        self.status_var.set(f"Zid {length:.2f} × {thickness:.2f} m — pomjeraj miš; klik postavlja zid.")
        self.redraw_active_view()

    def _draft_motion(self, event: tk.Event) -> None:
        if not self.wall_drafting or self.view_step.get() != 3:
            return
        point = self.snap_point(self.canvas_to_model(event.x, event.y))
        half = self.wall_draft_length / 2.0
        start = Point2D(point.x - half, point.y)
        end = Point2D(point.x + half, point.y)
        if self.wall_preview_id is not None:
            self.canvas.delete(self.wall_preview_id)
        x1, y1 = self.model_to_canvas(start)
        x2, y2 = self.model_to_canvas(end)
        self.wall_preview_id = self.canvas.create_line(x1, y1, x2, y2, fill="#2563eb", width=4, dash=(8, 4))
        self._draw_live_distances(point, start, end)

    def _draft_click(self, event: tk.Event) -> None:
        if self.wall_drafting and self.view_step.get() == 3:
            point = self.snap_point(self.canvas_to_model(event.x, event.y))
            half = self.wall_draft_length / 2.0
            start = Point2D(point.x - half, point.y)
            end = Point2D(point.x + half, point.y)
            wall = Wall(
                name=f"Zid {self.floor_plan.wall_count + 1}",
                segment=Segment2D(start, end),
                thickness=self.wall_draft_thickness,
            )
            self.floor_plan.add_wall(wall)
            self.editor.selected_wall_id = wall.wall_id
            self.wall_drafting = False
            self.wall_draft_start = point
            self.status_var.set(f"Postavljen zid: {self.wall_draft_length:.2f} × {self.wall_draft_thickness:.2f} m")
            self.refresh_view()
            return
        self.editor.click(event)

    def _external_bounds(self) -> tuple[float, float, float, float]:
        level = self.active_level
        return 0.0, max(level.length_m, 0.0), 0.0, max(level.width_m, 0.0)

    def _draw_live_distances(self, point: Point2D, start: Point2D, end: Point2D) -> None:
        # Remove only temporary dimension tags from the previous mouse position.
        self.canvas.delete("live-dimension")
        xmin, xmax, ymin, ymax = self._external_bounds()
        if xmax <= xmin or ymax <= ymin:
            return
        # For a horizontal wall, show distance from each end to the nearest vertical exterior wall
        # and from the wall centre to the nearest horizontal exterior wall.
        left = max(0.0, start.x - xmin)
        right = max(0.0, xmax - end.x)
        bottom = max(0.0, point.y - ymin)
        top = max(0.0, ymax - point.y)
        x1, y1 = self.model_to_canvas(start)
        x2, y2 = self.model_to_canvas(end)
        cx, cy = self.model_to_canvas(point)
        self.canvas.create_text(x1, y1 - 18, text=f"← {left:.2f} m", fill="#b45309", tags="live-dimension", anchor="e")
        self.canvas.create_text(x2, y2 - 18, text=f"{right:.2f} m →", fill="#b45309", tags="live-dimension", anchor="w")
        self.canvas.create_text(cx + 12, cy, text=f"↓ {bottom:.2f} m   ↑ {top:.2f} m", fill="#b45309", tags="live-dimension", anchor="w")
        self.canvas.create_text(cx, cy + 22, text=f"Zid {self.wall_draft_length:.2f} × {self.wall_draft_thickness:.2f} m", fill="#1d4ed8", tags="live-dimension")

    def draw_floor_plan(self) -> None:
        super().draw_floor_plan()
        if self.wall_drafting:
            # The motion event redraws the live preview; keep the instruction visible after redraws.
            self.canvas.create_text(20, 20, text="PREVIEW ZIDA — pomjeraj miš i klikni za postavljanje", anchor="nw", fill="#1d4ed8", font=("Segoe UI", 10, "bold"), tags="live-dimension")

    def _drop_opening(self, point: Point2D, kind: str) -> None:
        # Existing enhanced opening placement remains dimensioned and wall-snapped.
        super()._drop_opening(point, kind)


# Entry point used by the Windows installer for the new drafting workflow.
def main() -> None:
    DraftingLATCESApp().mainloop()


if __name__ == "__main__":
    main()
