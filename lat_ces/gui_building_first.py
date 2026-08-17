"""Compact Building-first LAT-CES desktop application."""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk

from lat_ces.building.floor_plan import FloorPlan, Point2D, Segment2D, Wall
from lat_ces.building.model import BuildingModel, Level
from lat_ces.building.project_spec import BuildingProjectSpec, LevelProjectSpec, RoomSpec, WallConstructionSpec
from lat_ces.building.workflow import BuildingWorkflow, make_blank_floor_plan

MODES = ("Projektovanje", "Geometrija", "Instalacije", "Konstrukcija", "Simulacija", "Provjera i izvještaj")


def blank_workflow() -> BuildingWorkflow:
    model = BuildingModel(name="Novi objekat")
    plan = make_blank_floor_plan("Prizemlje")
    level = model.add_level(Level(name="Prizemlje", elevation=0.0, height=2.80, floor_plan=plan))
    workflow = BuildingWorkflow(model=model, current_step=1, active_level_id=level.level_id)
    return workflow


def parse_positive(var: tk.StringVar, label: str) -> float:
    try:
        value = float(var.get().replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"{label}: unesite broj.") from exc
    if value <= 0:
        raise ValueError(f"{label}: vrijednost mora biti > 0.")
    return value


def make_preview_plan(spec: LevelProjectSpec) -> FloorPlan:
    """Build the first visible plan from the confirmed level specification."""
    from lat_ces.building.workflow import make_envelope_floor_plan, add_room_layout

    plan = make_envelope_floor_plan(
        spec.name,
        spec.length_m,
        spec.width_m,
        spec.construction.wall_thickness_m,
    )
    add_room_layout(plan, spec)
    return plan


class FirstStepDialog(tk.Toplevel):
    """Small mandatory first-step form. Confirmation creates the visible plan."""

    def __init__(self, app: "BuildingFirstApp") -> None:
        super().__init__(app)
        self.app = app
        self.title("LAT-CES — Prvi korak")
        self.geometry("600x560")
        self.minsize(560, 520)
        self.transient(app)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._blocked_close)

        self.length = tk.StringVar()
        self.width = tk.StringVar()
        self.height = tk.StringVar(value="2.80")
        self.block_brand = tk.StringVar()
        self.wall_thickness = tk.StringVar(value="0.25")
        self.insulation = tk.StringVar(value="EPS / stiropor")
        self.insulation_thickness = tk.StringVar(value="0.10")
        self.facade_brand = tk.StringVar()
        self.granulation = tk.StringVar()
        self.render_thickness = tk.StringVar(value="0.005")
        self._room_vars: list[tuple[tk.StringVar, tk.StringVar, tk.StringVar]] = []
        self._build()

    def _blocked_close(self) -> None:
        messagebox.showinfo("LAT-CES", "Prvi korak mora biti potvrđen prije rada na projektu.", parent=self)

    def _field(self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(parent, textvariable=var, width=24).grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=3)

    def _build(self) -> None:
        outer = ttk.Frame(self, padding=14)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="1. OSNOVNI PODACI OBJEKTA", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Unesi osnovni gabarit i nekoliko građevinskih podataka. Nakon potvrde LAT-CES odmah prikazuje tlocrt.", wraplength=550).pack(anchor="w", pady=(3, 10))

        top = ttk.LabelFrame(outer, text="Gabarit", padding=10)
        top.pack(fill="x", pady=(0, 8))
        top.columnconfigure(1, weight=1)
        self._field(top, 0, "Dužina objekta (m)", self.length)
        self._field(top, 1, "Širina objekta (m)", self.width)
        self._field(top, 2, "Visina etaže (m)", self.height)

        construction = ttk.LabelFrame(outer, text="Građevinski sastav", padding=10)
        construction.pack(fill="x", pady=(0, 8))
        construction.columnconfigure(1, weight=1)
        self._field(construction, 0, "Marka bloka", self.block_brand)
        self._field(construction, 1, "Debljina zida (m)", self.wall_thickness)
        self._field(construction, 2, "Izolacija", self.insulation)
        self._field(construction, 3, "Debljina izolacije (m)", self.insulation_thickness)
        self._field(construction, 4, "Marka fasade", self.facade_brand)
        self._field(construction, 5, "Granulacija fasade (mm)", self.granulation)
        self._field(construction, 6, "Završna žbuka (m)", self.render_thickness)

        rooms = ttk.LabelFrame(outer, text="Raspored prostorija", padding=10)
        rooms.pack(fill="both", expand=True)
        headers = ("Prostorija", "Dužina (m)", "Širina (m)")
        for col, text in enumerate(headers):
            ttk.Label(rooms, text=text).grid(row=0, column=col, sticky="w", padx=(0 if col == 0 else 8, 0))
        for row in range(1, 6):
            n, l, w = tk.StringVar(), tk.StringVar(), tk.StringVar()
            self._room_vars.append((n, l, w))
            ttk.Entry(rooms, textvariable=n, width=25).grid(row=row, column=0, sticky="ew", pady=2)
            ttk.Entry(rooms, textvariable=l, width=11).grid(row=row, column=1, padx=8, pady=2)
            ttk.Entry(rooms, textvariable=w, width=11).grid(row=row, column=2, pady=2)
        rooms.columnconfigure(0, weight=1)
        ttk.Label(rooms, text="Hodnik može biti dio osnovnog gabarita objekta.", foreground="#667085").grid(row=6, column=0, columnspan=3, sticky="w", pady=(5, 0))

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(buttons, text="Odustani", command=self.destroy).pack(side="left")
        ttk.Button(buttons, text="Potvrdi i prikaži tlocrt →", command=self.confirm).pack(side="right")

    def confirm(self) -> None:
        try:
            length = parse_positive(self.length, "Dužina objekta")
            width = parse_positive(self.width, "Širina objekta")
            height = parse_positive(self.height, "Visina etaže")
            wall_t = parse_positive(self.wall_thickness, "Debljina zida")
            insulation_t = parse_positive(self.insulation_thickness, "Debljina izolacije")
            render_t = parse_positive(self.render_thickness, "Završna žbuka")
            rooms: list[RoomSpec] = []
            for name_var, l_var, w_var in self._room_vars:
                name = name_var.get().strip()
                if not name:
                    continue
                rooms.append(RoomSpec(name=name, length_m=parse_positive(l_var, f"Dužina prostorije {name}"), width_m=parse_positive(w_var, f"Širina prostorije {name}")))

            construction = WallConstructionSpec(
                block_brand=self.block_brand.get().strip(),
                wall_thickness_m=wall_t,
                insulation_type=self.insulation.get().strip(),
                insulation_thickness_m=insulation_t,
                facade_brand=self.facade_brand.get().strip(),
                facade_granulation_mm=float(self.granulation.get().replace(",", ".")) if self.granulation.get().strip() else 0.0,
                render_thickness_m=render_t,
            )
            spec = LevelProjectSpec(
                name="Prizemlje",
                height_m=height,
                length_m=length,
                width_m=width,
                construction=construction,
                rooms=rooms,
                finalized=True,
            )
            project = BuildingProjectSpec(name="Novi objekat", floor_count=1, levels=[spec], floor_count_finalized=False)
            workflow = blank_workflow()
            workflow.project_spec = project
            workflow.set_level_spec(0, spec)
            workflow.current_step = 1
            self.app.workflow = workflow
            self.app.refresh_after_first_step()
            self.grab_release()
            self.destroy()
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)


class BuildingFirstApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1240x780")
        self.minsize(1050, 680)
        self.workflow = blank_workflow()
        self.canvas = tk.Canvas(self, background="white", highlightthickness=1)
        self.status_var = tk.StringVar(value="Korak 1 — početni projekat nije potvrđen")
        self.level_var = tk.StringVar(value="Prizemlje")
        self._build()
        self.after_idle(self.open_first_step)

    def _build(self) -> None:
        header = ttk.Frame(self, padding=(16, 10))
        header.pack(fill="x")
        ttk.Label(header, text="LAT-CES", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(header, text="Building Model", font=("Segoe UI", 10)).pack(side="left", padx=10)
        self.plan_info = ttk.Label(header, text="Prazan tlocrt — čeka potvrdu prvog koraka")
        self.plan_info.pack(side="left", padx=25)

        body = ttk.Frame(self, padding=(16, 0, 16, 10))
        body.pack(fill="both", expand=True)
        self.canvas.pack(in_=body, side="left", fill="both", expand=True)
        side = ttk.Frame(body, width=290)
        side.pack(side="left", fill="y", padx=(12, 0))
        side.pack_propagate(False)

        modes = ttk.LabelFrame(side, text="Režim rada", padding=8)
        modes.pack(fill="x")
        for mode in MODES:
            ttk.Button(modes, text=mode, command=lambda m=mode: self.status_var.set(f"Režim: {m}")).pack(fill="x", pady=2)

        step = ttk.LabelFrame(side, text="Projekt", padding=8)
        step.pack(fill="x", pady=(10, 0))
        self.step_label = ttk.Label(step, text="1. Tlocrt", font=("Segoe UI", 13, "bold"))
        self.step_label.pack(anchor="w")
        self.next_button = ttk.Button(step, text="Nastavi na spratnost →", command=self.next_to_levels)
        self.next_button.pack(fill="x", pady=(8, 3))
        self.next_button.configure(state="disabled")
        ttk.Button(step, text="Ponovi prvi korak", command=self.open_first_step).pack(fill="x", pady=2)
        ttk.Button(step, text="Sačuvaj konfiguraciju", command=self.save_stub).pack(fill="x", pady=2)

        self.summary = tk.Text(side, height=12, width=34, state="disabled", wrap="word")
        self.summary.pack(fill="x", pady=(10, 0))
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x")

    def open_first_step(self) -> None:
        FirstStepDialog(self)

    def refresh_after_first_step(self) -> None:
        self.next_button.configure(state="normal")
        self.plan_info.configure(text=f"Tlocrt — {self.workflow.floor_plan.name}  ({self.workflow.project_spec.levels[0].length_m:.2f} × {self.workflow.project_spec.levels[0].width_m:.2f} m)")
        self.status_var.set("Prvi korak potvrđen — tlocrt je generisan")
        self.draw_plan()
        self.update_summary()

    def next_to_levels(self) -> None:
        self.status_var.set("Sljedeći korak: spratnost — postojeći tlocrt ostaje osnova.")

    def save_stub(self) -> None:
        messagebox.showinfo("LAT-CES", "Spremanje konfiguracije ostaje dostupno; sada je fokus na provjeri prvog koraka.", parent=self)

    def plan_bounds(self) -> tuple[float, float, float, float]:
        points: list[Point2D] = []
        for wall in self.workflow.floor_plan.walls.values():
            points.extend((wall.segment.start, wall.segment.end))
        if not points:
            return 0.0, 10.0, 0.0, 10.0
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        return min(xs) - 1.0, max(xs) + 1.0, min(ys) - 1.0, max(ys) + 1.0

    def model_to_canvas(self, p: Point2D) -> tuple[float, float]:
        w = max(self.canvas.winfo_width(), 400)
        h = max(self.canvas.winfo_height(), 300)
        xmin, xmax, ymin, ymax = self.plan_bounds()
        scale = min((w - 80) / max(xmax - xmin, 1.0), (h - 80) / max(ymax - ymin, 1.0))
        ox = (w - (xmax - xmin) * scale) / 2 - xmin * scale
        oy = (h + (ymax - ymin) * scale) / 2 + ymin * scale
        return ox + p.x * scale, oy - p.y * scale

    def draw_plan(self) -> None:
        self.canvas.delete("all")
        w = max(self.canvas.winfo_width(), 400)
        h = max(self.canvas.winfo_height(), 300)
        for wall in self.workflow.floor_plan.walls.values():
            a = self.model_to_canvas(wall.segment.start)
            b = self.model_to_canvas(wall.segment.end)
            self.canvas.create_line(*a, *b, width=8, fill="#1f2937")
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            self.canvas.create_text(mx, my - 10, text=f"{wall.segment.length:.2f} m", fill="#374151", font=("Segoe UI", 9, "bold"))
        self.canvas.create_text(20, 20, text="TLOCRT — prvi potvrđeni prikaz", anchor="nw", font=("Segoe UI", 13, "bold"), fill="#374151")
        self.canvas.create_text(w - 20, 20, text="Sjever ↑", anchor="ne", fill="#667085")

    def update_summary(self) -> None:
        self.summary.configure(state="normal")
        self.summary.delete("1.0", "end")
        for level in self.workflow.model.levels.values():
            self.summary.insert("end", f"{level.name}\n")
            self.summary.insert("end", f"Visina: {level.height:.2f} m\n")
            self.summary.insert("end", f"Zidovi: {level.floor_plan.wall_count if level.floor_plan else 0}\n")
        self.summary.configure(state="disabled")


if __name__ == "__main__":
    BuildingFirstApp().mainloop()
