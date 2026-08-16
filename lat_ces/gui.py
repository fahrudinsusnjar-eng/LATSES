"""LAT-CES Building-first desktop application.

Project order: floor plan -> level height/floors -> openings -> 3-D model.
Scientific systems are downstream of the same BuildingModel.
"""
from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from lat_ces.application.service import analyze_config, export_report, load_config
from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall
from lat_ces.building.geometry3d import LevelGeometry3D
from lat_ces.building.model import BuildingModel
from lat_ces.building.workflow import BuildingWorkflow

MODE_DESCRIPTIONS = {
    "Projektovanje": "Tlocrt, prostorije, zidovi i otvori",
    "Geometrija": "Visine, spratovi i 3D geometrija",
    "Instalacije": "HVAC, FluidNetwork, voda i električne instalacije",
    "Konstrukcija": "Opterećenja, statika i mehanika konstrukcija",
    "Simulacija": "Fluidika, termika, akustika i energija",
    "Provjera i izvještaj": "Verifikacija, sigurnost i izvještaji",
}
EDITOR_TOOLS = (("select", "Izaberi"), ("draw", "Nacrtaj zid"), ("move", "Pomjeri"), ("delete", "Obriši"), ("door", "Vrata"), ("window", "Prozor"))
STEPS = ((1, "Tlocrt"), (2, "Visina / spratnost"), (3, "Otvori"), (4, "3D model"))


def build_default_floor_plan() -> FloorPlan:
    plan = FloorPlan(name="Novi objekat")
    walls = [("Sjever", (0, 0, 12, 0)), ("Jug", (0, 8, 12, 8)), ("Zapad", (0, 0, 0, 8)), ("Istok", (12, 0, 12, 8)), ("Pregrada 1", (7, 0, 7, 4.8)), ("Pregrada 2", (0, 4.8, 7, 4.8))]
    for name, (x1, y1, x2, y2) in walls:
        plan.add_wall(Wall(name=name, segment=Segment2D(Point2D(x1, y1), Point2D(x2, y2)), thickness=0.20))
    return plan


def new_workflow() -> BuildingWorkflow:
    workflow = BuildingWorkflow(model=BuildingModel(name="Novi objekat"))
    workflow.set_floor_plan(build_default_floor_plan())
    return workflow


class FloorPlanEditor:
    def __init__(self, app: "LATCESApp") -> None:
        self.app, self.tool = app, "select"
        self.start_point = self.selected_wall_id = self.drag_last = None

    def set_tool(self, tool: str) -> None:
        self.tool, self.start_point, self.drag_last = tool, None, None
        self.app.tool_var.set(tool)
        self.app.status_var.set(f"Alat: {dict(EDITOR_TOOLS)[tool]}")
        self.app.draw_floor_plan()

    @staticmethod
    def snap(point: Point2D) -> Point2D:
        return Point2D(round(point.x * 10) / 10.0, round(point.y * 10) / 10.0)

    @property
    def floor_plan(self) -> FloorPlan:
        return self.app.floor_plan

    def click(self, event: tk.Event) -> None:
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        if self.tool == "draw":
            if self.start_point is None:
                self.start_point = point
                self.app.status_var.set("Početak zida postavljen — klikni završnu tačku")
                return
            if math.hypot(point.x - self.start_point.x, point.y - self.start_point.y) < 0.05:
                return
            wall = Wall(name=f"Zid {self.floor_plan.wall_count + 1}", segment=Segment2D(self.start_point, point), thickness=0.20)
            self.floor_plan.add_wall(wall)
            self.start_point = None
            self.app.refresh_plan()
            self.app.status_var.set(f"Dodan zid: {wall.name}")
            return
        wall = self.app.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = None
            self.app.draw_floor_plan()
            return
        self.selected_wall_id = wall.wall_id
        if self.tool == "delete":
            del self.floor_plan.walls[wall.wall_id]
            self.selected_wall_id = None
            self.app.refresh_plan()
            self.app.status_var.set(f"Obrisan zid: {wall.name}")
        elif self.tool in {"door", "window"}:
            self.add_opening(wall, point, self.tool)
        else:
            self.app.draw_floor_plan()
            self.app.status_var.set(f"Izabran: {wall.name}")

    def begin_drag(self, event: tk.Event) -> None:
        if self.tool != "move":
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        wall = self.app.nearest_wall(point)
        if wall is None:
            self.selected_wall_id = self.drag_last = None
            return
        self.selected_wall_id, self.drag_last = wall.wall_id, point

    def drag(self, event: tk.Event) -> None:
        if self.tool != "move" or self.selected_wall_id is None or self.drag_last is None:
            return
        wall = self.floor_plan.walls.get(self.selected_wall_id)
        if wall is None:
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        dx, dy = point.x - self.drag_last.x, point.y - self.drag_last.y
        wall.segment = Segment2D(Point2D(wall.segment.start.x + dx, wall.segment.start.y + dy), Point2D(wall.segment.end.x + dx, wall.segment.end.y + dy))
        self.drag_last = point
        self.app.refresh_plan()

    def end_drag(self, _event: tk.Event) -> None:
        self.drag_last = None

    def add_opening(self, wall: Wall, point: Point2D, kind: str) -> None:
        length = wall.segment.length
        dx, dy = wall.segment.end.x - wall.segment.start.x, wall.segment.end.y - wall.segment.start.y
        projection = ((point.x - wall.segment.start.x) * dx + (point.y - wall.segment.start.y) * dy) / (length * length)
        offset = max(0.0, min(length, projection * length))
        default_width = 0.90 if kind == "door" else 1.20
        width = simpledialog.askfloat("Otvor", f"Širina {kind} (m):", initialvalue=default_width, minvalue=0.10, parent=self.app)
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


class LATCESApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1320x820")
        self.minsize(1100, 720)
        self.workflow, self.floor_plan = new_workflow(), None
        self.floor_plan = self.workflow.floor_plan
        self.active_mode = tk.StringVar(value="Projektovanje")
        self.tool_var = tk.StringVar(value="select")
        self.step_var = tk.IntVar(value=1)
        self.status_var = tk.StringVar(value="Korak 1 — Tlocrt")
        self.model_path = tk.StringVar()
        self.format_var = tk.StringVar(value="json")
        self.height_var = tk.StringVar(value="2.80")
        self.editor = FloorPlanEditor(self)
        self._build_ui()
        self.draw_floor_plan()

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 14)); header.pack(fill="x")
        ttk.Label(header, text="LAT-CES", font=("Segoe UI", 21, "bold")).pack(side="left")
        ttk.Label(header, text="Building Model", font=("Segoe UI", 11)).pack(side="left", padx=(14, 0), pady=(5, 0))
        ttk.Button(header, text="Novi projekat", command=self.new_project).pack(side="right")
        ttk.Button(header, text="Sačuvaj model", command=self.export_project).pack(side="right", padx=8)
        steps = ttk.Frame(self, padding=(18, 0, 18, 10)); steps.pack(fill="x")
        for number, title in STEPS:
            ttk.Radiobutton(steps, text=f"{number}. {title}", value=number, variable=self.step_var, command=self.goto_step).pack(side="left", padx=(0, 16))
        body = ttk.Frame(self, padding=(18, 0, 18, 12)); body.pack(fill="both", expand=True)
        self.workspace = ttk.LabelFrame(body, text="Tlocrt", padding=8); self.workspace.pack(side="left", fill="both", expand=True)
        self._build_workspace_toolbar()
        self.canvas = tk.Canvas(self.workspace, background="white", highlightthickness=1, highlightbackground="#cfd4da"); self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.redraw_active_view())
        self.canvas.bind("<Button-1>", self.editor.click); self.canvas.bind("<ButtonPress-1>", self.editor.begin_drag); self.canvas.bind("<B1-Motion>", self.editor.drag); self.canvas.bind("<ButtonRelease-1>", self.editor.end_drag)
        side = ttk.Frame(body, width=330); side.pack(side="left", fill="y", padx=(14, 0)); side.pack_propagate(False)
        self._build_side_panel(side)
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x")

    def _build_workspace_toolbar(self) -> None:
        if hasattr(self, "workspace_toolbar"):
            return
        self.workspace_toolbar = ttk.Frame(self.workspace); self.workspace_toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(self.workspace_toolbar, text="Uređivanje:").pack(side="left")
        for tool, label in EDITOR_TOOLS:
            ttk.Radiobutton(self.workspace_toolbar, text=label, value=tool, variable=self.tool_var, command=lambda value=tool: self.editor.set_tool(value)).pack(side="left", padx=(6, 0))
        ttk.Label(self.workspace_toolbar, text="Snap 0.10 m", foreground="#5f6368").pack(side="right")

    def _build_side_panel(self, side: ttk.Frame) -> None:
        mode_box = ttk.LabelFrame(side, text="Režim rada", padding=10); mode_box.pack(fill="x")
        for mode in MODE_DESCRIPTIONS:
            ttk.Button(mode_box, text=mode, command=lambda value=mode: self.select_mode(value)).pack(fill="x", pady=3)
        self.step_box = ttk.LabelFrame(side, text="Trenutni korak", padding=10); self.step_box.pack(fill="x", pady=(14, 0))
        self.step_title = ttk.Label(self.step_box, text="1. Tlocrt", font=("Segoe UI", 14, "bold")); self.step_title.pack(anchor="w")
        self.step_info = ttk.Label(self.step_box, text="Nacrtaj ili izmijeni zidove.", wraplength=290); self.step_info.pack(anchor="w", pady=(4, 8))
        self.step_controls = ttk.Frame(self.step_box); self.step_controls.pack(fill="x")
        summary = ttk.LabelFrame(side, text="Building Model", padding=10); summary.pack(fill="x", pady=(14, 0))
        self.summary_text = tk.Text(summary, height=7, width=36, wrap="word", state="disabled"); self.summary_text.pack(fill="x")
        tools = ttk.LabelFrame(side, text="LAT-CES alati", padding=10); tools.pack(fill="x", pady=(14, 0))
        ttk.Button(tools, text="Provjeri model", command=self.validate_model).pack(fill="x")
        ttk.Button(tools, text="Scientific Analysis", command=self.open_analysis).pack(fill="x", pady=6)
        ttk.Button(tools, text="Sačuvaj model", command=self.export_project).pack(fill="x")
        ttk.Label(side, text="Princip: jedan Building Model, zatim svi naučni sistemi na njemu.", wraplength=290, foreground="#5f6368").pack(anchor="w", pady=(16, 0))
        self.update_summary()

    @property
    def active_level(self): return self.workflow.active_level

    def redraw_active_view(self) -> None:
        self.draw_3d() if self.step_var.get() == 4 else self.draw_floor_plan()

    def goto_step(self) -> None:
        step = self.step_var.get()
        if step == 3: self.workflow.advance_to_openings()
        if step == 4: self.workflow.advance_to_3d()
        self.configure_step(step); self.redraw_active_view(); self.update_summary()

    def configure_step(self, step: int) -> None:
        for child in self.step_controls.winfo_children(): child.destroy()
        if step == 1:
            self.workspace.configure(text="Tlocrt"); self.step_title.configure(text="1. Tlocrt"); self.step_info.configure(text="Nacrtaj i izmijeni zidove. Vrata i prozori dolaze u koraku 3.")
        elif step == 2:
            self.workspace.configure(text="Visina / spratnost"); self.step_title.configure(text="2. Visina / spratnost"); self.step_info.configure(text="Definiši visinu etaže i dodaj spratove. Svi nivoi ostaju u istom BuildingModelu.")
            ttk.Label(self.step_controls, text="Visina aktivne etaže (m)").pack(anchor="w"); ttk.Entry(self.step_controls, textvariable=self.height_var).pack(fill="x", pady=4)
            ttk.Button(self.step_controls, text="Primijeni visinu", command=self.apply_height).pack(fill="x", pady=3); ttk.Button(self.step_controls, text="Dodaj sprat", command=self.add_level).pack(fill="x", pady=3)
            ttk.Button(self.step_controls, text="Sljedeće: Otvori →", command=lambda: (self.step_var.set(3), self.goto_step())).pack(fill="x", pady=(8, 0))
        elif step == 3:
            self.workspace.configure(text="Otvori — vrata i prozori"); self.step_title.configure(text="3. Otvori"); self.step_info.configure(text="Na odabranom zidu dodaj vrata ili prozor. Otvori su dio fizičkog modela.")
            ttk.Button(self.step_controls, text="Vrata", command=lambda: self.editor.set_tool("door")).pack(fill="x", pady=3); ttk.Button(self.step_controls, text="Prozor", command=lambda: self.editor.set_tool("window")).pack(fill="x", pady=3)
            ttk.Button(self.step_controls, text="Sljedeće: 3D model →", command=lambda: (self.step_var.set(4), self.goto_step())).pack(fill="x", pady=(8, 0))
        else:
            self.workspace.configure(text="3D Building Model"); self.step_title.configure(text="4. 3D model"); self.step_info.configure(text="3D geometrija je izvedena iz iste 2D FloorPlan + etaža. Nema paralelnog modela.")
            ttk.Button(self.step_controls, text="← Nazad na tlocrt", command=lambda: (self.step_var.set(1), self.goto_step())).pack(fill="x")

    def select_mode(self, mode: str) -> None: self.active_mode.set(mode); self.status_var.set(f"Režim: {mode} — Building Model ostaje centralni model")

    def apply_height(self) -> None:
        try: self.workflow.set_active_level_height(float(self.height_var.get().strip()))
        except (ValueError, TypeError) as exc: messagebox.showwarning("LAT-CES", str(exc), parent=self); return
        self.refresh_plan(); self.status_var.set(f"Visina {self.active_level.name}: {self.active_level.height:.2f} m")

    def add_level(self) -> None:
        name = simpledialog.askstring("Sprat", "Naziv sprata:", initialvalue=f"Sprat {len(self.workflow.model.levels)}", parent=self)
        if not name: return
        height = simpledialog.askfloat("Sprat", "Visina sprata (m):", initialvalue=2.80, minvalue=0.1, parent=self)
        if height is None: return
        level = self.workflow.add_level(name, height); level.set_floor_plan(build_default_floor_plan()); self.floor_plan = level.floor_plan; self.height_var.set(f"{height:.2f}"); self.refresh_plan(); self.status_var.set(f"Dodan {level.name}, elevacija {level.elevation:.2f} m")

    def new_project(self) -> None:
        self.workflow = new_workflow(); self.floor_plan = self.workflow.floor_plan; self.height_var.set("2.80"); self.step_var.set(1); self.configure_step(1); self.refresh_plan(); self.status_var.set("Novi projekat — Korak 1: Tlocrt")

    def refresh_plan(self) -> None: self.floor_plan = self.workflow.floor_plan; self.draw_floor_plan(); self.update_summary()

    def nearest_wall(self, point: Point2D, tolerance_m: float = 0.30) -> Wall | None:
        best = None
        for wall in self.floor_plan.walls.values():
            dx, dy = wall.segment.end.x - wall.segment.start.x, wall.segment.end.y - wall.segment.start.y; ls = dx * dx + dy * dy
            if ls == 0: distance = math.hypot(point.x - wall.segment.start.x, point.y - wall.segment.start.y)
            else:
                t = max(0.0, min(1.0, ((point.x - wall.segment.start.x) * dx + (point.y - wall.segment.start.y) * dy) / ls)); px, py = wall.segment.start.x + t * dx, wall.segment.start.y + t * dy; distance = math.hypot(point.x - px, point.y - py)
            if distance <= tolerance_m and (best is None or distance < best[0]): best = (distance, wall)
        return best[1] if best else None

    def model_to_canvas(self, point: Point2D) -> tuple[float, float]:
        width, height = max(self.canvas.winfo_width(), 400), max(self.canvas.winfo_height(), 300); margin = 70; scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0); ox, oy = (width - 12.0 * scale) / 2, (height - 8.0 * scale) / 2; return ox + point.x * scale, oy + point.y * scale

    def canvas_to_model(self, x: float, y: float) -> Point2D:
        width, height = max(self.canvas.winfo_width(), 400), max(self.canvas.winfo_height(), 300); margin = 70; scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0); ox, oy = (width - 12.0 * scale) / 2, (height - 8.0 * scale) / 2; return Point2D((x - ox) / scale, (y - oy) / scale)

    def draw_floor_plan(self) -> None:
        self.canvas.delete("all"); width, height = max(self.canvas.winfo_width(), 400), max(self.canvas.winfo_height(), 300); margin = 70; scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0); ox, oy = (width - 12.0 * scale) / 2, (height - 8.0 * scale) / 2
        for x in range(13): self.canvas.create_line(ox + x * scale, oy, ox + x * scale, oy + 8 * scale, fill="#edf0f2")
        for y in range(9): self.canvas.create_line(ox, oy + y * scale, ox + 12 * scale, oy + y * scale, fill="#edf0f2")
        for wall in self.floor_plan.walls.values():
            x1, y1 = self.model_to_canvas(wall.segment.start); x2, y2 = self.model_to_canvas(wall.segment.end); self.canvas.create_line(x1, y1, x2, y2, width=max(4, int(wall.thickness * scale)), fill="#374151")
            for opening in wall.openings:
                ratio = opening.offset / wall.segment.length; cx, cy = wall.segment.start.x + (wall.segment.end.x - wall.segment.start.x) * ratio, wall.segment.start.y + (wall.segment.end.y - wall.segment.start.y) * ratio; ex, ey = wall.segment.end.x - wall.segment.start.x, wall.segment.end.y - wall.segment.start.y; l = wall.segment.length; a, b = self.model_to_canvas(Point2D(cx, cy)), self.model_to_canvas(Point2D(cx + ex / l * opening.width, cy + ey / l * opening.width)); self.canvas.create_line(a[0], a[1], b[0], b[1], width=10, fill="white"); self.canvas.create_line(a[0], a[1], b[0], b[1], width=3, fill="#2563eb" if opening.kind == "window" else "#b45309")
        self.canvas.create_text(width - 18, 18, text=f"Nivo: {self.active_level.name} | h={self.active_level.height:.2f} m", anchor="ne", fill="#5f6368"); self.canvas.create_text(width - 18, 38, text="Sjever ↑", anchor="ne", fill="#5f6368")

    def draw_3d(self) -> None:
        self.canvas.delete("all")
        geometries: tuple[LevelGeometry3D, ...] = self.workflow.advance_to_3d(); width, height = max(self.canvas.winfo_width(), 400), max(self.canvas.winfo_height(), 300); scale = min((width - 160) / 12.0, (height - 180) / 8.0); ox, oy, z_scale = 90, height - 90, 35
        for index, geometry in enumerate(geometries):
            z = sum(g.height for g in geometries[:index])
            for wall in geometry.walls:
                x1, y1 = ox + wall.x1 * scale, oy - wall.y1 * scale - z * z_scale; x2, y2 = ox + wall.x2 * scale, oy - wall.y2 * scale - z * z_scale; top1, top2 = y1 - wall.height * z_scale, y2 - wall.height * z_scale; self.canvas.create_polygon(x1, y1, x2, y2, top2, top1, fill="#d1d5db", outline="#374151")
        self.canvas.create_text(20, 20, text="3D Building Model — izveden iz FloorPlan + Level", anchor="nw", font=("Segoe UI", 12, "bold")); self.canvas.create_text(20, 44, text=f"Etaže: {len(geometries)} | Ukupna visina: {sum(g.height for g in geometries):.2f} m", anchor="nw", fill="#5f6368")

    def update_summary(self) -> None:
        summary = self.workflow.summary(); openings = sum(len(w.openings) for l in self.workflow.model.levels.values() if l.floor_plan for w in l.floor_plan.walls.values()); text = f"Objekat: {summary['model']}\nEtaže: {summary['levels']}\nAktivna etaža: {summary['active_level']}\nZidovi: {self.floor_plan.wall_count}\nOtvori: {openings}\nPovršina: {summary['floor_area_m2']:.2f} m²\nVolumen: {summary['volume_m3']:.2f} m³"; self.summary_text.configure(state="normal"); self.summary_text.delete("1.0", "end"); self.summary_text.insert("1.0", text); self.summary_text.configure(state="disabled")

    def validate_model(self) -> None:
        findings = self.workflow.validate()
        if findings: messagebox.showwarning("LAT-CES", "\n".join(findings), parent=self); self.status_var.set(f"Provjera: {len(findings)} nalaza")
        else: messagebox.showinfo("LAT-CES", "Building Model je validan.", parent=self); self.status_var.set("Building Model: validan")

    def export_project(self) -> None:
        target = filedialog.asksaveasfilename(title="Sačuvaj Building Model", defaultextension=".json", filetypes=(("JSON files", "*.json"),), initialfile="building_model.json")
        if not target: return
        payload = {"name": self.workflow.model.name, "model_id": self.workflow.model.model_id, "levels": [{"name": level.name, "elevation_m": level.elevation, "height_m": level.height, "walls": [{"name": wall.name, "start": {"x_m": wall.segment.start.x, "y_m": wall.segment.start.y}, "end": {"x_m": wall.segment.end.x, "y_m": wall.segment.end.y}, "thickness_m": wall.thickness, "openings": [{"kind": o.kind, "offset_m": o.offset, "width_m": o.width} for o in wall.openings]} for wall in (level.floor_plan.walls.values() if level.floor_plan else ())]} for level in self.workflow.model.levels.values()]}
        Path(target).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"); self.model_path.set(target); self.status_var.set(f"Building Model sačuvan: {target}")

    def open_analysis(self) -> None:
        dialog = tk.Toplevel(self); dialog.title("LAT-CES — Scientific Analysis"); dialog.geometry("860x620"); path_var, output_var = tk.StringVar(), tk.StringVar(); cfg = ttk.Frame(dialog, padding=14); cfg.pack(fill="x")
        ttk.Label(cfg, text="JSON konfiguracija:").grid(row=0, column=0, sticky="w"); ttk.Entry(cfg, textvariable=path_var).grid(row=0, column=1, sticky="ew", padx=8); ttk.Button(cfg, text="Browse…", command=lambda: path_var.set(filedialog.askopenfilename(filetypes=(("JSON files", "*.json"),)))).grid(row=0, column=2); ttk.Label(cfg, text="Format:").grid(row=1, column=0, sticky="w", pady=(8, 0)); ttk.Combobox(cfg, textvariable=self.format_var, values=("json", "md"), state="readonly", width=10).grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0)); cfg.columnconfigure(1, weight=1)
        result = tk.Text(dialog, wrap="word", font=("Consolas", 10)); result.pack(fill="both", expand=True, padx=14, pady=8)
        def run() -> None:
            config_file = Path(path_var.get().strip())
            if not config_file.exists(): messagebox.showwarning("LAT-CES", "Odaberi validnu JSON konfiguraciju.", parent=dialog); return
            try:
                config = load_config(config_file); report, exporter = analyze_config(config, project_default="LAT-CES Desktop Analysis", plenum_default="PLENUM-GUI-01", equation_default="Custom equation"); fmt = self.format_var.get(); output = Path(output_var.get().strip() or config_file.with_name(f"latces_report.{fmt}")); export_report(exporter, output, fmt); content = json.loads(exporter.to_json()) if fmt == "json" else exporter.to_markdown(); display = json.dumps(content, indent=2, ensure_ascii=False) if isinstance(content, dict) else content; result.delete("1.0", "end"); result.insert("1.0", f"Status: [{report.status.value}]\nReport: {output}\n\n{display}")
            except Exception as exc: result.delete("1.0", "end"); result.insert("1.0", f"Analysis failed:\n\n{exc}"); messagebox.showerror("LAT-CES analysis error", str(exc), parent=dialog)
        ttk.Button(dialog, text="Run Analysis", command=run).pack(pady=(0, 14))


def main() -> None: LATCESApp().mainloop()


if __name__ == "__main__": main()
