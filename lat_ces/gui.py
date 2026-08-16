"""LAT-CES Windows desktop application.

Building-first GUI adapter. The floor plan is the primary workspace; analysis
and scientific domains are selected as operating modes around the same model.
"""
from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from lat_ces.application.service import analyze_config, export_report, load_config
from lat_ces.building.floor_plan import FloorPlan, Point2D, Segment2D, Wall


MODE_DESCRIPTIONS = {
    "Projektovanje": "Tlocrt, prostorije, zidovi i otvori",
    "Geometrija": "Visine, spratovi i 3D geometrija",
    "Instalacije": "HVAC, FluidNetwork, voda i električne instalacije",
    "Konstrukcija": "Opterećenja, statika i mehanika konstrukcija",
    "Simulacija": "Fluidika, termika, akustika i energija",
    "Provjera i izvještaj": "Verifikacija, sigurnost i izvještaji",
}


def build_default_floor_plan() -> FloorPlan:
    """Create a neutral starter plan; real projects will load their own model."""
    plan = FloorPlan(name="Novi objekat")
    width, depth = 12.0, 8.0
    walls = [
        ("Sjever", (0, 0, width, 0)),
        ("Jug", (0, depth, width, depth)),
        ("Zapad", (0, 0, 0, depth)),
        ("Istok", (width, 0, width, depth)),
        ("Pregrada 1", (7.0, 0, 7.0, 4.8)),
        ("Pregrada 2", (0.0, 4.8, 7.0, 4.8)),
    ]
    for name, (x1, y1, x2, y2) in walls:
        plan.add_wall(
            Wall(
                name=name,
                segment=Segment2D(Point2D(x1, y1), Point2D(x2, y2)),
                thickness=0.20,
            )
        )
    return plan


class LATCESApp(tk.Tk):
    """Building-first desktop shell around the canonical LAT-CES model."""

    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Building Model")
        self.geometry("1280x780")
        self.minsize(1050, 680)
        self.floor_plan = build_default_floor_plan()
        self.active_mode = tk.StringVar(value="Projektovanje")
        self.status_var = tk.StringVar(value="Spreman — tlocrt je početna radna površina")
        self.config_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.format_var = tk.StringVar(value="json")
        self._build_ui()
        self._draw_floor_plan()

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="LAT-CES", font=("Segoe UI", 21, "bold")).pack(side="left")
        ttk.Label(header, text="Building Model  /  Tlocrt", font=("Segoe UI", 11)).pack(
            side="left", padx=(14, 0), pady=(5, 0)
        )
        ttk.Button(header, text="Novi projekat", command=self.new_project).pack(side="right")
        ttk.Button(header, text="Otvori analizu…", command=self.browse_config).pack(side="right", padx=8)

        body = ttk.Frame(self, padding=(18, 0, 18, 12))
        body.pack(fill="both", expand=True)

        workspace = ttk.LabelFrame(body, text="Tlocrt", padding=8)
        workspace.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(
            workspace, background="white", highlightthickness=1, highlightbackground="#cfd4da"
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._draw_floor_plan())

        side = ttk.Frame(body, width=320)
        side.pack(side="left", fill="y", padx=(14, 0))
        side.pack_propagate(False)

        mode_box = ttk.LabelFrame(side, text="Režim rada", padding=10)
        mode_box.pack(fill="x")
        for mode in MODE_DESCRIPTIONS:
            ttk.Button(
                mode_box, text=mode, command=lambda value=mode: self.select_mode(value)
            ).pack(fill="x", pady=3)

        self.mode_title = ttk.Label(side, text="Projektovanje", font=("Segoe UI", 14, "bold"))
        self.mode_title.pack(anchor="w", pady=(18, 3))
        self.mode_desc = ttk.Label(side, text=MODE_DESCRIPTIONS["Projektovanje"], wraplength=280)
        self.mode_desc.pack(anchor="w")

        tools = ttk.LabelFrame(side, text="Radna svojstva", padding=10)
        tools.pack(fill="x", pady=(14, 0))
        ttk.Label(tools, text="Objekat").grid(row=0, column=0, sticky="w")
        ttk.Label(tools, text=self.floor_plan.name, font=("Segoe UI", 10, "bold")).grid(
            row=0, column=1, sticky="e"
        )
        ttk.Label(tools, text="Zidovi").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.wall_count_label = ttk.Label(tools, text=str(self.floor_plan.wall_count))
        self.wall_count_label.grid(row=1, column=1, sticky="e", pady=(6, 0))
        ttk.Label(tools, text="Nivo").grid(row=2, column=0, sticky="w", pady=(6, 0))
        ttk.Label(tools, text="Prizemlje").grid(row=2, column=1, sticky="e", pady=(6, 0))
        tools.columnconfigure(1, weight=1)

        action_box = ttk.LabelFrame(side, text="LAT-CES alati", padding=10)
        action_box.pack(fill="x", pady=(14, 0))
        ttk.Button(action_box, text="Scientific Analysis", command=self.open_analysis).pack(fill="x")
        ttk.Button(action_box, text="Provjeri tlocrt", command=self.validate_plan).pack(fill="x", pady=6)
        ttk.Button(action_box, text="Izvoz projekta", command=self.export_project).pack(fill="x")

        ttk.Label(
            side,
            text="Princip: jedan Building Model, više naučnih režima rada.",
            wraplength=280,
            foreground="#5f6368",
        ).pack(anchor="w", pady=(16, 0))
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x")

    def _draw_floor_plan(self) -> None:
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        margin = 70
        scale = min((width - 2 * margin) / 12.0, (height - 2 * margin) / 8.0)
        origin_x = (width - 12.0 * scale) / 2
        origin_y = (height - 8.0 * scale) / 2

        def xy(point: Point2D) -> tuple[float, float]:
            return origin_x + point.x * scale, origin_y + point.y * scale

        for x in range(13):
            px = origin_x + x * scale
            self.canvas.create_line(px, origin_y, px, origin_y + 8 * scale, fill="#edf0f2")
        for y in range(9):
            py = origin_y + y * scale
            self.canvas.create_line(origin_x, py, origin_x + 12 * scale, py, fill="#edf0f2")

        self.canvas.create_text(origin_x, origin_y - 26, text="12.00 m", anchor="w", fill="#5f6368")
        self.canvas.create_text(
            origin_x - 35, origin_y + 4 * scale, text="8.00 m", angle=90, fill="#5f6368"
        )

        for wall in self.floor_plan.walls.values():
            x1, y1 = xy(wall.segment.start)
            x2, y2 = xy(wall.segment.end)
            self.canvas.create_line(x1, y1, x2, y2, width=8, fill="#374151", capstyle=tk.BUTT)

        labels = (
            (3.5, 2.3, "Dnevni boravak / kuhinja"),
            (9.2, 2.3, "Soba"),
            (3.5, 6.2, "Ulaz / hodnik"),
        )
        for x, y, label in labels:
            self.canvas.create_text(
                origin_x + x * scale, origin_y + y * scale, text=label,
                fill="#4b5563", font=("Segoe UI", 11 if "Dnevni" in label else 10),
            )
        self.canvas.create_text(width - 20, 20, text="Sjever ↑", anchor="ne", fill="#5f6368")

    def select_mode(self, mode: str) -> None:
        self.active_mode.set(mode)
        self.mode_title.configure(text=mode)
        self.mode_desc.configure(text=MODE_DESCRIPTIONS[mode])
        self.status_var.set(f"Režim: {mode} — tlocrt ostaje centralni model")

    def new_project(self) -> None:
        self.floor_plan = build_default_floor_plan()
        self.wall_count_label.configure(text=str(self.floor_plan.wall_count))
        self.select_mode("Projektovanje")
        self._draw_floor_plan()

    def validate_plan(self) -> None:
        findings = self.floor_plan.validate()
        if findings:
            self.status_var.set(f"Tlocrt: {len(findings)} nalaza")
            messagebox.showwarning("Provjera tlocrta", "\n".join(findings))
            return
        self.status_var.set("Tlocrt je geometrijski validan")
        messagebox.showinfo("Provjera tlocrta", "Tlocrt je geometrijski validan.")

    def export_project(self) -> None:
        target = filedialog.asksaveasfilename(
            title="Sačuvaj Building Model",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"),),
            initialfile="building_model.json",
        )
        if not target:
            return
        payload = {
            "name": self.floor_plan.name,
            "plan_id": self.floor_plan.plan_id,
            "wall_count": self.floor_plan.wall_count,
            "gross_wall_length_m": self.floor_plan.gross_wall_length,
            "net_wall_length_m": self.floor_plan.net_wall_length,
        }
        Path(target).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status_var.set(f"Building Model izvezen: {target}")

    def browse_config(self) -> None:
        path = filedialog.askopenfilename(
            title="Select LAT-CES JSON configuration",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
        )
        if path:
            self.config_path.set(path)
            self.open_analysis()

    def open_analysis(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("LAT-CES — Scientific Analysis")
        dialog.geometry("860x620")
        dialog.transient(self)
        cfg = ttk.Frame(dialog, padding=14)
        cfg.pack(fill="x")
        path_var = tk.StringVar(value=self.config_path.get())
        output_var = tk.StringVar(value=self.output_path.get())

        ttk.Label(cfg, text="JSON konfiguracija:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cfg, textvariable=path_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(
            cfg,
            text="Browse…",
            command=lambda: path_var.set(
                filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
            ),
        ).grid(row=0, column=2)
        ttk.Label(cfg, text="Format:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Combobox(
            cfg, textvariable=self.format_var, values=("json", "md"), state="readonly", width=10
        ).grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))
        ttk.Label(cfg, text="Output:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(cfg, textvariable=output_var).grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=8, pady=(8, 0)
        )
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
                report, exporter = analyze_config(
                    config,
                    project_default="LAT-CES Desktop Analysis",
                    plenum_default="PLENUM-GUI-01",
                    equation_default="Custom equation",
                )
                fmt = self.format_var.get()
                output = Path(output_var.get().strip() or config_file.with_name(f"latces_report.{fmt}"))
                export_report(exporter, output, fmt)
                content = json.loads(exporter.to_json()) if fmt == "json" else exporter.to_markdown()
                display = json.dumps(content, indent=2, ensure_ascii=False) if isinstance(content, dict) else content
                result.delete("1.0", "end")
                result.insert("1.0", f"Status: [{report.status.value}]\nReport: {output}\n\n{display}")
                self.status_var.set(f"Scientific Analysis: {report.status.value}")
            except Exception as exc:
                result.delete("1.0", "end")
                result.insert("1.0", f"Analysis failed:\n\n{exc}")
                messagebox.showerror("LAT-CES analysis error", str(exc), parent=dialog)

        ttk.Button(dialog, text="Run Analysis", command=run).pack(pady=(0, 14))


def main() -> None:
    LATCESApp().mainloop()


if __name__ == "__main__":
    main()
