"""LAT-CES Building-first desktop application.

The user works from one BuildingModel. Each level has its own independent
floor plan. The editor is dimensional, persistent and ready for downstream
scientific systems.
"""
from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from lat_ces.application.service import analyze_config, export_report, load_config
from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall
from lat_ces.building.geometry3d import build_geometry
from lat_ces.building.model import BuildingModel
from lat_ces.building.project_io import load_workflow, save_workflow
from lat_ces.building.workflow import BuildingWorkflow, make_square_floor_plan

MODE_DESCRIPTIONS = {
    "Projektovanje": "Tlocrt, dimenzije, zidovi, pregrade i prostorije",
    "Geometrija": "Visine, etaže i 3D geometrija",
    "Instalacije": "HVAC, FluidNetwork, voda i električne instalacije",
    "Konstrukcija": "Opterećenja, statika i mehanika konstrukcija",
    "Simulacija": "Fluidika, termika, akustika i energija",
    "Provjera i izvještaj": "Verifikacija, sigurnost i izvještaji",
}
EDITOR_TOOLS = (
    ("select", "Izaberi"),
    ("draw", "Nova linija / zid"),
    ("move", "Pomjeri"),
    ("delete", "Obriši"),
    ("door", "Vrata"),
    ("window", "Prozor"),
)
STEPS = ((1, "Tlocrt"), (2, "Visina / spratnost"), (3, "Otvori"), (4, "3D model"))


def new_workflow() -> BuildingWorkflow:
    model = BuildingModel(name="Novi objekat")
    workflow = BuildingWorkflow(model=model)
    workflow.set_floor_plan(make_square_floor_plan("Prizemlje", 10.0))
    return workflow


class FloorPlanEditor:
    def __init__(self, app: "LATCESApp") -> None:
        self.app = app
        self.tool = "select"
        self.start_point: Point2D | None = None
        self.selected_wall_id: str | None = None
        self.drag_last: Point2D | None = None

    @property
    def floor_plan(self) -> FloorPlan:
        return self.app.workflow.floor_plan

    def set_tool(self, tool: str) -> None:
        self.tool = tool
        self.start_point = None
        self.drag_last = None
        self.app.tool_var.set(tool)
        self.app.status_var.set(f"Alat: {dict(EDITOR_TOOLS)[tool]}")
        self.app.redraw_active_view()

    @staticmethod
    def snap(point: Point2D) -> Point2D:
        return Point2D(round(point.x * 10) / 10.0, round(point.y * 10) / 10.0)

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

    def nearest_wall(self, point: Point2D, tolerance_m: float = 0.30) -> Wall | None:
        best: tuple[float, Wall] | None = None
        for wall in self.floor_plan.walls.values():
            distance = self.point_segment_distance(point, wall.segment.start, wall.segment.end)
            if distance <= tolerance_m and (best is None or distance < best[0]):
                best = (distance, wall)
        return best[1] if best else None

    def click(self, event: tk.Event) -> None:
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        if self.tool == "draw":
            if self.start_point is None:
                self.start_point = point
                self.app.status_var.set(f"Početak zida: ({point.x:.1f}, {point.y:.1f}) m — klikni kraj")
                self.app.redraw_active_view()
                return
            if math.hypot(point.x - self.start_point.x, point.y - self.start_point.y) < 0.1:
                return
            wall = Wall(
                name=f"Zid {self.floor_plan.wall_count + 1}",
                segment=Segment2D(self.start_point, point),
                thickness=0.20,
            )
            self.floor_plan.add_wall(wall)
            self.start_point = None
            self.selected_wall_id = wall.wall_id
            self.app.refresh_plan()
            self.app.status_var.set(f"Dodan zid {wall.name}: {wall.segment.length:.2f} m")
            return

        wall = self.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = None
            self.app.update_selected_wall()
            self.app.redraw_active_view()
            return
        self.selected_wall_id = wall.wall_id
        if self.tool == "delete":
            del self.floor_plan.walls[wall.wall_id]
            self.selected_wall_id = None
            self.app.refresh_plan()
            self.app.status_var.set(f"Obrisan: {wall.name}")
        elif self.tool in {"door", "window"}:
            self.add_opening(wall, point, self.tool)
        else:
            self.app.update_selected_wall()
            self.app.redraw_active_view()
            self.app.status_var.set(f"Izabran: {wall.name} — {wall.segment.length:.2f} m")

    def begin_drag(self, event: tk.Event) -> None:
        if self.tool != "move":
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        wall = self.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = None
            self.drag_last = None
            return
        self.selected_wall_id = wall.wall_id
        self.drag_last = point
        self.app.update_selected_wall()

    def drag(self, event: tk.Event) -> None:
        if self.tool != "move" or self.selected_wall_id is None or self.drag_last is None:
            return
        wall = self.floor_plan.walls.get(self.selected_wall_id)
        if wall is None:
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        dx, dy = point.x - self.drag_last.x, point.y - self.drag_last.y
        wall.segment = Segment2D(
            Point2D(wall.segment.start.x + dx, wall.segment.start.y + dy),
            Point2D(wall.segment.end.x + dx, wall.segment.end.y + dy),
        )
        self.drag_last = point
        self.app.refresh_plan()

    def end_drag(self, _event: tk.Event) -> None:
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
        self.app.status_var.set(f"Dodan otvor: {kind} / {width:.2f} m")


class LATCESApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1360x850")
        self.minsize(1150, 740)
        self.workflow = new_workflow()
        self.active_mode = tk.StringVar(value="Projektovanje")
        self.tool_var = tk.StringVar(value="select")
        self.step_var = tk.IntVar(value=1)
        self.height_var = tk.StringVar(value="2.80")
        self.model_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Korak 1 — početni tlocrt 10 × 10 m")
        self.selected_length_var = tk.StringVar(value="—")
        self.selected_thickness_var = tk.StringVar(value="0.20")
        self.editor = FloorPlanEditor(self)
        self._build_ui()
        self.redraw_active_view()

    @property
    def floor_plan(self) -> FloorPlan:
        return self.workflow.floor_plan

    @property
    def active_level(self):
        return self.workflow.active_level

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 12))
        header.pack(fill="x")
        ttk.Label(header, text="LAT-CES", font=("Segoe UI", 21, "bold")).pack(side="left")
        ttk.Label(header, text="Building Model", font=("Segoe UI", 11)).pack(side="left", padx=(14, 0), pady=(5, 0))
        ttk.Button(header, text="Učitaj konfiguraciju…", command=self.load_project).pack(side="right")
        ttk.Button(header, text="Sačuvaj konfiguraciju", command=self.save_project).pack(side="right", padx=8)
        ttk.Button(header, text="Novi projekat", command=self.new_project).pack(side="right")

        steps = ttk.Frame(self, padding=(18, 0, 18, 10))
        steps.pack(fill="x")
        for number, title in STEPS:
            ttk.Radiobutton(
                steps,
                text=f"{number}. {title}",
                value=number,
                variable=self.step_var,
                command=self.goto_step,
            ).pack(side="left", padx=(0, 18))

        body = ttk.Frame(self, padding=(18, 0, 18, 12))
        body.pack(fill="both", expand=True)
        self.workspace = ttk.LabelFrame(body, text="Tlocrt", padding=8)
        self.workspace.pack(side="left", fill="both", expand=True)

        toolbar = ttk.Frame(self.workspace)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(toolbar, text="Etaža:").pack(side="left")
        self.level_var = tk.StringVar()
        self.level_box = ttk.Combobox(toolbar, textvariable=self.level_var, state="readonly", width=18)
        self.level_box.pack(side="left", padx=6)
        self.level_box.bind("<<ComboboxSelected>>", self.select_level_from_combo)
        ttk.Label(toolbar, text="|  Uređivanje:").pack(side="left", padx=(8, 0))
        for tool, label in EDITOR_TOOLS:
            ttk.Radiobutton(
                toolbar,
                text=label,
                value=tool,
                variable=self.tool_var,
                command=lambda value=tool: self.editor.set_tool(value),
            ).pack(side="left", padx=(6, 0))
        ttk.Label(toolbar, text="Snap 0.10 m", foreground="#5f6368").pack(side="right")

        self.canvas = tk.Canvas(self.workspace, background="white", highlightthickness=1, highlightbackground="#cfd4da")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.redraw_active_view())
        self.canvas.bind("<Button-1>", self.editor.click)
        self.canvas.bind("<ButtonPress-1>", self.editor.begin_drag)
        self.canvas.bind("<B1-Motion>", self.editor.drag)
        self.canvas.bind("<ButtonRelease-1>", self.editor.end_drag)

        side = ttk.Frame(body, width=350)
        side.pack(side="left", fill="y", padx=(14, 0))
        side.pack_propagate(False)
        self._build_side_panel(side)
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x")

    def _build_side_panel(self, side: ttk.Frame) -> None:
        mode_box = ttk.LabelFrame(side, text="Režim rada", padding=10)
        mode_box.pack(fill="x")
        for mode in MODE_DESCRIPTIONS:
            ttk.Button(mode_box, text=mode, command=lambda value=mode: self.select_mode(value)).pack(fill="x", pady=3)

        step_box = ttk.LabelFrame(side, text="Trenutni korak", padding=10)
        step_box.pack(fill="x", pady=(14, 0))
        self.step_title = ttk.Label(step_box, text="1. Tlocrt", font=("Segoe UI", 14, "bold"))
        self.step_title.pack(anchor="w")
        self.step_info = ttk.Label(step_box, text="Početni kvadrat 10 × 10 m. Dodaj, pomjeraj i mijenjaj zidove.", wraplength=305)
        self.step_info.pack(anchor="w", pady=(4, 8))
        self.step_controls = ttk.Frame(step_box)
        self.step_controls.pack(fill="x")

        selected = ttk.LabelFrame(side, text="Odabrani zid", padding=10)
        selected.pack(fill="x", pady=(14, 0))
        ttk.Label(selected, text="Dužina (m)").grid(row=0, column=0, sticky="w")
        ttk.Entry(selected, textvariable=self.selected_length_var).grid(row=0, column=1, sticky="ew", padx=(8, 0))
        ttk.Label(selected, text="Debljina (m)").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(selected, textvariable=self.selected_thickness_var).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(6, 0))
        ttk.Button(selected, text="Primijeni dimenzije", command=self.apply_wall_dimensions).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        selected.columnconfigure(1, weight=1)

        model_box = ttk.LabelFrame(side, text="Building Model", padding=10)
        model_box.pack(fill="x", pady=(14, 0))
        self.summary_text = tk.Text(model_box, height=8, width=38, wrap="word", state="disabled")
        self.summary_text.pack(fill="x")

        tools = ttk.LabelFrame(side, text="LAT-CES alati", padding=10)
        tools.pack(fill="x", pady=(14, 0))
        ttk.Button(tools, text="Provjeri model", command=self.validate_model).pack(fill="x")
        ttk.Button(tools, text="Scientific Analysis", command=self.open_analysis).pack(fill="x", pady=6)
        ttk.Button(tools, text="Sačuvaj konfiguraciju", command=self.save_project).pack(fill="x")
        ttk.Label(side, text="Svaka etaža ima svoj FloorPlan. Raspored na spratu može biti potpuno drugačiji.", wraplength=305, foreground="#5f6368").pack(anchor="w", pady=(16, 0))
        self.refresh_level_combo()
        self.configure_step(1)

    def refresh_level_combo(self) -> None:
        levels = list(self.workflow.model.levels.values())
        self.level_box["values"] = [f"{idx + 1}. {level.name}" for idx, level in enumerate(levels)]
        active_index = next((idx for idx, level in enumerate(levels) if level.level_id == self.workflow.active_level_id), 0)
        if levels:
            self.level_box.current(active_index)
        self.height_var.set(f"{self.active_level.height:.2f}")

    def select_level_from_combo(self, _event: tk.Event) -> None:
        index = self.level_box.current()
        levels = list(self.workflow.model.levels.values())
        if 0 <= index < len(levels):
            self.workflow.set_active_level(levels[index].level_id)
            self.editor.selected_wall_id = None
            self.update_selected_wall()
            self.height_var.set(f"{self.active_level.height:.2f}")
            self.status_var.set(f"Aktivna etaža: {self.active_level.name}")
            self.redraw_active_view()
            self.update_summary()

    def canvas_to_model(self, x: float, y: float) -> Point2D:
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        xmin, xmax, ymin, ymax = self.plan_bounds()
        margin = 80
        scale = min((width - 2 * margin) / max(xmax - xmin, 1.0), (height - 2 * margin) / max(ymax - ymin, 1.0))
        origin_x = (width - (xmax - xmin) * scale) / 2 - xmin * scale
        origin_y = (height + (ymax - ymin) * scale) / 2 + ymin * scale
        return Point2D((x - origin_x) / scale, (origin_y - y) / scale)

    def model_to_canvas(self, point: Point2D) -> tuple[float, float]:
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        xmin, xmax, ymin, ymax = self.plan_bounds()
        margin = 80
        scale = min((width - 2 * margin) / max(xmax - xmin, 1.0), (height - 2 * margin) / max(ymax - ymin, 1.0))
        origin_x = (width - (xmax - xmin) * scale) / 2 - xmin * scale
        origin_y = (height + (ymax - ymin) * scale) / 2 + ymin * scale
        return origin_x + point.x * scale, origin_y - point.y * scale

    def plan_bounds(self) -> tuple[float, float, float, float]:
        points = []
        for wall in self.floor_plan.walls.values():
            points.extend((wall.segment.start, wall.segment.end))
        if not points:
            return 0.0, 10.0, 0.0, 10.0
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        padding = 1.0
        return min(xs) - padding, max(xs) + padding, min(ys) - padding, max(ys) + padding

    def draw_floor_plan(self) -> None:
        self.canvas.delete("all")
        xmin, xmax, ymin, ymax = self.plan_bounds()
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        margin = 80
        scale = min((width - 2 * margin) / max(xmax - xmin, 1.0), (height - 2 * margin) / max(ymax - ymin, 1.0))
        for x in range(math.floor(xmin), math.ceil(xmax) + 1):
            px, _ = self.model_to_canvas(Point2D(float(x), 0.0))
            self.canvas.create_line(px, 0, px, height, fill="#edf0f2")
        for y in range(math.floor(ymin), math.ceil(ymax) + 1):
            _, py = self.model_to_canvas(Point2D(0.0, float(y)))
            self.canvas.create_line(0, py, width, py, fill="#edf0f2")

        for wall in self.floor_plan.walls.values():
            x1, y1 = self.model_to_canvas(wall.segment.start)
            x2, y2 = self.model_to_canvas(wall.segment.end)
            selected = wall.wall_id == self.editor.selected_wall_id
            self.canvas.create_line(x1, y1, x2, y2, width=10 if selected else 7, fill="#111827" if not selected else "#2563eb")
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my - 10, text=f"{wall.segment.length:.2f} m", fill="#374151", font=("Segoe UI", 9, "bold"))
            for opening in wall.openings:
                t1 = opening.offset / wall.segment.length
                t2 = (opening.offset + opening.width) / wall.segment.length
                ox1 = x1 + (x2 - x1) * t1
                oy1 = y1 + (y2 - y1) * t1
                ox2 = x1 + (x2 - x1) * t2
                oy2 = y1 + (y2 - y1) * t2
                self.canvas.create_line(ox1, oy1, ox2, oy2, width=10, fill="#ffffff")
                self.canvas.create_text((ox1 + ox2) / 2, (oy1 + oy2) / 2 + 12, text=f"{opening.kind} {opening.width:.2f} m", fill="#4b5563", font=("Segoe UI", 8))

        self.canvas.create_text(width - 20, 20, text="Sjever ↑", anchor="ne", fill="#5f6368")
        self.canvas.create_text(20, height - 20, text=f"Aktivna etaža: {self.active_level.name}", anchor="sw", fill="#5f6368")

    def draw_3d(self) -> None:
        self.canvas.delete("all")
        geometries = build_geometry(self.workflow.model)
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        scale = 22.0
        for level_index, geometry in enumerate(geometries):
            z0 = sum(g.height for g in geometries[:level_index])
            for wall in geometry.walls:
                def project(x: float, y: float, z: float) -> tuple[float, float]:
                    return width * 0.25 + x * scale + y * 0.45 * scale, height * 0.72 - z * scale - y * 0.22 * scale
                a0 = project(wall.x1, wall.y1, z0)
                b0 = project(wall.x2, wall.y2, z0)
                a1 = project(wall.x1, wall.y1, z0 + wall.height)
                b1 = project(wall.x2, wall.y2, z0 + wall.height)
                self.canvas.create_line(*a0, *b0, fill="#374151", width=3)
                self.canvas.create_line(*a1, *b1, fill="#6b7280", width=3)
                self.canvas.create_line(*a0, *a1, fill="#9ca3af")
                self.canvas.create_line(*b0, *b1, fill="#9ca3af")
        self.canvas.create_text(20, 20, text="3D Building Model — izvedeno iz svih etaža", anchor="nw", fill="#374151", font=("Segoe UI", 12, "bold"))

    def redraw_active_view(self) -> None:
        self.draw_3d() if self.step_var.get() == 4 else self.draw_floor_plan()

    def refresh_plan(self) -> None:
        self.update_selected_wall()
        self.update_summary()
        self.redraw_active_view()

    def update_selected_wall(self) -> None:
        wall = self.floor_plan.walls.get(self.editor.selected_wall_id) if self.editor.selected_wall_id else None
        self.selected_length_var.set(f"{wall.segment.length:.2f}" if wall else "—")
        self.selected_thickness_var.set(f"{wall.thickness:.2f}" if wall else "0.20")

    def apply_wall_dimensions(self) -> None:
        wall = self.floor_plan.walls.get(self.editor.selected_wall_id) if self.editor.selected_wall_id else None
        if wall is None:
            messagebox.showinfo("LAT-CES", "Prvo odaberi zid.", parent=self)
            return
        try:
            new_length = float(self.selected_length_var.get())
            thickness = float(self.selected_thickness_var.get())
            if new_length <= 0 or thickness <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("LAT-CES", "Dimenzije moraju biti pozitivni brojevi.", parent=self)
            return
        dx = wall.segment.end.x - wall.segment.start.x
        dy = wall.segment.end.y - wall.segment.start.y
        old_length = wall.segment.length
        wall.thickness = thickness
        if old_length > 0:
            ux, uy = dx / old_length, dy / old_length
            wall.segment = Segment2D(wall.segment.start, Point2D(wall.segment.start.x + ux * new_length, wall.segment.start.y + uy * new_length))
        self.refresh_plan()
        self.status_var.set(f"Dimenzije primijenjene: {new_length:.2f} × {thickness:.2f} m")

    def configure_step(self, step: int) -> None:
        for child in self.step_controls.winfo_children():
            child.destroy()
        if step == 1:
            self.workspace.configure(text=f"Tlocrt — {self.active_level.name}")
            self.step_title.configure(text="1. Tlocrt")
            self.step_info.configure(text="Početni projekat je kvadrat 10 × 10 m. Dodaj linije/zidove, pregrade i mijenjaj dimenzije.")
            ttk.Button(self.step_controls, text="Nova pregrada", command=lambda: self.editor.set_tool("draw")).pack(fill="x", pady=3)
        elif step == 2:
            self.workspace.configure(text=f"Visina / spratnost — {self.active_level.name}")
            self.step_title.configure(text="2. Visina / spratnost")
            self.step_info.configure(text="Svaka etaža ima nezavisan tlocrt. Promjena sprata ne kopira raspored prethodnog sprata.")
            ttk.Label(self.step_controls, text="Visina aktivne etaže (m)").pack(anchor="w")
            ttk.Entry(self.step_controls, textvariable=self.height_var).pack(fill="x", pady=4)
            ttk.Button(self.step_controls, text="Primijeni visinu", command=self.apply_height).pack(fill="x", pady=3)
            ttk.Button(self.step_controls, text="Dodaj novu etažu", command=self.add_level).pack(fill="x", pady=3)
            ttk.Label(self.step_controls, text="Novi sprat dobija svoj prazan kvadratni tlocrt.", wraplength=300, foreground="#5f6368").pack(anchor="w", pady=(6, 0))
        elif step == 3:
            self.workspace.configure(text=f"Otvori — {self.active_level.name}")
            self.step_title.configure(text="3. Otvori")
            self.step_info.configure(text="Vrata i prozori pripadaju aktivnoj etaži. Raspored je nezavisan po spratu.")
            ttk.Button(self.step_controls, text="Dodaj vrata", command=lambda: self.editor.set_tool("door")).pack(fill="x", pady=3)
            ttk.Button(self.step_controls, text="Dodaj prozor", command=lambda: self.editor.set_tool("window")).pack(fill="x", pady=3)
        else:
            self.workspace.configure(text="3D Building Model")
            self.step_title.configure(text="4. 3D model")
            self.step_info.configure(text="Prikaz se izvodi iz svih nezavisnih etaža i njihovih tlocrta.")
            ttk.Button(self.step_controls, text="← Nazad na tlocrt", command=lambda: (self.step_var.set(1), self.goto_step())).pack(fill="x")

    def goto_step(self) -> None:
        step = self.step_var.get()
        if step >= 3:
            self.workflow.advance_to_openings()
        if step >= 4:
            self.workflow.advance_to_3d()
        self.configure_step(step)
        self.redraw_active_view()
        self.update_summary()

    def apply_height(self) -> None:
        try:
            self.workflow.set_active_level_height(float(self.height_var.get()))
            self.workflow.model.levels
        except ValueError as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)
            return
        self.update_summary()
        self.redraw_active_view()
        self.status_var.set(f"Visina {self.active_level.name}: {self.active_level.height:.2f} m")

    def add_level(self) -> None:
        number = len(self.workflow.model.levels) + 1
        level = self.workflow.add_level(f"Etaža {number}", float(self.height_var.get() or 2.80))
        self.height_var.set(f"{level.height:.2f}")
        self.refresh_level_combo()
        self.step_var.set(1)
        self.configure_step(1)
        self.redraw_active_view()
        self.update_summary()
        self.status_var.set(f"Dodana {level.name} — novi nezavisni tlocrt")

    def select_mode(self, mode: str) -> None:
        self.active_mode.set(mode)
        self.status_var.set(f"Režim: {mode} — Building Model ostaje centralni model")

    def validate_model(self) -> None:
        findings = self.workflow.validate()
        if findings:
            messagebox.showwarning("LAT-CES — Provjera", "\n".join(findings), parent=self)
            self.status_var.set(f"Model nije validan: {len(findings)} nalaza")
        else:
            messagebox.showinfo("LAT-CES — Provjera", "Building Model je geometrijski validan.", parent=self)
            self.status_var.set("Building Model je validan")

    def update_summary(self) -> None:
        data = self.workflow.summary()
        levels = [f"{idx + 1}. {level.name}: {level.height:.2f} m" for idx, level in enumerate(self.workflow.model.levels.values())]
        text = (
            f"Objekat: {data['model']}\n"
            f"Etaže: {data['levels']}\n"
            f"Aktivna: {data['active_level']}\n"
            f"Površina: {data['floor_area_m2']:.2f} m²\n"
            f"Zapremina: {data['volume_m3']:.2f} m³\n"
            f"Korak: {data['step']}\n\n" + "\n".join(levels)
        )
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", text)
        self.summary_text.configure(state="disabled")

    def save_project(self) -> None:
        target = self.model_path.get()
        if not target:
            target = filedialog.asksaveasfilename(
                title="Sačuvaj Building Model konfiguraciju",
                defaultextension=".json",
                filetypes=(("LAT-CES Building JSON", "*.json"), ("All files", "*.*")),
                initialfile="building_model.json",
            )
        if not target:
            return
        try:
            save_workflow(self.workflow, target)
            self.model_path.set(target)
            self.status_var.set(f"Konfiguracija sačuvana: {target}")
        except Exception as exc:
            messagebox.showerror("LAT-CES", str(exc), parent=self)

    def load_project(self) -> None:
        target = filedialog.askopenfilename(
            title="Učitaj Building Model konfiguraciju",
            filetypes=(("LAT-CES Building JSON", "*.json"), ("All files", "*.*")),
        )
        if not target:
            return
        try:
            self.workflow = load_workflow(target)
            self.editor = FloorPlanEditor(self)
            self.model_path.set(target)
            self.step_var.set(min(self.workflow.current_step, 4))
            self.refresh_level_combo()
            self.configure_step(self.step_var.get())
            self.redraw_active_view()
            self.update_summary()
            self.status_var.set(f"Konfiguracija učitana: {target}")
        except Exception as exc:
            messagebox.showerror("LAT-CES", str(exc), parent=self)

    def new_project(self) -> None:
        self.workflow = new_workflow()
        self.editor = FloorPlanEditor(self)
        self.model_path.set("")
        self.step_var.set(1)
        self.refresh_level_combo()
        self.configure_step(1)
        self.redraw_active_view()
        self.update_summary()
        self.status_var.set("Novi projekat — početni kvadrat 10 × 10 m")

    def open_analysis(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("LAT-CES — Scientific Analysis")
        dialog.geometry("860x620")
        dialog.transient(self)
        cfg = ttk.Frame(dialog, padding=14)
        cfg.pack(fill="x")
        path_var = tk.StringVar()
        output_var = tk.StringVar()
        ttk.Label(cfg, text="JSON konfiguracija:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cfg, textvariable=path_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(cfg, text="Browse…", command=lambda: path_var.set(filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*"))))).grid(row=0, column=2)
        ttk.Label(cfg, text="Output:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(cfg, textvariable=output_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=(8, 0))
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
                output = Path(output_var.get().strip() or config_file.with_name("latces_report.json"))
                export_report(exporter, output, "json")
                content = json.loads(exporter.to_json())
                result.delete("1.0", "end")
                result.insert("1.0", f"Status: [{report.status.value}]\nReport: {output}\n\n{json.dumps(content, indent=2, ensure_ascii=False)}")
            except Exception as exc:
                result.delete("1.0", "end")
                result.insert("1.0", f"Analysis failed:\n\n{exc}")

        ttk.Button(dialog, text="Run Analysis", command=run).pack(pady=(0, 14))


def main() -> None:
    LATCESApp().mainloop()


if __name__ == "__main__":
    main()
