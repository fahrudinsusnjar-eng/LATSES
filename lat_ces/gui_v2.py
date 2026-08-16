"""Clean Building-first LAT-CES desktop UI."""
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
from lat_ces.building.setup_wizard_v2 import SetupWizardV2
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
    wf = BuildingWorkflow(model=model)
    wf.set_floor_plan(make_blank_floor_plan("Prizemlje"))
    return wf


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
    def snap(p: Point2D) -> Point2D:
        return Point2D(round(p.x * 10) / 10, round(p.y * 10) / 10)

    @staticmethod
    def distance(p: Point2D, a: Point2D, b: Point2D) -> float:
        dx, dy = b.x - a.x, b.y - a.y
        d2 = dx * dx + dy * dy
        if d2 == 0: return math.hypot(p.x - a.x, p.y - a.y)
        t = max(0.0, min(1.0, ((p.x-a.x)*dx + (p.y-a.y)*dy) / d2))
        qx, qy = a.x + t*dx, a.y + t*dy
        return math.hypot(p.x-qx, p.y-qy)

    def nearest(self, p: Point2D, tol: float = 0.25) -> Wall | None:
        best = None
        for wall in self.plan.walls.values():
            d = self.distance(p, wall.segment.start, wall.segment.end)
            if d <= tol and (best is None or d < best[0]): best = (d, wall)
        return best[1] if best else None

    def set_tool(self, tool: str) -> None:
        self.tool, self.start, self.drag_last = tool, None, None
        self.app.tool_var.set(tool)
        self.app.status.set(f"Alat: {dict(TOOLS)[tool]}")
        self.app.redraw()

    def click(self, event: tk.Event) -> None:
        p = self.snap(self.app.canvas_to_model(event.x, event.y))
        if self.tool == "draw":
            if self.start is None:
                self.start = p; self.app.status.set(f"Početak: {p.x:.1f}, {p.y:.1f} m — klikni kraj"); return
            if math.hypot(p.x-self.start.x, p.y-self.start.y) < 0.1: return
            wall = Wall(f"Zid {self.plan.wall_count+1}", Segment2D(self.start, p), thickness=0.20)
            self.plan.add_wall(wall); self.selected = wall.wall_id; self.start = None; self.app.refresh(); return
        wall = self.nearest(p)
        if wall is None:
            self.selected = None; self.app.refresh(); return
        self.selected = wall.wall_id
        if self.tool == "delete":
            del self.plan.walls[wall.wall_id]; self.selected = None; self.app.refresh(); return
        if self.tool in {"door", "window"}:
            self.add_opening(wall, p, self.tool); return
        self.app.update_selection()

    def begin_drag(self, event: tk.Event) -> None:
        if self.tool != "move": return
        p = self.snap(self.app.canvas_to_model(event.x, event.y)); wall = self.nearest(p)
        if wall: self.selected, self.drag_last = wall.wall_id, p

    def drag(self, event: tk.Event) -> None:
        if self.tool != "move" or not self.selected or self.drag_last is None: return
        wall = self.plan.walls.get(self.selected)
        if wall is None: return
        p = self.snap(self.app.canvas_to_model(event.x, event.y)); dx, dy = p.x-self.drag_last.x, p.y-self.drag_last.y
        wall.segment = Segment2D(Point2D(wall.segment.start.x+dx, wall.segment.start.y+dy), Point2D(wall.segment.end.x+dx, wall.segment.end.y+dy))
        self.drag_last = p; self.app.refresh()

    def end_drag(self, _event: tk.Event) -> None: self.drag_last = None

    def add_opening(self, wall: Wall, p: Point2D, kind: str) -> None:
        dx, dy = wall.segment.end.x-wall.segment.start.x, wall.segment.end.y-wall.segment.start.y
        length = wall.segment.length
        t = max(0.0, min(1.0, ((p.x-wall.segment.start.x)*dx+(p.y-wall.segment.start.y)*dy)/(length*length)))
        offset = t*length; default = 0.90 if kind == "door" else 1.20
        width = simpledialog.askfloat("Otvor", f"Širina {kind} (m)", initialvalue=default, minvalue=0.1, parent=self.app)
        if width is None: return
        offset = min(max(0.0, offset-width/2), max(0.0, length-width))
        try: wall.add_opening(Opening(kind, offset, width))
        except ValueError as exc: messagebox.showwarning("LAT-CES", str(exc), parent=self.app); return
        self.app.refresh()


class LATCESBuildingApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1360x850"); self.minsize(1150,740)
        self.workflow = blank_workflow()
        self.mode = tk.StringVar(value="Projektovanje")
        self.tool_var = tk.StringVar(value="select")
        self.level_var = tk.StringVar(value="Prizemlje")
        self.status = tk.StringVar(value="Prazan projekat — započnite unos objekta")
        self.sel_length = tk.StringVar(value=""); self.sel_thickness = tk.StringVar(value="0.20")
        self.editor = FloorEditor(self)
        self._ui()
        self.redraw()
        self.after(150, self.open_setup)

    @property
    def plan(self): return self.workflow.floor_plan
    @property
    def level(self): return self.workflow.active_level

    def _ui(self) -> None:
        head=ttk.Frame(self,padding=(18,12)); head.pack(fill="x")
        ttk.Label(head,text="LAT-CES",font=("Segoe UI",21,"bold")).pack(side="left")
        ttk.Label(head,text="Building Model",font=("Segoe UI",11)).pack(side="left",padx=(14,0),pady=(5,0))
        ttk.Button(head,text="Postavi projekat",command=self.open_setup).pack(side="right")
        ttk.Button(head,text="Učitaj",command=self.load_project).pack(side="right",padx=6)
        ttk.Button(head,text="Sačuvaj",command=self.save_project).pack(side="right")

        body=ttk.Frame(self,padding=(18,0,18,12)); body.pack(fill="both",expand=True)
        main=ttk.LabelFrame(body,text="Tlocrt",padding=8); main.pack(side="left",fill="both",expand=True)
        bar=ttk.Frame(main); bar.pack(fill="x",pady=(0,8))
        ttk.Label(bar,text="Etaža").pack(side="left")
        box=ttk.Combobox(bar,textvariable=self.level_var,state="readonly",width=18); box.pack(side="left",padx=6); box.bind("<<ComboboxSelected>>",self.select_level)
        ttk.Label(bar,text="| Uređivanje").pack(side="left",padx=(8,0))
        for key,label in TOOLS: ttk.Radiobutton(bar,text=label,value=key,variable=self.tool_var,command=lambda k=key:self.editor.set_tool(k)).pack(side="left",padx=(5,0))
        ttk.Label(bar,text="Snap 0.10 m",foreground="#5f6368").pack(side="right")
        self.canvas=tk.Canvas(main,background="white",highlightthickness=1,highlightbackground="#cfd4da"); self.canvas.pack(fill="both",expand=True)
        self.canvas.bind("<Configure>",lambda _e:self.redraw()); self.canvas.bind("<Button-1>",self.editor.click); self.canvas.bind("<ButtonPress-1>",self.editor.begin_drag); self.canvas.bind("<B1-Motion>",self.editor.drag); self.canvas.bind("<ButtonRelease-1>",self.editor.end_drag)

        side=ttk.Frame(body,width=360); side.pack(side="left",fill="y",padx=(14,0)); side.pack_propagate(False)
        modes=ttk.LabelFrame(side,text="Režim rada",padding=10); modes.pack(fill="x")
        for label,desc in MODES: ttk.Button(modes,text=label,command=lambda m=label:self.select_mode(m)).pack(fill="x",pady=2)
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
        if any(isinstance(w,SetupWizardV2) for w in self.winfo_children()): return
        SetupWizardV2(self,self.workflow)

    def on_setup_complete(self) -> None:
        self.refresh_levels(); self.level_var.set(self.level.name); self.status.set("Osnovni model završen — 3D je izveden iz svih etaža"); self.update_summary(); self.draw_3d()

    def select_mode(self, mode:str) -> None:
        self.mode.set(mode); self.mode_desc.configure(text=dict(MODES)[mode]); self.status.set(f"Režim: {mode}")

    def refresh_levels(self) -> None:
        names=[lvl.name for lvl in self.workflow.model.levels.values()]
        if not names: names=["Prizemlje"]
        widgets=[w for w in self.winfo_children()]
        for frame in widgets: pass
        # find combobox through recursive widget lookup
        def walk(w):
            yield w
            for child in w.winfo_children(): yield from walk(child)
        combos=[w for w in walk(self) if isinstance(w,ttk.Combobox)]
        if combos: combos[0]["values"]=names
        if self.workflow.active_level_id and self.workflow.active_level_id in self.workflow.model.levels: self.level_var.set(self.workflow.active_level.name)

    def select_level(self,_event=None) -> None:
        value=self.level_var.get()
        for lvl in self.workflow.model.levels.values():
            if lvl.name==value: self.workflow.set_active_level(lvl.level_id); break
        self.redraw(); self.update_summary()

    def refresh(self) -> None: self.update_selection(); self.update_summary(); self.redraw()

    def update_selection(self) -> None:
        wall=self.plan.walls.get(self.editor.selected) if self.editor.selected else None
        if wall:
            self.sel_length.set(f"{wall.segment.length:.2f}"); self.sel_thickness.set(f"{wall.thickness:.3f}")
        else: self.sel_length.set(""); self.sel_thickness.set("0.20")

    def apply_wall_dimensions(self) -> None:
        wall=self.plan.walls.get(self.editor.selected) if self.editor.selected else None
        if wall is None: messagebox.showwarning("LAT-CES","Prvo odaberi zid.",parent=self); return
        try: length=float(self.sel_length.get().replace(",",".")); thick=float(self.sel_thickness.get().replace(",","."))
        except ValueError: messagebox.showwarning("LAT-CES","Dimenzije moraju biti brojevi.",parent=self); return
        if length<=0 or thick<=0: messagebox.showwarning("LAT-CES","Dimenzije moraju biti > 0.",parent=self); return
        old=wall.segment; dx,dy=old.end.x-old.start.x,old.end.y-old.start.y; old_len=old.length
        wall.segment=Segment2D(old.start,Point2D(old.start.x+dx/old_len*length,old.start.y+dy/old_len*length)); wall.thickness=thick; self.refresh(); self.status.set(f"Zid: {length:.2f} m × {thick:.3f} m")

    def canvas_to_model(self,x:float,y:float)->Point2D:
        plan=self.plan; max_x=max((w.segment.start.x for w in plan.walls.values()),default=10); max_x=max(max_x,max((w.segment.end.x for w in plan.walls.values()),default=10)); max_y=max((w.segment.start.y for w in plan.walls.values()),default=10); max_y=max(max_y,max((w.segment.end.y for w in plan.walls.values()),default=10)); max_x=max(max_x,10); max_y=max(max_y,10)
        width=max(self.canvas.winfo_width(),400); height=max(self.canvas.winfo_height(),300); margin=60; scale=min((width-2*margin)/max_x,(height-2*margin)/max_y)
        ox=(width-max_x*scale)/2; oy=(height-max_y*scale)/2
        return Point2D((x-ox)/scale,(y-oy)/scale)

    def model_to_canvas(self,p:Point2D):
        plan=self.plan; max_x=max((max(w.segment.start.x,w.segment.end.x) for w in plan.walls.values()),default=10); max_y=max((max(w.segment.start.y,w.segment.end.y) for w in plan.walls.values()),default=10); max_x=max(max_x,10); max_y=max(max_y,10); width=max(self.canvas.winfo_width(),400); height=max(self.canvas.winfo_height(),300); margin=60; scale=min((width-2*margin)/max_x,(height-2*margin)/max_y); ox=(width-max_x*scale)/2; oy=(height-max_y*scale)/2; return ox+p.x*scale,oy+p.y*scale

    def redraw(self) -> None:
        if not hasattr(self,"canvas"): return
        if self.mode.get()=="Geometrija" and self.workflow.current_step==4: self.draw_3d(); return
        self.canvas.delete("all")
        for wall in self.plan.walls.values():
            a=self.model_to_canvas(wall.segment.start); b=self.model_to_canvas(wall.segment.end); selected=wall.wall_id==self.editor.selected
            self.canvas.create_line(*a,*b,width=10 if selected else 6,fill="#111827" if not selected else "#2563eb")
            mid=((a[0]+b[0])/2,(a[1]+b[1])/2); self.canvas.create_text(mid[0],mid[1]-12,text=f"{wall.segment.length:.2f} m",fill="#374151")
            for opening in wall.openings:
                t=(opening.offset+opening.width/2)/wall.segment.length; ox=a[0]+t*(b[0]-a[0]); oy=a[1]+t*(b[1]-a[1]); self.canvas.create_text(ox,oy+13,text=f"{opening.kind} {opening.width:.2f} m",fill="#7c3aed")
        if not self.plan.walls: self.canvas.create_text(self.canvas.winfo_width()/2,self.canvas.winfo_height()/2,text="PRAZAN TLOCRT\nPokrenite 'Postavi projekat' za unos osnovnih mjera",font=("Segoe UI",16),fill="#6b7280",justify="center")
        self.canvas.create_text(18,18,text=f"{self.level.name}  |  gabarit iz projektnih podataka",anchor="nw",fill="#6b7280")

    def draw_3d(self) -> None:
        self.canvas.delete("all")
        geoms=build_geometry(self.workflow.model)
        if not geoms:
            self.redraw(); return
        sx,sy,sz=18,-9,16; ox,oy=160,520
        for gi,geom in enumerate(geoms):
            z0=sum(g.height for g in geoms[:gi])
            for wall in geom.walls:
                for z in (z0,z0+wall.height):
                    x1=ox+(wall.x1-wall.y1)*sx; y1=oy+(wall.x1+wall.y1)*sy-z*sz; x2=ox+(wall.x2-wall.y2)*sx; y2=oy+(wall.x2+wall.y2)*sy-z*sz; self.canvas.create_line(x1,y1,x2,y2,fill="#374151",width=4)
        self.canvas.create_text(20,20,text=f"3D Building Model — {len(geoms)} etaža",anchor="nw",font=("Segoe UI",13,"bold"),fill="#111827")

    def update_summary(self) -> None:
        if not hasattr(self,"summary"): return
        self.summary.configure(state="normal"); self.summary.delete("1.0","end")
        p=self.workflow.project_spec
        lines=[f"Objekat: {self.workflow.model.name}",f"Etaže: {len(self.workflow.model.levels)}",f"Aktivna: {self.workflow.active_level.name}"]
        if p:
            lines.append(f"Krov: {p.roof_shape}")
            for spec in p.levels: lines.append(f"{spec.name}: {spec.length_m:g} × {spec.width_m:g} m | h={spec.height_m:g} m | sobe={len(spec.rooms)}")
        self.summary.insert("1.0","\n".join(lines)); self.summary.configure(state="disabled")

    def validate_model(self) -> None:
        findings=self.workflow.validate(); messagebox.showinfo("LAT-CES", "Model je validan." if not findings else "\n".join(findings), parent=self)

    def save_project(self) -> None:
        path=filedialog.asksaveasfilename(title="Sačuvaj LAT-CES projekat",defaultextension=".json",filetypes=(("LAT-CES projekat","*.json"),))
        if path: save_workflow(self.workflow,path); self.status.set(f"Sačuvano: {path}")

    def load_project(self) -> None:
        path=filedialog.askopenfilename(title="Učitaj LAT-CES projekat",filetypes=(("LAT-CES projekat","*.json"),))
        if not path: return
        try: self.workflow=load_workflow(path); self.refresh_levels(); self.redraw(); self.update_summary(); self.status.set(f"Učitano: {path}")
        except Exception as exc: messagebox.showerror("LAT-CES",str(exc),parent=self)

    def analysis(self) -> None:
        dialog=tk.Toplevel(self); dialog.title("LAT-CES — Scientific Analysis"); dialog.geometry("780x560"); dialog.transient(self)
        path=tk.StringVar(); output=tk.StringVar(); fmt=tk.StringVar(value="json")
        frame=ttk.Frame(dialog,padding=14); frame.pack(fill="x"); frame.columnconfigure(1,weight=1)
        ttk.Label(frame,text="JSON konfiguracija").grid(row=0,column=0,sticky="w"); ttk.Entry(frame,textvariable=path).grid(row=0,column=1,sticky="ew",padx=8); ttk.Button(frame,text="Browse",command=lambda:path.set(filedialog.askopenfilename(filetypes=(("JSON","*.json"),)))).grid(row=0,column=2)
        ttk.Label(frame,text="Format").grid(row=1,column=0,sticky="w",pady=6); ttk.Combobox(frame,textvariable=fmt,values=("json","md"),state="readonly",width=8).grid(row=1,column=1,sticky="w",padx=8)
        out=tk.Text(dialog,wrap="word",font=("Consolas",10)); out.pack(fill="both",expand=True,padx=14,pady=8)
        def run():
            try:
                cfg=load_config(Path(path.get())); report,exporter=analyze_config(cfg,project_default="LAT-CES Desktop",plenum_default="PLENUM-GUI-01",equation_default="Custom equation"); target=Path(output.get() or Path(path.get()).with_name(f"latces_report.{fmt.get()}")); export_report(exporter,target,fmt.get()); text=exporter.to_json() if fmt.get()=="json" else exporter.to_markdown(); out.delete("1.0","end"); out.insert("1.0",f"Status: [{report.status.value}]\nReport: {target}\n\n{text}")
            except Exception as exc: messagebox.showerror("LAT-CES",str(exc),parent=dialog)
        ttk.Button(dialog,text="Run Analysis",command=run).pack(pady=(0,12))

    def on_close(self) -> None: self.destroy()


def main() -> None:
    app=LATCESBuildingApp(); app.protocol("WM_DELETE_WINDOW",app.on_close); app.mainloop()


if __name__ == "__main__": main()
