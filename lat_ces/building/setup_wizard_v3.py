"""Sequential compact Building-first project setup.

Workflow: ground floor -> optional floor 1 -> optional floor 2 -> roof -> 3-D.
Each level is saved independently into one BuildingProjectSpec.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .model import BuildingModel
from .project_spec import (
    BuildingProjectSpec,
    LevelProjectSpec,
    RoomSpec,
    WallConstructionSpec,
)
from .workflow import BuildingWorkflow


class SetupWizardV3(tk.Toplevel):
    """Compact sequential setup for ground floor and up to two upper floors."""

    def __init__(self, app: tk.Tk, workflow: BuildingWorkflow) -> None:
        super().__init__(app)
        self.app = app
        self.workflow = workflow
        self.title("LAT-CES — Objekat")
        self.geometry("900x700")
        self.minsize(820, 620)
        self.transient(app)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.phase = "ground"
        self.floor_index = 0
        self.project_name = tk.StringVar(value="Novi objekat")
        self.upper_floors = tk.IntVar(value=0)
        self.level_specs: list[LevelProjectSpec] = []
        self.roof_shape = tk.StringVar(value="Ravni")
        self.roof_height = tk.StringVar(value="0")
        self.vars = {k: tk.StringVar(value=v) for k, v in {
            "length": "", "width": "", "height": "2.80",
            "block": "", "block_l": "", "block_w": "", "block_h": "",
            "wall": "0.25", "insulation": "EPS / stiropor", "insulation_t": "0.10",
            "facade": "", "granulation": "", "render": "0.005",
        }.items()}
        self.room_vars: list[list[tk.StringVar]] = []
        self._render_ground()

    @staticmethod
    def _num(value: str, label: str, positive: bool = True) -> float:
        try:
            result = float(value.replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"{label}: unesite broj") from exc
        if positive and result <= 0:
            raise ValueError(f"{label}: mora biti > 0")
        return result

    def _clear_shell(self, title: str, subtitle: str) -> ttk.Frame:
        for child in self.winfo_children():
            child.destroy()
        head = ttk.Frame(self, padding=(18, 14, 18, 8))
        head.pack(fill="x")
        ttk.Label(head, text=title, font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(head, text=subtitle, foreground="#5f6368", wraplength=820).pack(anchor="w", pady=(3, 0))
        body = ttk.Frame(self, padding=(18, 0, 18, 8))
        body.pack(fill="both", expand=True)
        return body

    def _footer(self, primary: str, command, secondary: str | None = None, secondary_command=None) -> None:
        foot = ttk.Frame(self, padding=18)
        foot.pack(fill="x")
        ttk.Button(foot, text="Odustani", command=self.cancel).pack(side="left")
        if secondary and secondary_command:
            ttk.Button(foot, text=secondary, command=secondary_command).pack(side="left", padx=8)
        ttk.Button(foot, text=primary, command=command).pack(side="right")

    def _entry(self, parent: ttk.Frame, row: int, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(parent, textvariable=variable, width=22).grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=2)

    def _ensure_rooms(self, spec: LevelProjectSpec | None) -> None:
        existing = spec.rooms if spec else []
        self.room_vars = []
        for room in existing:
            self.room_vars.append([
                tk.StringVar(value=room.name),
                tk.StringVar(value=f"{room.length_m:g}"),
                tk.StringVar(value=f"{room.width_m:g}"),
            ])
        while len(self.room_vars) < 8:
            self.room_vars.append([tk.StringVar(), tk.StringVar(), tk.StringVar()])

    def _load_spec(self, spec: LevelProjectSpec | None) -> None:
        spec = spec or LevelProjectSpec(name=f"Etaža {self.floor_index + 1}")
        c = spec.construction
        values = {
            "length": spec.length_m,
            "width": spec.width_m,
            "height": spec.height_m,
            "block": c.block_brand,
            "block_l": c.block_length_m,
            "block_w": c.block_width_m,
            "block_h": c.block_height_m,
            "wall": c.wall_thickness_m or 0.25,
            "insulation": c.insulation_type or "EPS / stiropor",
            "insulation_t": c.insulation_thickness_m or 0.10,
            "facade": c.facade_brand,
            "granulation": c.facade_granulation_mm,
            "render": c.render_thickness_m or 0.005,
        }
        for key, value in values.items():
            if isinstance(value, (float, int)):
                self.vars[key].set(f"{value:g}")
            else:
                self.vars[key].set(str(value))
        self._ensure_rooms(spec)

    def _collect_level(self, name: str) -> LevelProjectSpec:
        rooms: list[RoomSpec] = []
        for name_var, length_var, width_var in self.room_vars:
            room_name = name_var.get().strip()
            if not room_name:
                continue
            rooms.append(RoomSpec(
                name=room_name,
                length_m=self._num(length_var.get(), f"Dužina {room_name}"),
                width_m=self._num(width_var.get(), f"Širina {room_name}"),
            ))
        def opt(key: str) -> float:
            text = self.vars[key].get().strip()
            return self._num(text, key) if text else 0.0
        construction = WallConstructionSpec(
            block_brand=self.vars["block"].get().strip(),
            block_length_m=opt("block_l"),
            block_width_m=opt("block_w"),
            block_height_m=opt("block_h"),
            wall_thickness_m=self._num(self.vars["wall"].get(), "Debljina zida"),
            insulation_type=self.vars["insulation"].get().strip(),
            insulation_thickness_m=self._num(self.vars["insulation_t"].get(), "Debljina izolacije"),
            facade_brand=self.vars["facade"].get().strip(),
            facade_granulation_mm=opt("granulation"),
            render_thickness_m=self._num(self.vars["render"].get(), "Debljina završne žbuke"),
        )
        return LevelProjectSpec(
            name=name,
            height_m=self._num(self.vars["height"].get(), "Visina etaže"),
            length_m=self._num(self.vars["length"].get(), "Dužina objekta"),
            width_m=self._num(self.vars["width"].get(), "Širina objekta"),
            construction=construction,
            rooms=rooms,
            finalized=True,
        )

    def _render_ground(self) -> None:
        self.phase = "ground"
        self.floor_index = 0
        body = self._clear_shell(
            "1. Prizemlje — osnovni tlocrt",
            "Unesi gabarit, zid, izolaciju i program prostorija. Nakon 'Spremi prizemlje' unos odmah postaje tlocrt objekta.",
        )
        top = ttk.Frame(body)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="Spratnost objekta:", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Combobox(top, textvariable=self.upper_floors, values=(0, 1, 2), state="readonly", width=6).pack(side="left", padx=8)
        ttk.Label(top, text="(0 = samo prizemlje, 1 = prizemlje + sprat 1, 2 = + sprat 2)", foreground="#5f6368").pack(side="left")

        grid = ttk.Frame(body)
        grid.pack(fill="both", expand=True)
        left = ttk.LabelFrame(grid, text="Gabarit i konstrukcija", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.columnconfigure(1, weight=1)
        self._entry(left, 0, "Naziv projekta", self.project_name)
        self._entry(left, 1, "Dužina objekta (m)", self.vars["length"])
        self._entry(left, 2, "Širina objekta (m)", self.vars["width"])
        self._entry(left, 3, "Visina etaže (m)", self.vars["height"])
        for row, (label, key) in enumerate((
            ("Marka bloka", "block"), ("Dužina bloka (m)", "block_l"), ("Širina bloka (m)", "block_w"),
            ("Visina bloka (m)", "block_h"), ("Debljina zida (m)", "wall"), ("Izolacija", "insulation"),
            ("Debljina izolacije (m)", "insulation_t"), ("Marka fasade", "facade"), ("Granulacija (mm)", "granulation"),
            ("Završna žbuka (m)", "render"),
        ), start=4):
            self._entry(left, row, label, self.vars[key])
        right = ttk.LabelFrame(grid, text="Program prostorija / raspored", padding=10)
        right.pack(side="left", fill="both", expand=True)
        for col, label in enumerate(("Prostorija", "Dužina (m)", "Širina (m)")):
            ttk.Label(right, text=label).grid(row=0, column=col, sticky="w")
        for row, room in enumerate(self.room_vars, start=1):
            for col, variable in enumerate(room):
                ttk.Entry(right, textvariable=variable).grid(row=row, column=col, sticky="ew" if col == 0 else "w", padx=(0 if col == 0 else 8), pady=2)
        right.columnconfigure(0, weight=1)
        self._footer(
            "Spremi prizemlje →",
            self.save_current_level,
            secondary="Završi tlocrt →",
            secondary_command=self.finish_tlocrta,
        )

    def _render_level(self, index: int) -> None:
        self.phase = "level"
        self.floor_index = index
        self._load_spec(self.level_specs[index])
        name = f"Sprat {index}"
        body = self._clear_shell(
            f"{2 + index}. {name} — tlocrt",
            "Svaki sprat ima potpuno nezavisan tlocrt. Spremanjem ove etaže prelazi se na sljedeću ili na krov.",
        )
        grid = ttk.Frame(body)
        grid.pack(fill="both", expand=True)
        left = ttk.LabelFrame(grid, text="Gabarit etaže", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.columnconfigure(1, weight=1)
        self._entry(left, 0, "Dužina (m)", self.vars["length"])
        self._entry(left, 1, "Širina (m)", self.vars["width"])
        self._entry(left, 2, "Visina (m)", self.vars["height"])
        for row, (label, key) in enumerate((
            ("Marka bloka", "block"), ("Dužina bloka (m)", "block_l"), ("Širina bloka (m)", "block_w"),
            ("Visina bloka (m)", "block_h"), ("Debljina zida (m)", "wall"), ("Izolacija", "insulation"),
            ("Debljina izolacije (m)", "insulation_t"), ("Marka fasade", "facade"), ("Granulacija (mm)", "granulation"),
            ("Završna žbuka (m)", "render"),
        ), start=3):
            self._entry(left, row, label, self.vars[key])
        right = ttk.LabelFrame(grid, text=f"Program prostorija — {name}", padding=10)
        right.pack(side="left", fill="both", expand=True)
        for col, label in enumerate(("Prostorija", "Dužina (m)", "Širina (m)")):
            ttk.Label(right, text=label).grid(row=0, column=col, sticky="w")
        for row, room in enumerate(self.room_vars, start=1):
            for col, variable in enumerate(room):
                ttk.Entry(right, textvariable=variable).grid(row=row, column=col, sticky="ew" if col == 0 else "w", padx=(0 if col == 0 else 8), pady=2)
        right.columnconfigure(0, weight=1)
        next_label = "Spremi sprat i pređi na krov →" if index == len(self.level_specs) - 1 else f"Spremi sprat {index} i pređi na sprat {index + 1} →"
        self._footer(next_label, self.save_current_level, secondary="← Nazad", secondary_command=self.back_level)

    def _render_roof(self) -> None:
        self.phase = "roof"
        body = self._clear_shell(
            "Krov — završni dio objekta",
            "Krov je dio istog Building Modela. Kada ga potvrdiš, cijeli objekat ide u 3D model.",
        )
        box = ttk.LabelFrame(body, text="Krov", padding=20)
        box.pack(fill="x", pady=50)
        ttk.Label(box, text="Oblik krova").pack(anchor="w")
        ttk.Combobox(box, textvariable=self.roof_shape, values=("Ravni", "Jednovodni", "Dvovodni", "Četvorovodni", "Mansardni", "Drugi"), state="readonly").pack(fill="x", pady=5)
        ttk.Label(box, text="Visina / uzdignuće krova (m)").pack(anchor="w", pady=(10, 0))
        ttk.Entry(box, textvariable=self.roof_height).pack(fill="x", pady=5)
        self._footer("Završi objekat i generiši 3D →", self.finish_object, secondary="← Nazad", secondary_command=self.back_from_roof)

    def save_current_level(self) -> None:
        try:
            name = "Prizemlje" if self.floor_index == 0 else f"Sprat {self.floor_index}"
            spec = self._collect_level(name)
            if self.floor_index >= len(self.level_specs):
                self.level_specs.extend(LevelProjectSpec(name=f"Etaža {i + 1}") for i in range(len(self.level_specs), self.floor_index + 1))
            self.level_specs[self.floor_index] = spec
            if self.floor_index == 0:
                self.upper_floors.set(int(self.upper_floors.get()))
                if self.upper_floors.get() == 0:
                    self.finish_tlocrta()
                    return
                self._render_level(1)
                return
            if self.floor_index < len(self.level_specs) - 1:
                self._render_level(self.floor_index + 1)
            else:
                self._render_roof()
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)

    def finish_tlocrta(self) -> None:
        try:
            spec = self._collect_level("Prizemlje")
            self.level_specs = [spec]
            self.upper_floors.set(0)
            self._render_roof()
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)

    def back_level(self) -> None:
        if self.floor_index == 1:
            self._render_ground()
        elif self.floor_index > 1:
            self._render_level(self.floor_index - 1)

    def back_from_roof(self) -> None:
        if self.level_specs:
            self._render_level(len(self.level_specs) - 1)
        else:
            self._render_ground()

    def finish_object(self) -> None:
        try:
            roof_h = self._num(self.roof_height.get(), "Visina krova", positive=False)
            if not self.level_specs:
                raise ValueError("Prvo mora biti spremljeno prizemlje")
            project = BuildingProjectSpec(
                name=self.project_name.get().strip() or "Novi objekat",
                floor_count=len(self.level_specs),
                levels=self.level_specs,
                floor_count_finalized=True,
                roof_shape=self.roof_shape.get(),
                roof_height_m=roof_h,
            )
            workflow = BuildingWorkflow(
                model=BuildingModel(project.name),
                project_spec=project,
                current_step=4,
                roof_shape=project.roof_shape,
                roof_height_m=roof_h,
            )
            for index, spec in enumerate(project.levels):
                workflow.set_level_spec(index, spec)
            self.app.workflow = workflow
            self.app.on_setup_complete()
            self.grab_release()
            self.destroy()
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES", str(exc), parent=self)

    def back(self) -> None:
        if self.phase == "ground":
            self.cancel()
        elif self.phase == "level":
            self.back_level()
        elif self.phase == "roof":
            self.back_from_roof()

    def cancel(self) -> None:
        self.grab_release()
        self.destroy()
