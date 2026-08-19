"""Complete desktop Building Model workspace.

Keeps the verified drafting GUI as the rendering core and adds real tabs for
roof dimensions, envelope layers, structural inputs/load take-off, engineering
reports and MEP access.
"""
from __future__ import annotations

import json
import math
import tkinter as tk
from tkinter import messagebox, ttk

from lat_ces.building.model import Material, Roof
from lat_ces.building.structural import calculate_structural_loads
from lat_ces.building.mep import ensure_mep_registry
from lat_ces.building.mep_engineering import ensure_engineering_results
from lat_ces.building.engineering_report import build_building_engineering_report
from lat_ces.building.floor_plan import Point2D, Segment2D
from lat_ces.gui_drafting import DraftingLATCESApp
from lat_ces.gui_mep_engineering import EngineeringMEPWorkspaceApp


class CompleteBuildingWorkspaceApp(DraftingLATCESApp):
    """Verified drafting GUI plus integrated envelope, structure, report and MEP tabs."""

    def __init__(self) -> None:
        self.facade_direction_var = None
        self.envelope_finish_var = None
        self.envelope_insulation_material_var = None
        self.envelope_insulation_thickness_var = None
        self.envelope_plaster_material_var = None
        self.envelope_plaster_thickness_var = None
        self.wall_load_bearing_var = None
        self.wall_material_var = None
        self.wall_tributary_var = None
        self.level_dead_load_var = None
        self.level_live_load_var = None
        self.material_name_var = None
        self.material_density_var = None
        self.material_e_var = None
        self.material_lambda_var = None
        self.roof_length_var = None
        self.roof_width_var = None
        self.roof_dead_load_var = None
        self.roof_snow_load_var = None
        self.calculation_output = None
        self.mep_output = None
        super().__init__()
        self._install_complete_tabs()
        self._refresh_complete_tabs()

    def _install_complete_tabs(self) -> None:
        children = list(self.winfo_children())
        old_steps = next((child for child in children if isinstance(child, ttk.Frame) and any(isinstance(x, ttk.Radiobutton) for x in child.winfo_children())), None)
        body = next((child for child in children if isinstance(child, ttk.Frame) and any(isinstance(x, ttk.LabelFrame) for x in child.winfo_children())), None)
        if old_steps is not None:
            old_steps.pack_forget()
        if body is None:
            return

        self.complete_tabs = ttk.Notebook(self)
        self.complete_tabs.pack(fill="x", padx=18, pady=(0, 8), before=body)
        self.complete_tabs.bind("<<NotebookTabChanged>>", self._complete_tab_changed)

        model_tab = ttk.Frame(self.complete_tabs, padding=8)
        envelope_tab = ttk.Frame(self.complete_tabs, padding=8)
        structure_tab = ttk.Frame(self.complete_tabs, padding=8)
        calc_tab = ttk.Frame(self.complete_tabs, padding=8)
        mep_tab = ttk.Frame(self.complete_tabs, padding=8)
        facade_tab = ttk.Frame(self.complete_tabs, padding=8)
        self.complete_tabs.add(model_tab, text="Model / Pogledi")
        self.complete_tabs.add(envelope_tab, text="Omotač / Fasada")
        self.complete_tabs.add(structure_tab, text="Konstrukcija / Statika")
        self.complete_tabs.add(calc_tab, text="Proračuni")
        self.complete_tabs.add(mep_tab, text="MEP")
        self.complete_tabs.add(facade_tab, text="Fasade")

        self._build_model_tab(model_tab)
        self._build_envelope_tab(envelope_tab)
        self._build_structure_tab(structure_tab)
        self._build_calculation_tab(calc_tab)
        self._build_mep_tab(mep_tab)
        self._build_facade_tab(facade_tab)

    def _build_model_tab(self, tab: ttk.Frame) -> None:
        ttk.Label(tab, text="Building Model", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 10))
        for label, step in (("Krov", 1), ("Sprat / dimenzije", 2), ("Tlocrt", 3), ("Presjek", 4), ("3D", 5)):
            ttk.Button(tab, text=label, command=lambda s=step: self._set_view_step(s)).pack(side="left", padx=2)
        ttk.Label(tab, text="Jedan BuildingModel ostaje izvor geometrije za sve prikaze i proračune.", foreground="#475569").pack(side="left", padx=12)

    def _build_envelope_tab(self, tab: ttk.Frame) -> None:
        self.envelope_finish_var = tk.StringVar(value=self.active_level.facade_finish)
        self.envelope_insulation_material_var = tk.StringVar(value=self.active_level.insulation_material)
        self.envelope_insulation_thickness_var = tk.StringVar(value=f"{self.active_level.insulation_thickness_m:.3f}")
        self.envelope_plaster_material_var = tk.StringVar(value=self.active_level.interior_plaster_material)
        self.envelope_plaster_thickness_var = tk.StringVar(value=f"{self.active_level.interior_plaster_thickness_m:.3f}")
        fields = (
            ("Fasadna završna obrada", self.envelope_finish_var),
            ("Izolacija — materijal", self.envelope_insulation_material_var),
            ("Izolacija — debljina (m)", self.envelope_insulation_thickness_var),
            ("Unutrašnja žbuka — materijal", self.envelope_plaster_material_var),
            ("Unutrašnja žbuka — debljina (m)", self.envelope_plaster_thickness_var),
        )
        for row, (label, var) in enumerate(fields):
            ttk.Label(tab, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(tab, textvariable=var, width=30).grid(row=row, column=1, sticky="ew", padx=8, pady=2)
        ttk.Button(tab, text="Primijeni slojeve omotača", command=self._apply_envelope).grid(row=5, column=0, columnspan=2, sticky="ew", pady=7)
        ttk.Label(tab, text="Ovi podaci ulaze u BuildingModel i kasnije u termički/energetski proračun. 3D prikaz ih prikazuje u legendi.", wraplength=700, foreground="#475569").grid(row=6, column=0, columnspan=2, sticky="w")
        tab.columnconfigure(1, weight=1)

    def _build_structure_tab(self, tab: ttk.Frame) -> None:
        self.wall_load_bearing_var = tk.BooleanVar(value=False)
        self.wall_material_var = tk.StringVar(value="")
        self.wall_tributary_var = tk.StringVar(value="0.00")
        self.level_dead_load_var = tk.StringVar(value=f"{self.active_level.dead_load_kpa:.2f}")
        self.level_live_load_var = tk.StringVar(value=f"{self.active_level.live_load_kpa:.2f}")
        ttk.Label(tab, text="Odabrani zid", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", columnspan=2)
        ttk.Checkbutton(tab, text="Nosivi zid", variable=self.wall_load_bearing_var).grid(row=1, column=0, sticky="w", pady=3)
        ttk.Label(tab, text="Materijal").grid(row=2, column=0, sticky="w")
        self.wall_material_combo = ttk.Combobox(tab, textvariable=self.wall_material_var, state="readonly", width=30)
        self.wall_material_combo.grid(row=2, column=1, sticky="ew", padx=8)
        ttk.Label(tab, text="Tributarna širina (m)").grid(row=3, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.wall_tributary_var).grid(row=3, column=1, sticky="ew", padx=8)
        ttk.Button(tab, text="Primijeni svojstva zida", command=self._apply_wall_structure).grid(row=4, column=0, columnspan=2, sticky="ew", pady=7)
        ttk.Separator(tab).grid(row=5, column=0, columnspan=2, sticky="ew", pady=6)
        ttk.Label(tab, text="Opterećenje etaže", font=("Segoe UI", 10, "bold")).grid(row=6, column=0, columnspan=2, sticky="w")
        ttk.Label(tab, text="Stalno q (kPa)").grid(row=7, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.level_dead_load_var).grid(row=7, column=1, sticky="ew", padx=8)
        ttk.Label(tab, text="Korisno q (kPa)").grid(row=8, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.level_live_load_var).grid(row=8, column=1, sticky="ew", padx=8)
        ttk.Button(tab, text="Primijeni opterećenje etaže", command=self._apply_level_loads).grid(row=9, column=0, columnspan=2, sticky="ew", pady=7)
        ttk.Separator(tab).grid(row=10, column=0, columnspan=2, sticky="ew", pady=6)
        ttk.Label(tab, text="Materijal za statiku", font=("Segoe UI", 10, "bold")).grid(row=11, column=0, columnspan=2, sticky="w")
        self.material_name_var = tk.StringVar(value="Armirani beton")
        self.material_density_var = tk.StringVar(value="2500")
        self.material_e_var = tk.StringVar(value="30000000000")
        self.material_lambda_var = tk.StringVar(value="2.10")
        for row, (label, var) in enumerate((("Naziv", self.material_name_var), ("Gustina (kg/m³)", self.material_density_var), ("E (Pa)", self.material_e_var), ("λ (W/mK)", self.material_lambda_var)), start=12):
            ttk.Label(tab, text=label).grid(row=row, column=0, sticky="w")
            ttk.Entry(tab, textvariable=var).grid(row=row, column=1, sticky="ew", padx=8)
        ttk.Button(tab, text="Dodaj materijal", command=self._add_material).grid(row=16, column=0, columnspan=2, sticky="ew", pady=7)
        tab.columnconfigure(1, weight=1)

    def _build_calculation_tab(self, tab: ttk.Frame) -> None:
        ttk.Button(tab, text="Izračunaj preliminarna vertikalna opterećenja", command=self._calculate_structure).pack(fill="x", pady=2)
        ttk.Button(tab, text="Izradi Building Engineering Report", command=self._calculate_building_report).pack(fill="x", pady=2)
        ttk.Button(tab, text="Provjeri BuildingModel", command=self.validate_model).pack(fill="x", pady=2)
        self.calculation_output = tk.Text(tab, height=9, width=95, wrap="word")
        self.calculation_output.pack(fill="both", expand=True, pady=(8, 0))
        self.calculation_output.configure(state="disabled")

    def _build_mep_tab(self, tab: ttk.Frame) -> None:
        ttk.Button(tab, text="Otvori MEP editor", command=self._open_mep_editor).pack(side="left", padx=(0, 6))
        ttk.Button(tab, text="Izračunaj sve MEP", command=self._calculate_building_report).pack(side="left", padx=6)
        ttk.Button(tab, text="Osvježi MEP listu", command=self._refresh_mep_tab).pack(side="left", padx=6)
        self.mep_output = tk.Text(tab, height=7, width=95, wrap="word")
        self.mep_output.pack(fill="both", expand=True, pady=(8, 0))
        self.mep_output.configure(state="disabled")

    def _build_facade_tab(self, tab: ttk.Frame) -> None:
        self.facade_direction_var = tk.StringVar(value="Sjever")
        ttk.Label(tab, text="Smjer fasade").pack(side="left")
        ttk.Combobox(tab, textvariable=self.facade_direction_var, state="readonly", values=("Sjever", "Istok", "Jug", "Zapad"), width=10).pack(side="left", padx=8)
        ttk.Button(tab, text="Prikaži fasadu", command=self._draw_facade).pack(side="left")
        ttk.Label(tab, text="Fasada koristi isti BuildingModel; otvori i slojevi omotača ostaju vezani za model.", foreground="#475569").pack(side="left", padx=12)

    def _complete_tab_changed(self, _event=None) -> None:
        self._refresh_complete_tabs()

    def _set_view_step(self, step: int) -> None:
        self.view_step.set(step)
        self.goto_step()

    def _apply_envelope(self) -> None:
        try:
            level = self.active_level
            level.facade_finish = self.envelope_finish_var.get().strip()
            level.insulation_material = self.envelope_insulation_material_var.get().strip()
            level.insulation_thickness_m = float(self.envelope_insulation_thickness_var.get())
            level.interior_plaster_material = self.envelope_plaster_material_var.get().strip()
            level.interior_plaster_thickness_m = float(self.envelope_plaster_thickness_var.get())
            if min(level.insulation_thickness_m, level.interior_plaster_thickness_m) < 0:
                raise ValueError("Debljina sloja ne može biti negativna")
        except ValueError as exc:
            messagebox.showwarning("LAT-CES — Omotač", str(exc), parent=self)
            return
        self.status_var.set("Slojevi omotača primijenjeni na BuildingModel")
        self.refresh_view()

    def _apply_level_loads(self) -> None:
        try:
            self.active_level.dead_load_kpa = float(self.level_dead_load_var.get())
            self.active_level.live_load_kpa = float(self.level_live_load_var.get())
            if min(self.active_level.dead_load_kpa, self.active_level.live_load_kpa) < 0:
                raise ValueError("Opterećenja ne mogu biti negativna")
        except ValueError as exc:
            messagebox.showwarning("LAT-CES — Statika", str(exc), parent=self)
            return
        self.status_var.set("Opterećenja etaže spremljena")

    def _apply_wall_structure(self) -> None:
        wall = self.floor_plan.walls.get(self.editor.selected_wall_id) if self.editor.selected_wall_id else None
        if wall is None:
            messagebox.showinfo("LAT-CES — Konstrukcija", "Prvo odaberi zid na tlocrtu.", parent=self)
            return
        try:
            tributary = float(self.wall_tributary_var.get())
            if tributary < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("LAT-CES — Konstrukcija", "Tributarna širina mora biti >= 0.", parent=self)
            return
        wall.load_bearing = bool(self.wall_load_bearing_var.get())
        wall.material_id = self.wall_material_combo.get() or None
        if wall.material_id:
            wall.material_id = next((mid for mid, mat in self.workflow.model.materials.items() if mat.name == wall.material_id), wall.material_id)
        wall.tributary_width_m = tributary
        self.status_var.set(f"{wall.role_label} · {wall.name}")
        self.refresh_view()

    def _add_material(self) -> None:
        try:
            material = Material(
                name=self.material_name_var.get().strip(),
                density=float(self.material_density_var.get()),
                youngs_modulus=float(self.material_e_var.get()),
                thermal_conductivity=float(self.material_lambda_var.get()),
            )
            self.workflow.model.add_material(material)
        except (ValueError, TypeError) as exc:
            messagebox.showwarning("LAT-CES — Materijal", str(exc), parent=self)
            return
        self.status_var.set(f"Materijal dodat: {material.name}")
        self._refresh_structure_materials()

    def _refresh_structure_materials(self) -> None:
        if not hasattr(self, "wall_material_combo"):
            return
        self.wall_material_combo["values"] = [material.name for material in self.workflow.model.materials.values()]
        wall = self.floor_plan.walls.get(self.editor.selected_wall_id) if self.editor.selected_wall_id else None
        if wall and wall.material_id in self.workflow.model.materials:
            self.wall_material_var.set(self.workflow.model.materials[wall.material_id].name)

    def _calculate_structure(self) -> None:
        report = calculate_structural_loads(self.workflow.model)
        lines = [f"Status: {report.status}", f"Ukupno vertikalno linijsko opterećenje: {report.total_vertical_line_load_kn_m:.3f} kN/m"]
        if report.findings:
            lines.append("\nNalazi:")
            lines.extend(f"- {finding}" for finding in report.findings)
        if report.walls:
            lines.append("\nNosivi zidovi:")
            for wall in report.walls:
                lines.append(f"{wall.wall_name} · vlastita {wall.self_weight_kn_m:.3f} · etaža {wall.tributary_floor_load_kn_m:.3f} · krov {wall.tributary_roof_load_kn_m:.3f} · ukupno {wall.total_line_load_kn_m:.3f} kN/m")
        self._set_output(self.calculation_output, "\n".join(lines))

    def _calculate_building_report(self) -> None:
        report = build_building_engineering_report(self.workflow.model)
        lines = [
            f"Status: {report.status}",
            f"Rezultata: {report.result_count}",
            f"CALCULATED: {report.calculated_count}",
            f"INPUT_REQUIRED: {report.input_required_count}",
            f"INPUT_CONFLICT: {report.conflict_count}",
            f"Ventilacija: {report.total_ventilation_flow_m3_h:.3f} m³/h",
            f"Grijanje: {report.total_heating_load_w:.3f} W",
            f"Voda: {report.total_water_pressure_drop_pa:.3f} Pa",
        ]
        self._set_output(self.calculation_output, "\n".join(lines))
        self._refresh_mep_tab()

    def _refresh_mep_tab(self) -> None:
        if self.mep_output is None:
            return
        registry = ensure_mep_registry(self.workflow.model)
        results = ensure_engineering_results(registry)
        lines = [
            f"Ventilacija: {len(registry.all_ventilation_openings)}",
            f"Vodene grane: {len(registry.all_water_branches)}",
            f"Zone grijanja: {len(registry.all_heating_zones)}",
        ]
        for result in results.all:
            lines.append(f"{result.object_type}:{result.object_id} → {result.status}")
        self._set_output(self.mep_output, "\n".join(lines))

    def _open_mep_editor(self) -> None:
        try:
            app = EngineeringMEPWorkspaceApp()
            app.title("LAT-CES — MEP Engineering")
            app.mainloop()
        except Exception as exc:
            messagebox.showerror("LAT-CES — MEP", str(exc), parent=self)

    @staticmethod
    def _set_output(widget, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _refresh_complete_tabs(self) -> None:
        if self.envelope_finish_var is not None:
            level = self.active_level
            self.envelope_finish_var.set(level.facade_finish)
            self.envelope_insulation_material_var.set(level.insulation_material)
            self.envelope_insulation_thickness_var.set(f"{level.insulation_thickness_m:.3f}")
            self.envelope_plaster_material_var.set(level.interior_plaster_material)
            self.envelope_plaster_thickness_var.set(f"{level.interior_plaster_thickness_m:.3f}")
        self._refresh_structure_materials()
        self._refresh_mep_tab()

    def refresh_view(self) -> None:
        super().refresh_view()
        self._refresh_complete_tabs()

    def update_selected_wall(self) -> None:
        super().update_selected_wall()
        wall = self.floor_plan.walls.get(self.editor.selected_wall_id) if self.editor.selected_wall_id else None
        if wall is not None and self.wall_load_bearing_var is not None:
            self.wall_load_bearing_var.set(wall.load_bearing)
            self.wall_tributary_var.set(f"{wall.tributary_width_m:.2f}")
            if wall.material_id and wall.material_id in self.workflow.model.materials:
                self.wall_material_var.set(self.workflow.model.materials[wall.material_id].name)

    def apply_roof(self) -> None:
        try:
            roof = Roof(
                roof_type=self.roof_type_var.get().strip(),
                construction=self.roof_construction_var.get().strip(),
                covering=self.roof_covering_var.get().strip(),
                substructure=self.roof_substructure_var.get().strip(),
                support=self.roof_support_var.get().strip(),
                length_m=float(self.roof_length_var.get()) if self.roof_length_var else float(self.level_length_var.get()),
                width_m=float(self.roof_width_var.get()) if self.roof_width_var else float(self.level_width_var.get()),
                slope_deg=float(self.roof_slope_var.get()),
                height_m=float(self.roof_height_var.get()),
                dead_load_kpa=float(self.roof_dead_load_var.get()) if self.roof_dead_load_var else 0.0,
                snow_load_kpa=float(self.roof_snow_load_var.get()) if self.roof_snow_load_var else 0.0,
            )
            self.workflow.model.set_roof(roof)
        except ValueError as exc:
            messagebox.showwarning("LAT-CES — Krov", str(exc), parent=self)
            return
        self.status_var.set(f"Krov: {roof.length_m:.2f} × {roof.width_m:.2f} m · {roof.slope_deg:.1f}°")
        self.refresh_view()

    def _draw_facade(self) -> None:
        self.view_step.set(5)
        self.canvas.delete("all")
        direction = self.facade_direction_var.get()
        width, height = max(self.canvas.winfo_width(), 700), max(self.canvas.winfo_height(), 450)
        levels = list(self.workflow.model.levels.values())
        scale = min(55.0, (width - 160) / max(max((l.length_m for l in levels), default=10.0), 1.0))
        base_y = height - 60
        current_z = 0.0
        horizontal = direction in {"Sjever", "Jug"}
        for level in levels:
            span = level.length_m if horizontal else level.width_m
            x0 = (width - span * scale) / 2.0
            x1 = x0 + span * scale
            y0 = base_y - current_z * scale * 0.65
            y1 = y0 - level.height * scale * 0.65
            self.canvas.create_rectangle(x0, y1, x1, y0, outline="#374151", width=3)
            if level.floor_plan:
                for wall in level.floor_plan.walls.values():
                    aligned = abs(wall.segment.start.y - wall.segment.end.y) < 1e-6 if horizontal else abs(wall.segment.start.x - wall.segment.end.x) < 1e-6
                    if not aligned:
                        continue
                    coordinate = wall.segment.start.y if horizontal else wall.segment.start.x
                    edge = level.width_m if direction == "Sjever" else 0.0 if direction == "Jug" else level.length_m if direction == "Istok" else 0.0
                    if abs(coordinate - edge) > max(0.25, wall.thickness):
                        continue
                    axis0 = min(wall.segment.start.x, wall.segment.end.x) if horizontal else min(wall.segment.start.y, wall.segment.end.y)
                    axis1 = max(wall.segment.start.x, wall.segment.end.x) if horizontal else max(wall.segment.start.y, wall.segment.end.y)
                    for opening in wall.openings:
                        fraction0 = opening.offset / max(wall.segment.length, 1e-9)
                        fraction1 = (opening.offset + opening.width) / max(wall.segment.length, 1e-9)
                        ox0 = x0 + (axis0 * scale) + (axis1 - axis0) * scale * fraction0
                        ox1 = x0 + (axis0 * scale) + (axis1 - axis0) * scale * fraction1
                        oy1 = y0 - opening.height_m * scale * 0.65
                        self.canvas.create_rectangle(ox0, oy1, ox1, y0, fill="white", outline="#64748b")
            current_z += level.height
        self.canvas.create_text(20, 20, text=f"FASADA — {direction}", anchor="nw", font=("Segoe UI", 14, "bold"), fill="#1f2937")
        self.canvas.create_text(20, 45, text=f"Omotač: {self.active_level.facade_finish or 'nije definisan'} · izolacija {self.active_level.insulation_thickness_m*1000:.0f} mm", anchor="nw", fill="#475569")


def main() -> None:
    CompleteBuildingWorkspaceApp().mainloop()


if __name__ == "__main__":
    main()
