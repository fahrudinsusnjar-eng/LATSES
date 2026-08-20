"""Master desktop shell over the canonical CompleteBuildingWorkspaceApp."""
from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk

from lat_ces.building.quantity_takeoff import calculate_quantity_takeoff
from lat_ces.building.reference_house_project import build_reference_house_workflow
from lat_ces.gui_complete import CompleteBuildingWorkspaceApp
from lat_ces.gui_theme import apply_latces_theme
from lat_ces.materials.building_catalog import BuildingMaterialCatalog


class MasterBuildingWorkspaceApp(CompleteBuildingWorkspaceApp):
    """Single desktop workspace using one canonical BuildingModel."""

    def __init__(self) -> None:
        super().__init__()
        apply_latces_theme(self)
        self.catalog = BuildingMaterialCatalog.default()
        self._master_command_panel = None
        self._master_metrics_panel = None
        self._master_metric_vars: dict[str, tk.StringVar] = {}
        self._level_room_text = None
        self._install_master_layout()
        self._install_catalog_tab()
        self._install_window_adaptation()
        self._refresh_master_metrics()
        self._refresh_level_selector()

    # ---------- screen adaptation ----------
    def _install_window_adaptation(self) -> None:
        self.resizable(True, True)
        self._fullscreen = False
        self._resize_after_id = None
        self.bind("<F11>", lambda _e: self._toggle_fullscreen())
        self.bind("<Escape>", lambda _e: self._exit_fullscreen())
        self.bind("<Control-Key-0>", lambda _e: self._fit_to_screen())
        self.bind("<Configure>", self._on_window_configure, add="+")
        self.after(120, self._fit_to_screen_if_needed)

    def _fit_to_screen_if_needed(self) -> None:
        if self.winfo_screenwidth() < 1450 or self.winfo_screenheight() < 920:
            self._fit_to_screen()

    def _fit_to_screen(self) -> None:
        if self._fullscreen:
            return
        screen_w = max(self.winfo_screenwidth(), 800)
        screen_h = max(self.winfo_screenheight(), 600)
        width = min(1600, screen_w - 24)
        height = min(980, screen_h - 56)
        if sys.platform.startswith("win"):
            try:
                self.state("zoomed")
                return
            except tk.TclError:
                pass
        self.geometry(f"{width}x{height}+{max((screen_w - width)//2, 0)}+{max((screen_h - height)//2, 0)}")

    def _toggle_fullscreen(self) -> None:
        self._fullscreen = not self._fullscreen
        try:
            self.attributes("-fullscreen", self._fullscreen)
        except tk.TclError:
            self._fullscreen = False

    def _exit_fullscreen(self) -> None:
        if not self._fullscreen:
            return
        self._fullscreen = False
        try:
            self.attributes("-fullscreen", False)
        except tk.TclError:
            pass
        self._fit_to_screen()

    def _on_window_configure(self, _event: tk.Event) -> None:
        if self._resize_after_id is not None:
            try:
                self.after_cancel(self._resize_after_id)
            except tk.TclError:
                pass
        self._resize_after_id = self.after(150, self._refresh_adaptive_layout)

    def _refresh_adaptive_layout(self) -> None:
        self._resize_after_id = None
        if hasattr(self, "_master_command_canvas"):
            self._master_command_canvas.configure(scrollregion=self._master_command_canvas.bbox("all"))

    # ---------- master layout ----------
    def _install_master_layout(self) -> None:
        """Keep the engineering viewport central and put tools on the right.

        The legacy top notebook and metric strip are deliberately not packed into
        the master shell.  The underlying canonical workspace remains available
        to the existing methods; the master shell exposes those actions through
        the vertical tool rail instead of consuming the drawing viewport.
        """
        self._install_command_panel()
        if hasattr(self, "complete_tabs"):
            self.complete_tabs.pack_forget()

    def _existing_body(self):
        widgets = list(self.winfo_children())
        for widget in widgets:
            if widget is not self._master_command_panel and widget is not self._master_metrics_panel and widget is not getattr(self, "complete_tabs", None):
                return widget
        return None

    def _install_command_panel(self) -> None:
        shell = ttk.LabelFrame(self, text="ALATI", padding=4)
        shell.pack(side="right", fill="y", padx=(8, 10), pady=10)
        shell.configure(width=235)
        shell.pack_propagate(False)
        self._master_command_panel = shell

        canvas = tk.Canvas(shell, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        self._master_command_canvas = canvas
        inner.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=e.width))
        canvas.bind_all("<MouseWheel>", self._master_mousewheel, add="+")

        ttk.Label(inner, text="BUILDING MODEL", font=("Segoe UI", 10, "bold")).pack(fill="x", pady=(2, 8))
        ttk.Label(inner, text="Aktivni model").pack(anchor="w")
        self.model_selector_var = tk.StringVar(value=self.workflow.model.name)
        self.model_selector = ttk.Combobox(inner, textvariable=self.model_selector_var, state="readonly", values=(self.workflow.model.name,))
        self.model_selector.pack(fill="x", pady=(2, 6))
        self.model_selector.bind("<<ComboboxSelected>>", self._select_model)

        ttk.Button(inner, text="Referentna kuća P+2", style="LATCES.Primary.TButton", command=self._load_reference_house).pack(fill="x", pady=(2, 8))
        ttk.Button(inner, text="Prilagodi ekranu  (Ctrl+0)", command=self._fit_to_screen).pack(fill="x", pady=2)
        ttk.Button(inner, text="Fullscreen  (F11)", command=self._toggle_fullscreen).pack(fill="x", pady=2)

        ttk.Label(inner, text="Aktivna etaža", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 3))
        self.level_selector_var = tk.StringVar()
        self.level_selector = ttk.Combobox(inner, textvariable=self.level_selector_var, state="readonly")
        self.level_selector.pack(fill="x")
        self.level_selector.bind("<<ComboboxSelected>>", self._select_active_level)
        self._level_room_text = tk.Text(inner, height=8, width=28, wrap="word", state="disabled")
        self._level_room_text.pack(fill="x", pady=(6, 8))

        commands = (
            ("Model", lambda: self._master_goto_step(1)),
            ("Tlocrt", lambda: self._master_goto_step(3)),
            ("Presjek", lambda: self._master_goto_step(4)),
            ("3D", lambda: self._master_goto_step(5)),
            ("Provjera", self.validate_model),
            ("Izvještaj / proračun", self._calculate_building_report),
        )
        for label, callback in commands:
            ttk.Button(inner, text=label, style="LATCES.Secondary.TButton", command=callback).pack(fill="x", pady=2)

        ttk.Separator(inner).pack(fill="x", pady=8)
        ttk.Button(inner, text="Osvježi matematiku", style="LATCES.Primary.TButton", command=self._refresh_master_metrics).pack(fill="x")
        ttk.Label(inner, text="Svaka etaža je zaseban aktivni Level u istom BuildingWorkflow projektu. Promjena etaže ne pravi novi projekat.", wraplength=205, foreground="#475569").pack(fill="x", pady=(10, 6))

    def _master_mousewheel(self, event: tk.Event) -> None:
        if not hasattr(self, "_master_command_canvas"):
            return
        self._master_command_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _install_metrics_panel(self) -> None:
        panel = ttk.LabelFrame(self, text="Matematika / Engineering", padding=8)
        panel.pack(side="top", fill="x", padx=10, pady=(10, 4))
        self._master_metrics_panel = panel
        metrics = (("area", "Površina"), ("volume", "Zapremina"), ("wall", "Dužina zidova"), ("roof", "Krov — tlocrt"), ("levels", "Etaže"), ("rooms", "Prostorije"), ("elements", "Elementi"), ("status", "Status"))
        for index, (key, label) in enumerate(metrics):
            panel.columnconfigure(index, weight=1)
            cell = ttk.Frame(panel); cell.grid(row=0, column=index, sticky="ew", padx=3)
            ttk.Label(cell, text=label).pack(anchor="w")
            var = tk.StringVar(value="—"); self._master_metric_vars[key] = var
            ttk.Label(cell, textvariable=var, font=("Segoe UI", 10, "bold")).pack(anchor="w")

    # ---------- model / level switching ----------
    def _select_model(self, _event=None):
        if self.model_selector_var.get().strip() == self.workflow.model.name:
            self._refresh_master_metrics()

    def _load_reference_house(self) -> None:
        self.workflow = build_reference_house_workflow()
        self.model_selector_var.set(self.workflow.model.name)
        self.status_var.set("Referentna kuća P+2 učitana u isti BuildingWorkflow projekat")
        self._refresh_level_selector()
        self._refresh_master_metrics()
        self.refresh_view()

    def _refresh_level_selector(self) -> None:
        levels = list(self.workflow.model.levels.values())
        values = [level.name for level in levels]
        if hasattr(self, "level_selector"):
            self.level_selector["values"] = values
            if self.workflow.active_level_id in self.workflow.model.levels:
                self.level_selector_var.set(self.workflow.model.levels[self.workflow.active_level_id].name)
        if hasattr(self, "level_box"):
            self.level_box["values"] = values
            if values and self.workflow.active_level_id in self.workflow.model.levels:
                self.level_var.set(self.workflow.model.levels[self.workflow.active_level_id].name)
        self._refresh_level_context()

    def _select_active_level(self, _event=None):
        wanted = self.level_selector_var.get().strip()
        for level in self.workflow.model.levels.values():
            if level.name == wanted:
                self.workflow.set_active_level(level.level_id)
                if hasattr(self, "level_var"):
                    self.level_var.set(level.name)
                self._refresh_level_context()
                self.refresh_view()
                return

    def select_level_from_combo(self, _event=None):
        super().select_level_from_combo(_event)
        self._refresh_level_selector()

    def _refresh_level_context(self) -> None:
        if self._level_room_text is None:
            return
        level = self.workflow.active_level
        lines = [f"{level.name}", f"Gabarit: {level.length_m:.2f} × {level.width_m:.2f} m", f"Visina: {level.height:.2f} m", f"Stalno: {level.dead_load_kpa:.2f} kPa", f"Korisno: {level.live_load_kpa:.2f} kPa"]
        project = self.workflow.project_spec
        if project is not None:
            item = next((x for x in project.levels if x.name == level.name), None)
            if item is not None and item.rooms:
                lines.append("Prostorije referentne kuće:")
                lines.extend(f"• {room.name} — {room.area_m2:.1f} m²" for room in item.rooms)
        self._level_room_text.configure(state="normal")
        self._level_room_text.delete("1.0", "end")
        self._level_room_text.insert("1.0", "\n".join(lines))
        self._level_room_text.configure(state="disabled")

    def _master_goto_step(self, step: int):
        self.view_step.set(step)
        self.goto_step()
        self._refresh_master_metrics()

    def _select_complete_tab(self, index: int):
        if hasattr(self, "complete_tabs") and index < len(self.complete_tabs.tabs()):
            self.complete_tabs.select(index)
            self._refresh_master_metrics()

    def _show_catalog_tab(self):
        if hasattr(self, "complete_tabs") and self.complete_tabs.tabs():
            self.complete_tabs.select(self.complete_tabs.tabs()[-1])

    # ---------- engineering metrics ----------
    def _refresh_master_metrics(self):
        model = self.workflow.model
        qto = calculate_quantity_takeoff(model)
        self._master_metric_vars["area"].set(f"{qto.floor_area_m2:.2f} m²")
        self._master_metric_vars["volume"].set(f"{qto.volume_m3:.2f} m³")
        self._master_metric_vars["wall"].set(f"{qto.wall_length_m:.2f} m")
        self._master_metric_vars["roof"].set(f"{qto.roof_plan_area_m2:.2f} m²")
        self._master_metric_vars["levels"].set(str(len(model.levels)))
        rooms = model.room_count
        if rooms == 0 and self.workflow.project_spec is not None:
            rooms = sum(level.room_count for level in self.workflow.project_spec.levels)
        self._master_metric_vars["rooms"].set(str(rooms))
        self._master_metric_vars["elements"].set(str(model.element_count))
        findings = model.validate()
        self._master_metric_vars["status"].set("PASS" if not findings else f"CHECK ({len(findings)})")
        self._refresh_level_context()

    def refresh_view(self):
        super().refresh_view()
        if hasattr(self, "_master_metric_vars"):
            self._refresh_level_selector()
            self._refresh_master_metrics()

    # ---------- catalog ----------
    def _install_catalog_tab(self):
        tab = ttk.Frame(self.complete_tabs, padding=10)
        self.complete_tabs.add(tab, text="Katalog")
        toolbar = ttk.Frame(tab); toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(toolbar, text="Pretraga").pack(side="left")
        self.catalog_search_var = tk.StringVar()
        entry = ttk.Entry(toolbar, textvariable=self.catalog_search_var, width=38); entry.pack(side="left", padx=6)
        entry.bind("<KeyRelease>", lambda _event: self._refresh_catalog_view())
        ttk.Button(toolbar, text="Osvježi", style="LATCES.Secondary.TButton", command=self._refresh_catalog_view).pack(side="left")
        body = ttk.Frame(tab); body.pack(fill="both", expand=True)
        self.catalog_list = tk.Listbox(body, height=16, activestyle="none"); self.catalog_list.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.catalog_list.yview); scrollbar.pack(side="left", fill="y")
        self.catalog_list.configure(yscrollcommand=scrollbar.set)
        right = ttk.LabelFrame(body, text="Odabrani element / materijal", padding=10); right.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.catalog_detail = tk.Text(right, height=14, wrap="word"); self.catalog_detail.pack(fill="both", expand=True); self.catalog_detail.configure(state="disabled")
        self.catalog_list.bind("<<ListboxSelect>>", self._show_catalog_selection)
        status = ttk.Label(tab, text="Parametarski katalog — komercijalne dimenzije i projektne vrijednosti moraju biti verificirane.", style="LATCES.Warning.TLabel", wraplength=900)
        status.pack(fill="x", pady=(8, 0))
        self._refresh_catalog_view()

    def _refresh_catalog_view(self):
        items = self.catalog.search(self.catalog_search_var.get())
        self.catalog_visible_items = items
        self.catalog_list.delete(0, "end")
        for item in items:
            marker = " · dimenzije obavezne" if item.requires_dimensions else ""
            self.catalog_list.insert("end", f"{item.name} [{item.unit}]{marker}")
        self._set_catalog_detail("Odaberi stavku.\n\nKategorije su parametarske: upiši stvarne mjere/proizvod nakon odabira.\nNormativni proračun ne koristi katalog kao zamjenu za projektne vrijednosti.")

    def _show_catalog_selection(self, _event=None):
        selection = self.catalog_list.curselection()
        if not selection:
            return
        item = self.catalog_visible_items[selection[0]]
        text = (f"ID: {item.item_id}\n" f"Naziv: {item.name}\n" f"Jedinica obračuna: {item.unit}\n" f"Dimenzije potrebne: {'DA' if item.requires_dimensions else 'NE'}\n\n" "Proračunski parametri nisu automatski izmišljeni. Za stvarni proizvod unesi ili uvezi verificirane podatke: dimenzije, gustinu, λ/U, čvrstoće, masu i proizvođača.")
        if item.item_id == "glazing":
            text += "\n\nStakla: " + ", ".join(option.option_id for option in self.catalog.glazing_options)
        self._set_catalog_detail(text)

    def _set_catalog_detail(self, value: str):
        self.catalog_detail.configure(state="normal")
        self.catalog_detail.delete("1.0", "end")
        self.catalog_detail.insert("1.0", value)
        self.catalog_detail.configure(state="disabled")


def main() -> None:
    MasterBuildingWorkspaceApp().mainloop()


if __name__ == "__main__":
    main()
