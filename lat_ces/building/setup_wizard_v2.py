"""Clean mandatory Building Model setup wizard."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .model import BuildingModel
from .project_spec import BuildingProjectSpec, LevelProjectSpec, RoomSpec, WallConstructionSpec
from .workflow import BuildingWorkflow


class SetupWizardV2(tk.Toplevel):
    def __init__(self, app: tk.Tk, workflow: BuildingWorkflow) -> None:
        super().__init__(app)
        self.app, self.workflow = app, workflow
        self.title("LAT-CES — Novi objekat")
        self.geometry("820x760")
        self.minsize(760, 680)
        self.transient(app)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.phase = "base"
        self.level_index = 0
        self.level_specs: list[LevelProjectSpec] = []
        self.name = tk.StringVar(value="Novi objekat")
        self.floor_count = tk.IntVar(value=1)
        self.vars = {key: tk.StringVar(value=value) for key, value in {
            "length": "", "width": "", "height": "2.80", "block": "", "block_l": "", "block_w": "", "block_h": "",
            "wall": "0.25", "insulation": "EPS / stiropor", "insulation_t": "0.10", "facade": "", "granulation": "", "render": "0.005",
            "roof_h": "0", "roof": "Ravni",
        }.items()}
        self.room_vars: list[list[tk.StringVar]] = []
        self._render_base()

    @staticmethod
    def _num(value: str, label: str, positive: bool = True) -> float:
        try: result = float(value.replace(",", "."))
        except ValueError as exc: raise ValueError(f"{label}: unesite broj") from exc
        if positive and result <= 0: raise ValueError(f"{label}: mora biti > 0")
        return result

    def _shell(self, title: str, back: bool = False, next_text: str = "Nastavi →") -> tuple[ttk.Frame, ttk.Frame]:
        for child in self.winfo_children(): child.destroy()
        head = ttk.Frame(self, padding=18); head.pack(fill="x")
        ttk.Label(head, text=title, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        body = ttk.Frame(self, padding=(18, 0, 18, 8)); body.pack(fill="both", expand=True)
        foot = ttk.Frame(self, padding=18); foot.pack(fill="x")
        ttk.Button(foot, text="Odustani", command=self.cancel).pack(side="left")
        if back: ttk.Button(foot, text="← Nazad", command=self.back).pack(side="left", padx=8)
        ttk.Button(foot, text=next_text, command=self.next).pack(side="right")
        return head, body

    def _entry(self, frame: ttk.Frame, row: int, label: str, var: tk.StringVar) -> None:
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=var).grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=3)

    def _ensure_rooms(self, spec: LevelProjectSpec | None) -> None:
        self.room_vars=[]
        for room in (spec.rooms if spec else []):
            self.room_vars.append([tk.StringVar(value=room.name), tk.StringVar(value=f"{room.length_m:g}"), tk.StringVar(value=f"{room.width_m:g}")])
        while len(self.room_vars)<10: self.room_vars.append([tk.StringVar(),tk.StringVar(),tk.StringVar()])

    def _load_spec(self, spec: LevelProjectSpec | None) -> None:
        spec = spec or LevelProjectSpec(name=f"Etaža {self.level_index+1}")
        c=spec.construction
        data={"length":spec.length_m,"width":spec.width_m,"height":spec.height_m,"block":c.block_brand,"block_l":c.block_length_m,"block_w":c.block_width_m,"block_h":c.block_height_m,"wall":c.wall_thickness_m,"insulation":c.insulation_type or "EPS / stiropor","insulation_t":c.insulation_thickness_m,"facade":c.facade_brand,"granulation":c.facade_granulation_mm,"render":c.render_thickness_m}
        for key,val in data.items(): self.vars[key].set(f"{val:g}" if isinstance(val,(int,float)) and val else (str(val) if val is not None else ""))
        if not self.vars["wall"].get(): self.vars["wall"].set("0.25")
        if not self.vars["insulation_t"].get(): self.vars["insulation_t"].set("0.10")
        if not self.vars["render"].get(): self.vars["render"].set("0.005")
        self._ensure_rooms(spec)

    def _render_base(self) -> None:
        self.phase="base"; self.level_index=0
        head, body=self._shell("1. Osnovni tlocrt i građevinski sastav", next_text="Potvrdi i odredi spratnost →")
        ttk.Label(head,text="Početni tlocrt je prazan. Ovdje se zadaju gabarit, zid, izolacija, fasada i program prostorija.",foreground="#5f6368").pack(anchor="w",pady=(4,0))
        self._load_spec(None)
        g=ttk.LabelFrame(body,text="Gabarit",padding=12); g.pack(fill="x",pady=(0,8)); g.columnconfigure(1,weight=1)
        self._entry(g,0,"Naziv projekta",self.name); self._entry(g,1,"Dužina objekta (m)",self.vars["length"]); self._entry(g,2,"Širina objekta (m)",self.vars["width"]); self._entry(g,3,"Visina etaže (m)",self.vars["height"])
        c=ttk.LabelFrame(body,text="Zidani sistem / izolacija / fasada",padding=12); c.pack(fill="x",pady=(0,8)); c.columnconfigure(1,weight=1)
        fields=[("Marka bloka","block"),("Dužina bloka (m)","block_l"),("Širina bloka (m)","block_w"),("Visina bloka (m)","block_h"),("Debljina zida (m)","wall"),("Izolacija","insulation"),("Debljina izolacije (m)","insulation_t"),("Marka fasade","facade"),("Granulacija fasade (mm)","granulation"),("Debljina završne žbuke (m)","render")]
        for i,(label,key) in enumerate(fields): self._entry(c,i,label,self.vars[key])
        r=ttk.LabelFrame(body,text="Program prostorija / raspored",padding=12); r.pack(fill="both",expand=True)
        for col,text in enumerate(("Prostorija","Dužina (m)","Širina (m)")): ttk.Label(r,text=text).grid(row=0,column=col,sticky="w",padx=(0 if col==0 else 8,0))
        for row,rv in enumerate(self.room_vars,start=1):
            for col,var in enumerate(rv): ttk.Entry(r,textvariable=var).grid(row=row,column=col,sticky="ew" if col==0 else "w",padx=(0 if col==0 else 8),pady=2)
        r.columnconfigure(0,weight=1)
        ttk.Label(r,text="Primjer: kuhinja, spavaća, WC, hodnik. Hodnik se može postaviti unutar osnovnog gabarita.",foreground="#5f6368").grid(row=11,column=0,columnspan=3,sticky="w",pady=(8,0))

    def _collect(self)->LevelProjectSpec:
        rooms=[]
        for nv,lv,wv in self.room_vars:
            if not nv.get().strip(): continue
            rooms.append(RoomSpec(nv.get().strip(),self._num(lv.get(),f"Dužina {nv.get().strip()}"),self._num(wv.get(),f"Širina {nv.get().strip()}")))
        c=WallConstructionSpec(block_brand=self.vars["block"].get().strip(),block_length_m=self._num(self.vars["block_l"].get(),"Dužina bloka") if self.vars["block_l"].get().strip() else 0.0,block_width_m=self._num(self.vars["block_w"].get(),"Širina bloka") if self.vars["block_w"].get().strip() else 0.0,block_height_m=self._num(self.vars["block_h"].get(),"Visina bloka") if self.vars["block_h"].get().strip() else 0.0,wall_thickness_m=self._num(self.vars["wall"].get(),"Debljina zida"),insulation_type=self.vars["insulation"].get().strip(),insulation_thickness_m=self._num(self.vars["insulation_t"].get(),"Debljina izolacije"),facade_brand=self.vars["facade"].get().strip(),facade_granulation_mm=self._num(self.vars["granulation"].get(),"Granulacija",False) if self.vars["granulation"].get().strip() else 0.0,render_thickness_m=self._num(self.vars["render"].get(),"Debljina završne žbuke"))
        return LevelProjectSpec(f"Etaža {self.level_index+1}",self._num(self.vars["height"].get(),"Visina etaže"),self._num(self.vars["length"].get(),"Dužina"),self._num(self.vars["width"].get(),"Širina"),c,rooms,True)

    def _render_floor_count(self):
        self.phase="count"; head,body=self._shell("2. Spratnost",back=True,next_text="Potvrdi spratnost →")
        ttk.Label(head,text="Bez ovog odgovora krov i 3D ne mogu biti otključani.",foreground="#5f6368").pack(anchor="w",pady=(4,0))
        box=ttk.LabelFrame(body,text="Broj etaža",padding=25); box.pack(fill="x",pady=60); ttk.Label(box,text="Broj etaža (1–50)",font=("Segoe UI",13,"bold")).pack(anchor="w"); ttk.Spinbox(box,from_=1,to=50,textvariable=self.floor_count,width=10).pack(anchor="w",pady=15)

    def _render_level(self,index:int):
        self.phase="levels"; self.level_index=index; self._load_spec(self.level_specs[index]); head,body=self._shell(f"1. Podaci za {self.level_specs[index].name}",back=True,next_text=("Zaključi etažu →" if index+1==len(self.level_specs) else "Zaključi etažu i pređi na sljedeću →"))
        ttk.Label(head,text="Ova etaža ima vlastiti tlocrt. Ne pretpostavljamo da je isti raspored kao na prethodnoj etaži.",foreground="#5f6368").pack(anchor="w",pady=(4,0))
        g=ttk.LabelFrame(body,text="Dimenzije etaže",padding=12); g.pack(fill="x",pady=(0,8)); g.columnconfigure(1,weight=1); self._entry(g,0,"Dužina (m)",self.vars["length"]); self._entry(g,1,"Širina (m)",self.vars["width"]); self._entry(g,2,"Visina (m)",self.vars["height"])
        c=ttk.LabelFrame(body,text="Konstrukcija zida / izolacija / fasada",padding=12); c.pack(fill="x",pady=(0,8)); c.columnconfigure(1,weight=1)
        for i,(label,key) in enumerate([("Marka bloka","block"),("Dužina bloka (m)","block_l"),("Širina bloka (m)","block_w"),("Visina bloka (m)","block_h"),("Debljina zida (m)","wall"),("Izolacija","insulation"),("Debljina izolacije (m)","insulation_t"),("Marka fasade","facade"),("Granulacija fasade (mm)","granulation"),("Debljina završne žbuke (m)","render")]): self._entry(c,i,label,self.vars[key])
        r=ttk.LabelFrame(body,text="Program prostorija",padding=12); r.pack(fill="both",expand=True)
        for col,text in enumerate(("Prostorija","Dužina (m)","Širina (m)")): ttk.Label(r,text=text).grid(row=0,column=col,sticky="w")
        for row,rv in enumerate(self.room_vars,start=1):
            for col,var in enumerate(rv): ttk.Entry(r,textvariable=var).grid(row=row,column=col,sticky="ew" if col==0 else "w",padx=(0 if col==0 else 8),pady=2)
        r.columnconfigure(0,weight=1)

    def _render_roof(self):
        self.phase="roof"; head,body=self._shell("3. Krov",back=True,next_text="Zaključi i generiši 3D →"); ttk.Label(head,text="Sve etaže su zaključane. Sada zadajemo oblik i visinu krova.",foreground="#5f6368").pack(anchor="w",pady=(4,0))
        box=ttk.LabelFrame(body,text="Krov",padding=24); box.pack(fill="x",pady=50); ttk.Label(box,text="Oblik krova").pack(anchor="w"); ttk.Combobox(box,textvariable=self.vars["roof"],values=("Ravni","Jednovodni","Dvovodni","Četvorovodni","Mansardni","Drugi"),state="readonly").pack(fill="x",pady=6); ttk.Label(box,text="Visina / uzdignuće krova (m)").pack(anchor="w",pady=(10,0)); ttk.Entry(box,textvariable=self.vars["roof_h"]).pack(fill="x",pady=6)

    def next(self):
        try:
            if self.phase=="base": self.level_specs=[self._collect()]; self._render_floor_count(); return
            if self.phase=="count":
                n=int(self.floor_count.get())
                if n<1 or n>50: raise ValueError("Spratnost mora biti 1–50")
                while len(self.level_specs)<n: self.level_specs.append(LevelProjectSpec(name=f"Etaža {len(self.level_specs)+1}"))
                self.level_specs=self.level_specs[:n]; self._render_level(0); return
            if self.phase=="levels":
                self.level_specs[self.level_index]=self._collect()
                if self.level_index+1<len(self.level_specs): self._render_level(self.level_index+1)
                else: self._render_roof()
                return
            roof_h=self._num(self.vars["roof_h"].get(),"Visina krova",False)
            project=BuildingProjectSpec(name=self.name.get().strip() or "Novi objekat",floor_count=len(self.level_specs),levels=self.level_specs,floor_count_finalized=True,roof_shape=self.vars["roof"].get(),roof_height_m=roof_h)
            wf=BuildingWorkflow(model=BuildingModel(project.name),project_spec=project,current_step=4,roof_shape=project.roof_shape,roof_height_m=roof_h)
            for i,spec in enumerate(project.levels): wf.set_level_spec(i,spec)
            wf.current_step=4
            self.app.workflow=wf; self.app.on_setup_complete(); self.grab_release(); self.destroy()
        except (ValueError,TypeError) as exc: messagebox.showwarning("LAT-CES",str(exc),parent=self)

    def back(self):
        if self.phase=="count": self._render_base()
        elif self.phase=="levels": self._render_floor_count() if self.level_index==0 else self._render_level(self.level_index-1)
        elif self.phase=="roof": self._render_level(len(self.level_specs)-1)

    def cancel(self): self.grab_release(); self.destroy()
