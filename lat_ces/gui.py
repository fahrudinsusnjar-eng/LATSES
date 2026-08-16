"""LAT-CES Windows desktop application.

A thin GUI over the canonical scientific CLI functionality. The command-line
interface remains available; this module provides the normal double-click
Windows application experience requested by users.
"""
from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from lat_ces.scientific.analysis.plenum import PlenumAnalysisEngine
from lat_ces.scientific.cli import _parse_quantity_dict
from lat_ces.scientific.reports.exporter import SKOReportExporter


class LATCESApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES Scientific Engineering")
        self.geometry("900x620")
        self.minsize(760, 520)
        self.config_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.format_var = tk.StringVar(value="json")
        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="LAT-CES Scientific Engineering", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(root, text="Plenum / fluid safety analysis", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 16))

        cfg = ttk.LabelFrame(root, text="Analysis configuration", padding=12)
        cfg.pack(fill="x")
        ttk.Label(cfg, text="JSON configuration:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cfg, textvariable=self.config_path).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(cfg, text="Browse…", command=self.browse_config).grid(row=0, column=2)
        cfg.columnconfigure(1, weight=1)

        out = ttk.LabelFrame(root, text="Output", padding=12)
        out.pack(fill="x", pady=12)
        ttk.Label(out, text="Format:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(out, textvariable=self.format_var, values=("json", "md"), state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=8)
        ttk.Label(out, text="Output file (optional):").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(out, textvariable=self.output_path).grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=(8, 0))
        out.columnconfigure(1, weight=1)

        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=(4, 10))
        ttk.Button(actions, text="Run Analysis", command=self.run_analysis).pack(side="left")
        ttk.Button(actions, text="Open Output Folder", command=self.open_output_folder).pack(side="left", padx=8)
        ttk.Button(actions, text="Exit", command=self.destroy).pack(side="right")

        result = ttk.LabelFrame(root, text="Result", padding=10)
        result.pack(fill="both", expand=True)
        self.text = tk.Text(result, wrap="word", font=("Consolas", 10))
        self.text.pack(fill="both", expand=True)
        self.text.configure(state="disabled")

        ttk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x", pady=(10, 0))

    def browse_config(self) -> None:
        path = filedialog.askopenfilename(title="Select LAT-CES JSON configuration", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if path:
            self.config_path.set(path)
            if not self.output_path.get():
                self.output_path.set(str(Path(path).with_name("latces_report.json")))

    def open_output_folder(self) -> None:
        path = self.output_path.get()
        folder = str(Path(path).resolve().parent) if path else str(Path.home())
        try:
            import os
            os.startfile(folder)
        except Exception as exc:
            messagebox.showerror("LAT-CES", f"Could not open folder:\n{exc}")

    def _show(self, text: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
        self.text.configure(state="disabled")

    def run_analysis(self) -> None:
        config_file = Path(self.config_path.get().strip())
        if not config_file.exists():
            messagebox.showwarning("LAT-CES", "Select a valid JSON configuration file first.")
            return
        try:
            with config_file.open("r", encoding="utf-8") as fh:
                config = json.load(fh)
            inputs = {name: _parse_quantity_dict(q) for name, q in config.get("inputs", {}).items()}
            calculated_q = _parse_quantity_dict(config["calculated_value"])
            limit_q = _parse_quantity_dict(config["limit_value"])
            report = PlenumAnalysisEngine.evaluate_limit(
                calculated=calculated_q,
                limit=limit_q,
                coverage_factor=float(config.get("coverage_factor", 2.0)),
            )
            exporter = SKOReportExporter(
                project_name=config.get("project_name", "LAT-CES Desktop Analysis"),
                engineer_name=config.get("engineer_name", "Engineer"),
                plenum_id=config.get("plenum_id", "PLENUM-GUI-01"),
                safety_report=report,
                inputs=inputs,
                equation_name=config.get("equation_name", "Custom equation"),
            )
            fmt = self.format_var.get()
            output = Path(self.output_path.get().strip() or config_file.with_name(f"latces_report.{fmt}"))
            output.parent.mkdir(parents=True, exist_ok=True)
            content = exporter.to_json() if fmt == "json" else exporter.to_markdown()
            output.write_text(content, encoding="utf-8")
            self._show(
                f"Analysis completed successfully.\n\nStatus: [{report.status.value}]\n\n"
                f"Report: {output}\n\n{content}"
            )
            self.status_var.set(f"Completed — {output}")
        except Exception as exc:
            self.status_var.set("Analysis failed")
            self._show(f"Analysis failed:\n\n{exc}")
            messagebox.showerror("LAT-CES analysis error", str(exc))


def main() -> None:
    LATCESApp().mainloop()


if __name__ == "__main__":
    main()
