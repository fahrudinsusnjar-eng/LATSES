"""LAT-CES Building-first desktop UI.

The project starts with an empty floor plan. A compact sequential setup then
collects the ground floor, optional floors 1-2, and roof before creating 3-D.
"""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall
from lat_ces.building.geometry3d import build_geometry
from lat_ces.building.model import BuildingModel
from lat_ces.building.project_io import load_workflow, save_workflow
from lat_ces.building.setup_wizard_v3 import SetupWizardV3
from lat_ces.building.workflow import BuildingWorkflow, make_blank_floor_plan

MODES = (
    ("Projektovanje", "Tlocrt, dimenzije, pregrade, prostorije i otvori"),
    ("Geometrija", "Etaže, visine, krov i 3D model"),
    ("Instalacije", "HVAC, FluidNetwork, voda i električne instalacije"),
    ("Konstrukcija", "Opterećenja, statika i mehanika konstrukcija"),
    ("Simulacija", "Fluidika, termika, akustika i energija"),
    ("Provjera i izvještaj", "Verifikacija, sigurnost i izvještaji"),
)
TOOLS = (("select", "Izaberi"), ("draw", "Nova linija / zid"), ("move", "Pomjeri"), ("delete", "Obriši"), ("door", "Vrata"), ("window", "Prozor"))


def blank_workflow() -> BuildingWorkflow:
    model = BuildingModel("Novi objekat")
    workflow = BuildingWorkflow(model=model)
    workflow.set_floor_plan(make_blank_floor_plan("Prizemlje"))
    return workflow


class FloorEditor:
    def __init__(self, app: "LATCESBuildingApp") -> None:
        self.app, self.tool = app, "select"
        self.start: Point2D | None = None
        self.selected: str | None = None
        self.drag_last: Point2D | None = None

    @property
    def plan(self) -> FloorPlan:
        return self.app.workflow.floor_plan

    @staticmethod
    def snap(point: Point2D) -> Point2D:
        return Point2D(round(point.x * 10) / 10, round(point.y * 10) / 10)

    @staticmethod
    def distance(point: Point2D, start: Point2D, end: Point2D) -> float:
        dx, dy = end.x - start.x, end.y - start.y
        d2 = dx * dx + dy * dy
        if d2 == 0:
            return math.hypot(point.x - start.x, point.y - start.y)
        t = max(0.0, min(1.0, ((point.x-start.x)*dx + (point.y-start.y)*dy) / d2))
        px, py = start.x + t * dx, start.y + t * dy
        return math.hypot(point.x - px, point.y - py)

    def nearest(self, point: Point2D, tolerance: float = 0.25) -> Wall | None:
        best: tuple[float, Wall] | None = None
        for wall in self.plan.walls.values():
            distance = self.distance(point, wall.segment.start, wall.segment.end)
            if distance <= tolerance and (best is None or distance < best[0]):
                best = (distance, wall)
        return best[1] if best else None

    def set_tool(self, tool: str) -> None:
        self.tool, self.start, self.drag_last = tool, None, None
        self.app.tool_var.set(tool)
        self.app.status.set(f"Alat: {dict(TOOLS)[tool]}")
        self.app.redraw()

    def click(self, event: tk.Event) -> None:
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        if self.tool == "draw":
            if self.start is None:
                self.start = point
                self.app.status.set(f"Početak: {point.x:.1f}, {point.y:.1f} m — klikni kraj")
                return
            if math.hypot(point.x - self.start.x, point.y - self.start.y) < 0.1:
                return
            wall = Wall(f"Zid {self.plan.wall_count + 1}", Segment2D(self.start, point), thickness=0.20)
            self.plan.add_wall(wall)
            self.selected = wall.wall_id
            self.start = None
            self.app.refresh()
            return
        wall = self.nearest(point)
        if wall is None:
            self.selected = None
            self.app.refresh()
            return
        self.selected = wall.wall_id
        if self.tool == "delete":
            del self.plan.walls[wall.wall_id]
            self.selected = None
            self.app.refresh()
            return
        if self.tool in {"door", "window"}:
            self.add_opening(wall, point, self.tool)
            return
        self.app.update_selection()

    def begin_drag(self, event: tk.Event) -> None:
        if self.tool != "move":
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        wall = self.nearest(point)
        if wall:
            self.selected, self.drag_last = wall.wall_id, point

    def drag(self, event: tk.Event) -> None:
        if self.tool != "move" or not self.selected or self.drag_last is None:
            return
        wall = self.plan.walls.get(self.selected)
        if wall is None:
            return
        point = self.snap(self.app.canvas_to_model(event.x, event.y))
        dx, dy = point.x - self.drag_last.x, point.y - self.drag_last.y
        wall.segment = Segment2D(
            Point2D(wall.segment.start.x + dx, wall.segment.start.y + dy),
            Point2D(wall.segment.end.x + dx, wall.segment.end.y + dy),
        )
        self.drag_last = point
        self.app.refresh()

    def end_drag(self, _event: tk.Event) -> None:
        self.drag_last = None

    def add_opening(self, wall: Wall, point: Point2D, kind: str) -> None:
        dx, dy = wall.segment.end.x-wall.segment.start.x, wall.segment.end.y-wall.segment.start.y
        length = wall.segment.length
        t = max(0.0, min(1.0, ((point.x-wall.segment.start.x)*dx + (point.y-wall.segment.start.y)*dy)/(length*length)))
        offset = t * length
        default = 0.90 if kind == "door" else 1.20
        width = simpledialog.askfloat("Otvor", f"Širina {kind} (m)", initialvalue=default, minvalue=0.1, parent=self.app)
        if width is None:
            return
        offset = min(max(0.0, offset - width/2), max(0.0, length-width))
        try:
            wall.add_opening(Opening(kind, offset, width))
        except ValueError as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self.app)
            return
        self.app.refresh()


class LATCESBuildingApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1360x850")
        self.minsize(1150,740)
        self.workflow = blank_workflow()
        self.mode = tk.StringVar(value="Projektovanje")
        self.tool_var = tk.StringVar(value="select")
        self.level_var = tk.StringVar(value="Prizemlje")
        self.status = tk.StringVar(value="Prazan projekat — započnite unos objekta")
        self.sel_length = tk.StringVar(value="")
        self.sel_thickness = tk.StringVar(value="0.20")
        self.editor = FloorEditor(self)
        self._ui()
        self.redraw()
        self.after(150, self.open_setup)

    @property
    def plan(self) -> FloorPlan:
        return self.workflow.floor_plan

    @property
    def level(self):
        return self.workflow.active_level

    def _ui(self) -> None:
        head = ttk.Frame(self, padding=(18,12)); head.pack(fill="x")
        ttk.Label(head, text="LAT-CES", font=("Segoe UI",21,"bold")).pack(side="left")
        ttk.Label(head, text="Building Model", font=("Segoe UI",11)).pack(side="left", padx=(14,0), pady=(5,0))
        ttk.Button(head,text="Postavi projekat",command=self.open_setup).pack(side="right")
        ttk.Button(head,text="Učitaj",command=self.load_project).pack(side="right",padx=6)
        ttk.Button(head,text="Sačuvaj",command=self.save_project).pack(side="right")
        body=ttk.Frame(self,padding=(18,0,18,12)); body.pack(fill="both",expand=True)
        main=ttk.LabelFrame(body,text="Tlocrt",padding=8); main.pack(side="left",fill="both",expand=True)
        bar=ttk.Frame(main); bar.pack(fill="x",pady=(0,8))
        ttk.Label(bar,text="Etaža").pack(side="left")
        box=ttk.Combobox(bar,textvariable=self.level_var,state="readonly",width=18); box.pack(side="left",padx=6); box.bind("<<ComboboxSelected>>",self.select_level)
        ttk.Label(bar,text="| Uređivanje").pack(side="left",padx=(8,0))
        for key,label in TOOLS:
            ttk.Radiobutton(bar,text=label,value=key,variable=self.tool_var,command=lambda k=key:self.editor.set_tool(k)).pack(side="left",padx=(5,0))
        ttk.Label(bar,text="Snap 0.10 m",foreground="#5f6368").pack(side="right")
        self.canvas=tk.Canvas(main,background="white",highlightthickness=1,highlightbackground="#cfd4da"); self.canvas.pack(fill="both",expand=True)
        self.canvas.bind("<Configure>",lambda _e:self.redraw()); self.canvas.bind("<Button-1>",self.editor.click); self.canvas.bind("<ButtonPress-1>",self.editor.begin_drag); self.canvas.bind("<B1-Motion>",self.editor.drag); self.canvas.bind("<ButtonRelease-1>",self.editor.end_drag)
        side=ttk.Frame(body,width=360); side.pack(side="left",fill="y",padx=(14,0)); side.pack_propagate(False)
        modes=ttk.LabelFrame(side,text="Režim rada",padding=10); modes.pack(fill="x")
        for label,desc in MODES:
            ttk.Button(modes,text=label,command=lambda m=label:self.select_mode(m)).pack(fill="x",pady=2)
        self.mode_desc=ttk.Label(side,text=dict(MODES)["Projektovanje"],wraplength=325); self.mode_desc.pack(anchor="w",pady=(8,0))
        project=ttk.LabelFrame(side,text="Trenutni objekat",padding=10); project.pack(fill="x",pady=(14,0))
        self.summary=tk.Text(project,height=8,width=40,state="disabled",wrap="word"); self.summary.pack(fill="x")
        selected=ttk.LabelFrame(side,text="Odabrani zid",padding=10); selected.pack(fill="x",pady=(14,0)); selected.columnconfigure(1,weight=1)
        ttk.Label(selected,text="Dužina (m)").grid(row=0,column=0,sticky="w"); ttk.Entry(selected,textvariable=self.sel_length).grid(row=0,column=1,sticky="ew",padx=(8,0))
        ttk.Label(selected,text="Debljina (m)").grid(row=1,column=0,sticky="w",pady=(5,0)); ttk.Entry(selected,textvariable=self.sel_thickness).grid(row=1,column=1,sticky="ew",padx=(8,0),pady=(5,0))
        ttk.Button(selected,text="Primijeni dimenzije",command=self.apply_wall_dimensions).grid(row=2,column=0,columnspan=2,sticky="ew",pady=(8,0))
        tools=ttk.LabelFrame(side,text="LAT-CES alati",padding=10); tools.pack(fill="x",pady=(14,0))
        ttk.Button(tools,text="Provjeri model",command=self.validate_model).pack(fill="x")
        ttk.Button(tools,text="Scientific Analysis",command=self.analysis).pack(fill="x",pady=5)
        ttk.Button(tools,text="Ponovi početni unos",command=self.open_setup).pack(fill="x")
        ttk.Label(side,text="Tlocrt je ulazni model. Svi kasniji sistemi rade nad istim BuildingModelom.",wraplength=325,foreground="#5f6368").pack(anchor="w",pady=(14,0))
        ttk.Label(self,textvariable=self.status,relief="sunken",anchor="w").pack(fill="x")
        self.refresh_levels(); self.update_summary()

    def open_setup(self) -> None:
        if any(isinstance(w, SetupWizardV3) for w in self.winfo_children()):
            return
        SetupWizardV3(self, self.workflow)

    def on_setup_complete(self) -> None:
        self.refresh_levels(); self.level_var.set(self.level.name); self.status.set("Objekat je formiran — etaže + krov + 3D"); self.update_summary(); self.draw_3d()

    def select_mode(self, mode: str) -> None:
        self.mode.set(mode); self.mode_desc.configure(text=dict(MODES)[mode]); self.status.set(f"Režim: {mode}")

    def refresh_levels(self) -> None:
        names=[lvl.name for lvl in self.workflow.model.levels.values()] or ["Prizemlje"]
        def walk(widget):
            yield widget
            for child in widget.winfo_children(): yield from walk(child)
        combos=[w for w in walk(self) if isinstance(w,ttk.Combobox)]
        if combos: combos[0]["values"]=names
        if self.workflow.active_level_id and self.workflow.active_level_id in self.workflow.model.levels:
            self.level_var.set(self.workflow.active_level.name)

    def select_level(self,_event=None) -> None:
        value=self.level_var.get()
        for lvl in self.workflow.model.levels.values():
            if lvl.name==value: self.workflow.set_active_level(lvl.level_id); break
        self.redraw(); self.update_summary()

    def refresh(self) -> None:
        self.update_selection(); self.update_summary(); self.redraw()

    def update_selection(self) -> None:
        wall=self.plan.walls.get(self.editor.selected) if self.editor.selected else None
        if wall:
            self.sel_length.set(f"{wall.segment.length:.2f}"); self.sel_thickness.set(f"{wall.thickness:.3f}")
        else:
            self.sel_length.set(""); self.sel_thickness.set("0.20")

    def apply_wall_dimensions(self) -> None:
        wall=self.plan.walls.get(self.editor.selected) if self.editor.selected else None
        if wall is None:
            messagebox.showwarning("LAT-CES","Prvo odaberi zid.",parent=self); return
        try:
            length=float(self.sel_length.get().replace(",",".")); thick=float(self.sel_thickness.get().replace(",","."))
        except ValueError:
            messagebox.showwarning("LAT-CES","Dimenzije moraju biti brojevi.",parent=self); return
        if length<=0 or thick<=0:
            messagebox.showwarning("LAT-CES","Dimenzije moraju biti > 0.",parent=self); return
        old=wall.segment; dx,dy=old.end.x-old.start.x,old.end.y-old.start.y; old_len=old.length
        wall.segment=Segment2D(old.start,Point2D(old.start.x+dx/old_len*length,old.start.y+dy/old_len*length)); wall.thickness=thick; self.refresh(); self.status.set(f"Zid: {length:.2f} m × {thick:.3f} m")

    def plan_bounds(self):
        points=[p for wall in self.plan.walls.values() for p in (wall.segment.start,wall.segment.end)]
        if not points: return 0,10,0,10
        xs=[p.x for p in points]; ys=[p.y for p in points]; return min(xs)-1,max(xs)+1,min(ys)-1,max(ys)+1

    def canvas_to_model(self,x,y):
        xmin,xmax,ymin,ymax=self.plan_bounds(); width=max(self.canvas.winfo_width(),400); height=max(self.canvas.winfo_height(),300); margin=70; scale=min((width-2*margin)/max(xmax-xmin,1),(height-2*margin)/max(ymax-ymin,1)); ox=(width-(xmax-xmin)*scale)/2-xmin*scale; oy=(height+(ymax-ymin)*scale)/2+ymin*scale; return Point2D((x-ox)/scale,(oy-y)/scale)

    def model_to_canvas(self,p):
        xmin,xmax,ymin,ymax=self.plan_bounds(); width=max(self.canvas.winfo_width(),400); height=max(self.canvas.winfo_height(),300); margin=70; scale=min((width-2*margin)/max(xmax-xmin,1),(height-2*margin)/max(ymax-ymin,1)); ox=(width-(xmax-xmin)*scale)/2-xmin*scale; oy=(height+(ymax-ymin)*scale)/2+ymin*scale; return ox+p.x*scale,oy-p.y*scale

    def draw_floor(self):
        self.canvas.delete("all")
        for wall in self.plan.walls.values():
            x1,y1=self.model_to_canvas(wall.segment.start); x2,y2=self.model_to_canvas(wall.segment.end); selected=wall.wall_id==self.editor.selected
            self.canvas.create_line(x1,y1,x2,y2,width=10 if selected else 7,fill="#2563eb" if selected else "#111827")
            self.canvas.create_text((x1+x2)/2,(y1+y2)/2-10,text=f"{wall.segment.length:.2f} m",fill="#374151",font=("Segoe UI",9,"bold"))
            for opening in wall.openings:
                t1=opening.offset/wall.segment.length; t2=(opening.offset+opening.width)/wall.segment.length; ox1=x1+(x2-x1)*t1; oy1=y1+(y2-y1)*t1; ox2=x1+(x2-x1)*t2; oy2=y1+(y2-y1)*t2; self.canvas.create_line(ox1,oy1,ox2,oy2,width=10,fill="white"); self.canvas.create_text((ox1+ox2)/2,(oy1+oy2)/2+12,text=f"{opening.kind} {opening.width:.2f} m",fill="#4b5563",font=("Segoe UI",8))
        self.canvas.create_text(20,20,text=f"{self.level.name} — tlocrt",anchor="nw",fill="#374151",font=("Segoe UI",12,"bold"))

    def draw_3d(self):
        self.canvas.delete("all"); geometries=build_geometry(self.workflow.model); width=max(self.canvas.winfo_width(),400); height=max(self.canvas.winfo_height(),300); scale=22.0
        for idx,geometry in enumerate(geometries):
            z0=sum(g.height for g in geometries[:idx])
            for wall in geometry.walls:
                def project(x,y,z): return width*0.25+x*scale+y*0.45*scale,height*0.72-z*scale-y*0.22*scale
                a0=project(wall.x1,wall.y1,z0); b0=project(wall.x2,wall.y2,z0); a1=project(wall.x1,wall.y1,z0+wall.height); b1=project(wall.x2,wall.y2,z0+wall.height); self.canvas.create_line(*a0,*b0,fill="#374151",width=3); self.canvas.create_line(*a1,*b1,fill="#6b7280",width=3); self.canvas.create_line(*a0,*a1,fill="#9ca3af"); self.canvas.create_line(*b0,*b1,fill="#9ca3af")
        self.canvas.create_text(20,20,text="3D Building Model — sve etaže",anchor="nw",fill="#374151",font=("Segoe UI",12,"bold"))

    def redraw(self):
        self.draw_3d() if getattr(self.workflow,"current_step",1)>=4 and self.workflow.project_spec else self.draw_floor()

    def update_summary(self):
        data=self.workflow.summary(); levels=[f"{i+1}. {lvl.name}: {lvl.height:.2f} m" for i,lvl in enumerate(self.workflow.model.levels.values())]; text=f"Objekat: {data['model']}\nEtaže: {data['levels']}\nAktivna: {data['active_level']}\nKorak: {data['step']}\n\n"+"\n".join(levels); self.summary.configure(state="normal"); self.summary.delete("1.0","end"); self.summary.insert("1.0",text); self.summary.configure(state="disabled")

    def validate_model(self):
        findings=self.workflow.validate(); messagebox.showwarning("LAT-CES — Provjera","\n".join(findings),parent=self) if findings else messagebox.showinfo("LAT-CES — Provjera","Building Model je geometrijski validan.",parent=self)

    def save_project(self):
        target=filedialog.asksaveasfilename(title="Sačuvaj Building Model",defaultextension=".json",filetypes=(("LAT-CES JSON","*.json"),("All files","*.*")),initialfile="building_model.json")
        if not target: return
        try: save_workflow(self.workflow,target); self.status.set(f"Sačuvano: {target}")
        except Exception as exc: messagebox.showwarning("LAT-CES",f"Nije moguće sačuvati: {exc}",parent=self)

    def load_project(self):
        source=filedialog.askopenfilename(title="Učitaj Building Model",filetypes=(("LAT-CES JSON","*.json"),("All files","*.*")))
        if not source: return
        try: self.workflow=load_workflow(source); self.refresh_levels(); self.update_summary(); self.redraw(); self.status.set(f"Učitano: {source}")
        except Exception as exc: messagebox.showwarning("LAT-CES",f"Nije moguće učitati: {exc}",parent=self)

    def analysis(self):
        messagebox.showinfo("LAT-CES","Scientific Analysis ostaje dostupan kao režim rada nad BuildingModelom.",parent=self)


if __name__ == "__main__":
    LATCESBuildingApp().mainloop()
