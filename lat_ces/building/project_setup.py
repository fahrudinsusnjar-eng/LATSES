"""Modal project-setup wizard for the Building-first LAT-CES UI."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .model import BuildingModel
from .project_spec import BuildingProjectSpec, LevelProjectSpec, RoomSpec, WallConstructionSpec
from .workflow import BuildingWorkflow


class ProjectSetupWizard(tk.Toplevel):
    """Mandatory setup: level data -> floor count -> each level -> roof -> 3-D."""

    def __init__(self, app: tk.Tk) -> None:
        super().__init__(app)
        self.app = app
        self.title("LAT-CES — Početak projekta")
        self.geometry("760x700")
        self.minsize(700, 620)
        self.transient(app)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._blocked_close)

        self.step = 1
        self.level_index = 0
        self.level_specs: list[LevelProjectSpec] = []
        self.project_name = tk.StringVar(value="Novi objekat")
        self.floor_count = tk.IntVar(value=1)
        self.length = tk.StringVar()
        self.width = tk.StringVar()
        self.height = tk.StringVar(value="2.80")
        self.block_brand = tk.StringVar()
        self.block_l = tk.StringVar()
        self.block_w = tk.StringVar()
        self.block_h = tk.StringVar()
        self.wall_thickness = tk.StringVar(value="0.25")
        self.insulation = tk.StringVar(value="EPS / stiropor")
        self.insulation_thickness = tk.StringVar(value="0.10")
        self.facade_brand = tk.StringVar()
        self.granulation = tk.StringVar()
        self.render_thickness = tk.StringVar(value="0.005")
        self.roof_shape = tk.StringVar(value="Ravni")
        self.roof_height = tk.StringVar(value="0")
        self._rooms: list[tuple[tk.StringVar, tk.StringVar, tk.StringVar]] = []
        self._build()

    def _blocked_close(self) -> None:
        messagebox.showinfo("LAT-CES", "Početni projektni unos mora biti završen ili otkazan dugmetom 'Odustani'.", parent=self)

    def _build(self) -> None:
        header = ttk.Frame(self, padding=18)
        header.pack(fill="x")
        ttk.Label(header, text="LAT-CES — Početak projekta", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        self.subtitle = ttk.Label(header, text="Korak 1: osnovne dimenzije i građevinski sastav", wraplength=680)
        self.subtitle.pack(anchor="w", pady=(4, 0))
        self.body = ttk.Frame(self, padding=(18, 0, 18, 10))
        self.body.pack(fill="both", expand=True)
        footer = ttk.Frame(self, padding=18)
        footer.pack(fill="x")
        self.back_btn = ttk.Button(footer, text="← Nazad", command=self.back)
        self.back_btn.pack(side="left")
        self.cancel_btn = ttk.Button(footer, text="Odustani", command=self.cancel)
        self.cancel_btn.pack(side="left", padx=8)
        self.next_btn = ttk.Button(footer, text="Nastavi →", command=self.next)
        self.next_btn.pack(side="right")
        self._show_step_one()

    def _clear(self) -> None:
        for child in self.body.winfo_children():
            child.destroy()

    def _field(self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar, width: int = 18) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=1, sticky="ew", pady=4, padx=(10, 0))

    def _show_step_one(self) -> None:
        self._clear()
        self.step = 1
        self.back_btn.configure(state="disabled")
        self.next_btn.configure(text="Potvrdi etažu →")
        self.subtitle.configure(text=f"Korak 1: dimenzije, zid i raspored prostorija — {self.level_index + 1}. etaža")

        top = ttk.LabelFrame(self.body, text="Gabarit i visina", padding=12)
        top.pack(fill="x", pady=(0, 10))
        top.columnconfigure(1, weight=1)
        self._field(top, 0, "Dužina objekta (m)", self.length)
        self._field(top, 1, "Širina objekta (m)", self.width)
        self._field(top, 2, "Visina etaže (m)", self.height)
        if self.level_index == 0:
            self._field(top, 3, "Naziv projekta", self.project_name)

        construction = ttk.LabelFrame(self.body, text="Zidani sistem / fasada", padding=12)
        construction.pack(fill="x", pady=(0, 10))
        construction.columnconfigure(1, weight=1)
        self._field(construction, 0, "Marka bloka", self.block_brand)
        self._field(construction, 1, "Dužina bloka (m)", self.block_l)
        self._field(construction, 2, "Širina bloka (m)", self.block_w)
        self._field(construction, 3, "Visina bloka (m)", self.block_h)
        self._field(construction, 4, "Debljina zida (m)", self.wall_thickness)
        self._field(construction, 5, "Izolacija / materijal", self.insulation)
        self._field(construction, 6, "Debljina izolacije (m)", self.insulation_thickness)
        self._field(construction, 7, "Marka fasade", self.facade_brand)
        self._field(construction, 8, "Granulacija fasade (mm)", self.granulation)
        self._field(construction, 9, "Debljina završne žbuke (m)", self.render_thickness)

        rooms_box = ttk.LabelFrame(self.body, text="Program prostorija / raspored", padding=12)
        rooms_box.pack(fill="both", expand=True)
        ttk.Label(rooms_box, text="Prostorija").grid(row=0, column=0, sticky="w")
        ttk.Label(rooms_box, text="Dužina (m)").grid(row=0, column=1, sticky="w", padx=8)
        ttk.Label(rooms_box, text="Širina (m)").grid(row=0, column=2, sticky="w")
        for row in range(1, 8):
            name = tk.StringVar()
            l = tk.StringVar()
            w = tk.StringVar()
            self._rooms.append((name, l, w))
            ttk.Entry(rooms_box, textvariable=name).grid(row=row, column=0, sticky="ew", pady=2)
            ttk.Entry(rooms_box, textvariable=l, width=10).grid(row=row, column=1, padx=8, pady=2)
            ttk.Entry(rooms_box, textvariable=w, width=10).grid(row=row, column=2, pady=2)
        rooms_box.columnconfigure(0, weight=1)
        ttk.Label(rooms_box, text="Primjer: kuhinja, spavaća, WC, hodnik. Hodnik može biti dio gabarita osnovnog tlocrta.", foreground="#5f6368", wraplength=650).grid(row=8, column=0, columnspan=3, sticky="w", pady=(8, 0))

    def _parse_positive(self, value: str, label: str) -> float:
        try:
            number = float(value.replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"{label}: unesite broj") from exc
        if number <= 0:
            raise ValueError(f"{label}: vrijednost mora biti > 0")
        return number

    def _collect_level(self) -> LevelProjectSpec:
        length = self._parse_positive(self.length.get(), "Dužina")
        width = self._parse_positive(self.width.get(), "Širina")
        height = self._parse_positive(self.height.get(), "Visina etaže")
        wall_t = self._parse_positive(self.wall_thickness.get(), "Debljina zida")
        insulation_t = self._parse_positive(self.insulation_thickness.get(), "Debljina izolacije")
        render_t = self._parse_positive(self.render_thickness.get(), "Debljina završne žbuke")

        def optional_number(value: str) -> float:
            if not value.strip():
                return 0.0
            return float(value.replace(",", "."))

        rooms: list[RoomSpec] = []
        for name_var, l_var, w_var in self._rooms:
            name = name_var.get().strip()
            if not name:
                continue
            if not l_var.get().strip() or not w_var.get().strip():
                raise ValueError(f"Dimenzije prostorije '{name}' nisu unesene")
            rooms.append(RoomSpec(name=name, length_m=self._parse_positive(l_var.get(), f"Dužina prostorije {name}"), width_m=self._parse_positive(w_var.get(), f"Širina prostorije {name}")))

        construction = WallConstructionSpec(
            block_brand=self.block_brand.get().strip(),
            block_length_m=optional_number(self.block_l.get()),
            block_width_m=optional_number(self.block_w.get()),
            block_height_m=optional_number(self.block_h.get()),
            wall_thickness_m=wall_t,
            insulation_type=self.insulation.get().strip(),
            insulation_thickness_m=insulation_t,
            facade_brand=self.facade_brand.get().strip(),
            facade_granulation_mm=optional_number(self.granulation.get()),
            render_thickness_m=render_t,
        )
        return LevelProjectSpec(name=f"Etaža {self.level_index + 1}", height_m=height, length_m=length, width_m=width, construction=construction, rooms=rooms, finalized=True)

    def _show_floor_count(self) -> None:
        self._clear()
        self.step = 2
        self.back_btn.configure(state="normal")
        self.next_btn.configure(text="Započni etaže →")
        self.subtitle.configure(text="Korak 2: spratnost — odredite broj etaža prije nastavka")
        box = ttk.LabelFrame(self.body, text="Broj etaža", padding=24)
        box.pack(fill="x", pady=40)
        ttk.Label(box, text="Koliko etaža ima objekat? (1–50)", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Spinbox(box, from_=1, to=50, textvariable=self.floor_count, width=10).pack(anchor="w", pady=16)
        ttk.Label(box, text="Dok spratnost nije potvrđena, krov i 3D model ostaju zaključani.", foreground="#5f6368").pack(anchor="w")

    def _show_roof(self) -> None:
        self._clear()
        self.step = 3
        self.back_btn.configure(state="normal")
        self.next_btn.configure(text="Zaključi projekat →")
        self.subtitle.configure(text="Korak 3: krov — bira se tek nakon što su sve etaže unesene")
        box = ttk.LabelFrame(self.body, text="Krov", padding=20)
        box.pack(fill="x", pady=40)
        ttk.Label(box, text="Oblik krova").pack(anchor="w")
        ttk.Combobox(box, textvariable=self.roof_shape, values=("Ravni", "Jednovodni", "Dvovodni", "Četvorovodni", "Mansardni", "Drugi"), state="readonly").pack(fill="x", pady=6)
        ttk.Label(box, text="Visina/uzdignuće krova (m)").pack(anchor="w", pady=(12, 0))
        ttk.Entry(box, textvariable=self.roof_height).pack(fill="x", pady=6)
        ttk.Label(box, text="3D model se generiše nakon zaključavanja krova i svih visina etaža.", foreground="#5f6368").pack(anchor="w", pady=(12, 0))

    def next(self) -> None:
        try:
            if self.step == 1:
                spec = self._collect_level()
                if self.level_index < len(self.level_specs):
                    self.level_specs[self.level_index] = spec
                else:
                    self.level_specs.append(spec)
                self._show_floor_count()
            elif self.step == 2:
                count = int(self.floor_count.get())
                if count < 1 or count > 50:
                    raise ValueError("Spratnost mora biti između 1 i 50")
                if len(self.level_specs) > count:
                    self.level_specs = self.level_specs[:count]
                if len(self.level_specs) < count:
                    self.level_specs.extend(LevelProjectSpec(name=f"Etaža {i + 1}") for i in range(len(self.level_specs), count))
                self.level_index = 0
                self._load_level_into_form(self.level_specs[0])
                self.next_btn.configure(text="Zaključi etažu →")
                self._show_step_one()
                if count == 1:
                    self.next_btn.configure(text="Zaključi etažu i nastavi →")
            else:
                height = float(self.roof_height.get().replace(",", "."))
                if height < 0:
                    raise ValueError("Visina krova ne može biti negativna")
                self._finish(height)
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)

    def _load_level_into_form(self, spec: LevelProjectSpec) -> None:
        self.length.set(f"{spec.length_m:g}" if spec.length_m else "")
        self.width.set(f"{spec.width_m:g}" if spec.width_m else "")
        self.height.set(f"{spec.height_m:g}")
        c = spec.construction
        self.block_brand.set(c.block_brand); self.block_l.set(f"{c.block_length_m:g}" if c.block_length_m else "")
        self.block_w.set(f"{c.block_width_m:g}" if c.block_width_m else ""); self.block_h.set(f"{c.block_height_m:g}" if c.block_height_m else "")
        self.wall_thickness.set(f"{c.wall_thickness_m:g}" if c.wall_thickness_m else "0.25")
        self.insulation.set(c.insulation_type or "EPS / stiropor"); self.insulation_thickness.set(f"{c.insulation_thickness_m:g}" if c.insulation_thickness_m else "0.10")
        self.facade_brand.set(c.facade_brand); self.granulation.set(f"{c.facade_granulation_mm:g}" if c.facade_granulation_mm else "")
        self.render_thickness.set(f"{c.render_thickness_m:g}" if c.render_thickness_m else "0.005")
        self._rooms = []
        for room in spec.rooms:
            self._rooms.append((tk.StringVar(value=room.name), tk.StringVar(value=f"{room.length_m:g}"), tk.StringVar(value=f"{room.width_m:g}")))

    def _continue_levels(self, index: int) -> None:
        self.level_index = index
        self._load_level_into_form(self.level_specs[index])
        self._show_step_one()
        self.next_btn.configure(text="Zaključi etažu →")

    def back(self) -> None:
        if self.step == 2:
            self._show_step_one()
        elif self.step == 3:
            self._continue_levels(max(0, len(self.level_specs) - 1))

    def cancel(self) -> None:
        self.grab_release()
        self.destroy()

    def _finish(self, roof_height: float) -> None:
        project = BuildingProjectSpec(name=self.project_name.get().strip() or "Novi objekat")
        project.set_floor_count(len(self.level_specs))
        project.levels = self.level_specs
        project.floor_count_finalized = True
        project.roof_shape = self.roof_shape.get()
        project.roof_height_m = roof_height
        workflow = BuildingWorkflow(model=BuildingModel(name=project.name), project_spec=project, current_step=3, roof_shape=project.roof_shape, roof_height_m=roof_height)
        for index, spec in enumerate(project.levels):
            workflow.set_level_spec(index, spec)
        project.floor_count_finalized = True
        workflow.current_step = 4
        self.app.workflow = workflow
        self.app.step_var.set(4)
        self.app.redraw_active_view()
        self.app.refresh_level_combo()
        self.app.update_summary()
        self.grab_release()
        self.destroy()
        messagebox.showinfo("LAT-CES", "Osnovni Building Model je formiran. Sljedeći korak je pregled 3D modela.", parent=self.app)

    def start(self) -> None:
        self._show_step_one()
