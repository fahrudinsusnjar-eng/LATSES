"""LAT-CES Windows desktop application.

Building-first GUI adapter. The floor plan is the primary workspace and can
be edited directly; scientific domains operate on the same BuildingModel.
"""
from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from lat_ces.application.service import analyze_config, export_report, load_config
from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall


MODE_DESCRIPTIONS = {
    "Projektovanje": "Tlocrt, prostorije, zidovi i otvori",
    "Geometrija": "Visine, spratovi i 3D geometrija",
    "Instalacije": "HVAC, FluidNetwork, voda i električne instalacije",
    "Konstrukcija": "Opterećenja, statika i mehanika konstrukcija",
    "Simulacija": "Fluidika, termika, akustika i energija",
    "Provjera i izvještaj": "Verifikacija, sigurnost i izvještaji",
}

EDITOR_TOOLS = (
    ("select", "Izaberi"),
    ("draw", "Nacrtaj zid"),
    ("move", "Pomjeri"),
    ("delete", "Obriši"),
    ("door", "Vrata"),
    ("window", "Prozor"),
)


class FloorPlanEditor:
    """Interaction/controller layer for a canonical :class:`FloorPlan`."""

    def __init__(self, app: "LATCESApp") -> None:
        self.app = app
        self.tool = "select"
        self.start_point: Point2D | None = None
        self.selected_wall_id: str | None = None
        self.drag_last: Point2D | None = None

    @property
    def canvas(self) -> tk.Canvas:
        return self.app.canvas

    def set_tool(self, tool: str) -> None:
        self.tool = tool
        self.start_point = None
        self.drag_last = None
        self.app.tool_var.set(tool)
        label = dict(EDITOR_TOOLS).get(tool, tool)
        self.app.status_var.set(f"Alat: {label}")
        self.app._draw_floor_plan()

    def snap(self, point: Point2D) -> Point2D:
        return Point2D(round(point.x * 10) / 10.0, round(point.y * 10) / 10.0)

    def canvas_to_model(self, x: float, y: float) -> Point2D:
        return self.app.canvas_to_model(x, y)

    def nearest_wall(self, point: Point2D, tolerance_m: float = 0.30) -> Wall | None:
        best: tuple[float, Wall] | None = None
        for wall in self.app.floor_plan.walls.values():
            distance = self.point_segment_distance(point, wall.segment.start, wall.segment.end)
            if distance <= tolerance_m and (best is None or distance < best[0]):
                best = (distance, wall)
        return best[1] if best else None

    @staticmethod
    def point_segment_distance(point: Point2D, start: Point2D, end: Point2D) -> float:
        dx = end.x - start.x
        dy = end.y - start.y
        length_sq = dx * dx + dy * dy
        if length_sq == 0:
            return math.hypot(point.x - start.x, point.y - start.y)
        t = ((point.x - start.x) * dx + (point.y - start.y) * dy) / length_sq
        t = max(0.0, min(1.0, t))
        px = start.x + t * dx
        py = start.y + t * dy
        return math.hypot(point.x - px, point.y - py)

    def click(self, event: tk.Event) -> None:
        point = self.snap(self.canvas_to_model(event.x, event.y))
        tool = self.tool

        if tool == "draw":
            if self.start_point is None:
                self.start_point = point
                self.app.status_var.set("Početak zida postavljen — klikni završnu tačku")
                self.app._draw_floor_plan()
                return
            if math.hypot(point.x - self.start_point.x, point.y - self.start_point.y) < 0.05:
                return
            wall = Wall(
                name=f"Zid {self.app.floor_plan.wall_count + 1}",
                segment=Segment2D(self.start_point, point),
                thickness=0.20,
            )
            self.app.floor_plan.add_wall(wall)
            self.start_point = None
            self.app.refresh_plan()
            self.app.status_var.set(f"Dodan zid: {wall.name}")
            return

        wall = self.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = None
            self.app.refresh_plan()
            return

        self.selected_wall_id = wall.wall_id
        if tool == "delete":
            del self.app.floor_plan.walls[wall.wall_id]
            self.selected_wall_id = None
            self.app.refresh_plan()
            self.app.status_var.set(f"Obrisan zid: {wall.name}")
        elif tool in {"door", "window"}:
            self.add_opening(wall, point, "door" if tool == "door" else "window")
        else:
            self.app.refresh_plan()
            self.app.status_var.set(f"Izabran: {wall.name}")

    def begin_drag(self, event: tk.Event) -> None:
        if self.tool != "move":
            return
        point = self.snap(self.canvas_to_model(event.x, event.y))
        wall = self.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = None
            self.drag_last = None
            self.app.refresh_plan()
            return
        self.selected_wall_id = wall.wall_id
        self.drag_last = point
        self.app.status_var.set(f"Pomjeranje: {wall.name}")

    def drag(self, event: tk.Event) -> None:
        if self.tool != "move" or self.selected_wall_id is None or self.drag_last is None:
            return
        wall = self.app.floor_plan.walls.get(self.selected_wall_id)
        if wall is None:
            return
        point = self.snap(self.canvas_to_model(event.x, event.y))
        dx = point.x - self.drag_last.x
        dy = point.y - self.drag_last.y
        wall.segment = Segment2D(
            Point2D(wall.segment.start.x + dx, wall.segment.start.y + dy),
            Point2D(wall.segment.end.x + dx, wall.segment.end.y + dy),
        )
        for opening in wall.openings:
            _ = opening
        self.drag_last = point
        self.app.refresh_plan()

    def end_drag(self, _event: tk.Event) -> None:
        if self.tool == "move" and self.selected_wall_id:
            wall = self.app.floor_plan.walls.get(self.selected_wall_id)
            self.app.status_var.set(f"Pomjeren: {wall.name}" if wall else "Spremno")
        self.drag_last = None

    def add_opening(self, wall: Wall, point: Point2D, kind: str) -> None:
        length = wall.segment.length
        dx = wall.segment.end.x - wall.segment.start.x
        dy = wall.segment.end.y - wall.segment.start.y
        projection = ((point.x - wall.segment.start.x) * dx + (point.y - wall.segment.start.y) * dy) / (length * length)
        offset = max(0.0, min(length, projection * length))
        default_width = 0.90 if kind == "door" else 1.20
        width = simpledialog.askfloat(
            "Otvor",
            f"Širina {kind} (m):",
            initialvalue=default_width,
            minvalue=0.10,
            parent=self.app,
        )
        if width is None:
            return
        offset = min(max(0.0, offset - width / 2.0), max(0.0, length - width))
        try:
            wall.add_opening(Opening(kind=kind, offset=offset, width=width))
        except ValueError as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self.app)
            return
        self.app.refresh_plan()
        self.app.status_var.set(f"Dodan otvor: {kind} u {wall.name}")



def build_default_floor_plan() -> FloorPlan:
    """Create a neutral starter plan; real projects will load their own model."""
    plan = FloorPlan(name="Novi objekat")
    width, depth = 12.0, 8.0
    walls = [
        ("Sjever", (0, 0, width, 0)),
        ("Jug", (0, depth, width, depth)),
        ("Zapad", (0, 0, 0, depth)),
        ("Istok", (width, 0, width, depth)),
        ("Pregrada 1", (7.0, 0, 7.0, 4.8)),
        ("Pregrada 2", (0.0, 4.8, 7.0, 4.8)),
    ]
    for name, (x1, y1, x2, y2) in walls:
        plan.add_wall(Wall(name=name, segment=Segment2D(Point2D(x1, y1), Point2D(x2, y2)), thickness=0.20))
    return plan


class LATCESApp(tk.Tk):
    """Building-first desktop shell around the canonical LAT-CES model."""

    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1280x780")
        self.minsize(1050, 680)
        self.floor_plan = build_default_floor_plan()
        self.active_mode = tk.StringVar(value="Projektovanje")
        self.tool_var = tk.StringVar(value="select")
        self.status_var = tk.StringVar(value="Spreman — tlocrt je početna radna površina")
        self.config_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.format_var = tk.StringVar(value="json")
        self.editor = FloorPlanEditor(self)
        self._build_ui()
        self._draw_floor_plan()

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="LAT-CES", font=("Segoe UI", 21, "bold")).pack(side="left")
        ttk.Label(header, text="Building Model  /  Tlocrt", font=("Segoe UI", 11)).pack(side="left", padx=(14, 0), pady=(5, 0))
        ttk.Button(header, text="Novi projekat", command=self.new_project).pack(side="right")
        ttk.Button(header, text="Otvori analizu…", command=self.browse_config).pack(side="right", padx=8)

        body = ttk.Frame(self, padding=(18, 0, 18, 12))
        body.pack(fill="both", expand=True)

        workspace = ttk.LabelFrame(body, text="Tlocrt", padding=8)
        workspace.pack(side="left", fill="both", expand=True)

        toolbar = ttk.Frame(workspace)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(toolbar, text="Uređivanje:").pack(side="left")
        for tool, label in EDITOR_TOOLS:
            ttk.Radiobutton(toolbar, text=label, value=tool, variable=self.tool_var, command=lambda value=tool: self.editor.set_tool(value)).pack(side="left", padx=(6, 0))
        ttk.Label(toolbar, text="Snap 0.10 m", foreground="#5f6368").pack(side="right")

        self.canvas = tk.Canvas(workspace, background="white", highlightthickness=1, highlightbackground="#cfd4da")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._draw_floor_plan())
        self.canvas.bind("<Button-1>", self.editor.click)
        self.canvas.bind("<ButtonPress-1>", self.editor.begin_drag)
        self.canvas.bind("<B1-Motion>", self.editor.drag)
        self.canvas.bind("<ButtonRelease-1>", self.editor.end_drag)

        side = ttk.Frame(body, width=320)
        side.pack(side="left", fill="y", padx=(14, 0))
        side.pack_propagate(False)

        mode_box = ttk.LabelFrame(side, text="Režim rada", padding=10)
        mode_box.pack(fill="x")
        for mode in MODE_DESCRIPTIONS:
            ttk.Button(mode_box, text=mode, command=lambda value=mode: self.select_mode(value)).pack(fill="x", pady=3)

        self.mode_title = ttk.Label(side, text="Projektovanje", font=("Segoe UI", 14, "bold"))
        self.mode_title.pack(anchor="w", pady=(18, 3))
        self.mode_desc = ttk.Label(side, text=MODE_DESCRIPTIONS["Projektovanje"], wraplength=280)
        self.mode_desc.pack(anchor="w")

        tools = ttk.LabelFrame(side, text="Radna svojstva", padding=10)
        tools.pack(fill="x", pady=(14, 0))
        ttk.Label(tools, text="Objekat").grid(row=0, column=0, sticky="w")
        ttk.Label(tools, text=self.floor_plan.name, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="e")
        ttk.Label(tools, text="Zidovi").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.wall_count_label = ttk.Label(tools, text=str(self.floor_plan.wall_count))
        self.wall_count_label.grid(row=1, column=1, sticky="e", pady=(6, 0))
        ttk.Label(tools, text="Otvoreni zidovi").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.opening_count_label = ttk.Label(tools, text="0")
        self.opening_count_label.grid(row=2, column=1, sticky="e", pady=(6, 0))
        ttk.Label(tools, text="Nivo").grid(row=3, column=0, sticky="w", pady=(6, 0))
        ttk.Label(tools, text="Prizemlje").grid(row=3, column=1, sticky="e", pady=(6, 0))
        tools.columnconfigure(1, weight=1)

        action_box = ttk.LabelFrame(side, text="LAT-CES alati", padding=10)
        action_box.pack(fill="x", pady=(14, 0))
        ttk.Button(action_box, text="Scientific Analysis", command=self.open_analysis).pack(fill="x")
        ttk.Button(action_box, text="Provjeri tlocrt", command=self.validate_plan).pack(fill="x", pady=6)
        ttk.Button(action_box, text="Izvoz projekta", command=self.export_project).pack(fill="x")

        ttk.Label(side, text="Princip: jedan Building Model, više naučnih režima rada.", wraplength=280, foreground="#5f6368").pack(anchor="w", pady=(16, 0))
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x")

    def model_to_canvas(self, point: Point2D) -> tuple[float, float]:
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        margin = 70
        scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0)
        origin_x = (width - 12.0 * scale) / 2
        origin_y = (height - 8.0 * scale) / 2
        return origin_x + point.x * scale, origin_y + point.y * scale

    def canvas_to_model(self, x: float, y: float) -> Point2D:
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        margin = 70
        scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0)
        origin_x = (width - 12.0 * scale) / 2
        origin_y = (height - 8.0 * scale) / 2
        return Point2D((x - origin_x) / scale, (y - origin_y) / scale)

    def _draw_floor_plan(self) -> None:
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        margin = 70
        scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0)
        origin_x = (width - 12.0 * scale) / 2
        origin_y = (height - 8.0 * scale) / 2

        for x in range(13):
            px = origin_x + x * scale
            self.canvas.create_line(px, origin_y, px, origin_y + 8 * scale, fill="#edf0f2")
        for y in range(9):
            py = origin_y + y * scale
            self.canvas.create_line(origin_x, py, origin_x + 12 * scale, py, fill="#edf0f2")

        for wall in self.floor_plan.walls.values():
            x1, y1 = self.model_to_canvas(wall.segment.start)
            x2, y2 = self.model_to_canvas(wall.segment.end)
            selected = wall.wall_id == self.editor.selected_wall_id
            self.canvas.create_line(x1, y1, x2, y2, width=10 if selected else 8, fill="#2563eb" if selected else "#374151", capstyle=tk.BUTT)

            length = wall.segment.length
            for opening in wall.openings:
                t1 = opening.offset / length
                t2 = (opening.offset + opening.width) / length
                ox1 = wall.segment.start.x + (wall.segment.end.x - wall.segment.start.x) * t1
                oy1 = wall.segment.start.y + (wall.segment.end.y - wall.segment.start.y) * t1
                ox2 = wall.segment.start.x + (wall.segment.end.x - wall.segment.start.x) * t2
                oy2 = wall.segment.start.y + (wall.segment.end.y - wall.segment.start.y) * t2
                cx1, cy1 = self.model_to_canvas(Point2D(ox1, oy1))
                cx2, cy2 = self.model_to_canvas(Point2D(ox2, oy2))
                self.canvas.create_line(cx1, cy1, cx2, cy2, width=7, fill="#ffffff")
                self.canvas.create_text((cx1 + cx2) / 2, (cy1 + cy2) / 2 - 10, text=opening.kind, fill="#1f2937", font=("Segoe UI", 8))

        labels = ((3.5, 2.3, "Dnevni boravak / kuhinja"), (9.2, 2.3, "Soba"), (3.5, 6.2, "Ulaz / hodnik"))
        for x, y, label in labels:
            self.canvas.create_text(origin_x + x * scale, origin_y + y * scale, text=label, fill="#4b5563", font=("Segoe UI", 11 if "Dnevni" in label else 10))
        self.canvas.create_text(width - 20, 20, text="Sjever ↑", anchor="ne", fill="#5f6368")
        if self.editor.start_point is not None:
            sx, sy = self.model_to_canvas(self.editor.start_point)
            self.canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, fill="#dc2626", outline="")

    def refresh_plan(self) -> None:
        self.wall_count_label.configure(text=str(self.floor_plan.wall_count))
        opening_count = sum(len(w.openings) for w in self.floor_plan.walls.values())
        self.opening_count_label.configure(text=str(opening_count))
        self._draw_floor_plan()

    def select_mode(self, mode: str) -> None:
        self.active_mode.set(mode)
        self.mode_title.configure(text=mode)
        self.mode_desc.configure(text=MODE_DESCRIPTIONS[mode])
        self.status_var.set(f"Režim: {mode} — tlocrt ostaje centralni model")

    def new_project(self) -> None:
        self.floor_plan = build_default_floor_plan()
        self.editor.selected_wall_id = None
        self.editor.start_point = None
        self.refresh_plan()
        self.select_mode("Projektovanje")

    def validate_plan(self) -> None:
        findings = self.floor_plan.validate()
        if findings:
            self.status_var.set(f"Tlocrt: {len(findings)} nalaza")
            messagebox.showwarning("Provjera tlocrta", "\n".join(findings))
            return
        self.status_var.set("Tlocrt je geometrijski validan")
        messagebox.showinfo("Provjera tlocrta", "Tlocrt je geometrijski validan.")

    def export_project(self) -> None:
        target = filedialog.asksaveasfilename(title="Sačuvaj Building Model", defaultextension=".json", filetypes=(("JSON files", "*.json"),), initialfile="building_model.json")
        if not target:
            return
        payload = {
            "name": self.floor_plan.name,
            "plan_id": self.floor_plan.plan_id,
            "walls": [
                {
                    "id": wall.wall_id,
                    "name": wall.name,
                    "start": {"x": wall.segment.start.x, "y": wall.segment.start.y},
                    "end": {"x": wall.segment.end.x, "y": wall.segment.end.y},
                    "thickness_m": wall.thickness,
                    "openings": [
                        {"id": o.opening_id, "kind": o.kind, "offset_m": o.offset, "width_m": o.width}
                        for o in wall.openings
                    ],
                }
                for wall in self.floor_plan.walls.values()
            ],
        }
        Path(target).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status_var.set(f"Building Model izvezen: {target}")

    def browse_config(self) -> None:
        path = filedialog.askopenfilename(title="Select LAT-CES JSON configuration", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if path:
            self.config_path.set(path)
            self.open_analysis()

    def open_analysis(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("LAT-CES — Scientific Analysis")
        dialog.geometry("860x620")
        dialog.transient(self)
        cfg = ttk.Frame(dialog, padding=14)
        cfg.pack(fill="x")
        path_var = tk.StringVar(value=self.config_path.get())
        output_var = tk.StringVar(value=self.output_path.get())
        ttk.Label(cfg, text="JSON konfiguracija:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cfg, textvariable=path_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(cfg, text="Browse…", command=lambda: path_var.set(filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*"))))).grid(row=0, column=2)
        ttk.Label(cfg, text="Format:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Combobox(cfg, textvariable=self.format_var, values=("json", "md"), state="readonly", width=10).grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))
        ttk.Label(cfg, text="Output:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(cfg, textvariable=output_var).grid(row=2, column=1, columnspan=2, sticky="ew", padx=8, pady=(8, 0))
        cfg.columnconfigure(1, weight=1)

        result = tk.Text(dialog, wrap="word", font=("Consolas", 10))
        result.pack(fill="both", expand=True, padx=14, pady=8)

        def run() -> None:
            config_file = Path(path_var.get().strip())
            if not config_file.exists():
                messagebox.showwarning("LAT-CES", "Odaberi validnu JSON konfiguraciju.", parent=dialog)
                return
            try:
                config = load_config(config_file)
                report, exporter = analyze_config(config, project_default="LAT-CES Desktop Analysis", plenum_default="PLENUM-GUI-01", equation_default="Custom equation")
                fmt = self.format_var.get()
                output = Path(output_var.get().strip() or config_file.with_name(f"latces_report.{fmt}"))
                export_report(exporter, output, fmt)
                content = json.loads(exporter.to_json()) if fmt == "json" else exporter.to_markdown()
                display = json.dumps(content, indent=2, ensure_ascii=False) if isinstance(content, dict) else content
                result.delete("1.0", "end")
                result.insert("1.0", f"Status: [{report.status.value}]\nReport: {output}\n\n{display}")
                self.status_var.set(f"Scientific Analysis: {report.status.value}")
            except Exception as exc:
                result.delete("1.0", "end")
                result.insert("1.0", f"Analysis failed:\n\n{exc}")
                messagebox.showerror("LAT-CES analysis error", str(exc), parent=dialog)

        ttk.Button(dialog, text="Run Analysis", command=run).pack(pady=(0, 14))


def main() -> None:
    LATCESApp().mainloop()


if __name__ == "__main__":
    main()
