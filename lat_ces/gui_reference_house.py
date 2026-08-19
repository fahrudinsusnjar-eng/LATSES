"""Interactive LAT-CES reference-house showroom.

This is a deterministic demonstration surface, not a normative design tool.
It is intentionally independent from the drafting editor so the demo can be
used as a regression/golden-model showcase without changing project state.
"""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

from lat_ces.reference_house import ReferenceHouse


class ReferenceHouseShowroom(tk.Tk):
    """Responsive fullscreen showroom with 360° building and room navigation."""

    BG = "#F5F7FA"
    PANEL = "#FFFFFF"
    TEXT = "#0F172A"
    MUTED = "#475569"
    BLUE = "#2563EB"
    TEAL = "#0EA5A4"
    GREEN = "#16A34A"
    AMBER = "#D97706"
    RED = "#DC2626"

    def __init__(self) -> None:
        super().__init__()
        self.title("LAT-CES — Referentna kuća / 360° Engineering Showroom")
        self.geometry("1600x900")
        self.minsize(1050, 650)
        self.configure(bg=self.BG)
        self.house = ReferenceHouse.default()
        self.angle = 35.0
        self.font_scale = 1.0
        self.overlay = "all"
        self.fullscreen = False
        self.room_id = self.house.conditioned_rooms[0]["id"]
        self._style()
        self._build()
        self.bind("<F11>", lambda _e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda _e: self._exit_fullscreen())
        self.bind("<Configure>", lambda _e: self._responsive_refresh())
        self.after(80, self._draw)

    def _style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Sub.TLabel", foreground=self.MUTED, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(10, 7))
        style.configure("Primary.TButton", foreground="white", background=self.BLUE)
        style.map("Primary.TButton", background=[("active", self.TEAL)])
        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10, "bold"))

    def _build(self) -> None:
        top = ttk.Frame(self, padding=(18, 12)); top.pack(fill="x")
        ttk.Label(top, text="LAT-CES · REFERENTNA KUĆA", style="Title.TLabel").pack(side="left")
        ttk.Label(top, text="P+2 · dvovodni krov · MEP · energija · količine", style="Sub.TLabel").pack(side="left", padx=18)
        ttk.Button(top, text="A−", command=lambda: self._font(-0.1)).pack(side="right", padx=2)
        ttk.Button(top, text="A+", command=lambda: self._font(0.1)).pack(side="right", padx=2)
        ttk.Button(top, text="FULL SCREEN", style="Primary.TButton", command=self.toggle_fullscreen).pack(side="right", padx=6)

        self.tabs = ttk.Notebook(self); self.tabs.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self.view_tab = ttk.Frame(self.tabs, padding=8); self.house_tab = ttk.Frame(self.tabs, padding=8); self.calc_tab = ttk.Frame(self.tabs, padding=8); self.mep_tab = ttk.Frame(self.tabs, padding=8)
        self.tabs.add(self.view_tab, text="Kuća 360°"); self.tabs.add(self.house_tab, text="Ulazak u prostorije"); self.tabs.add(self.calc_tab, text="Proračuni"); self.tabs.add(self.mep_tab, text="MEP / osjećaj prostora")

        self.canvas = tk.Canvas(self.view_tab, bg="#E9EEF5", highlightthickness=0); self.canvas.pack(side="left", fill="both", expand=True)
        controls = ttk.Frame(self.view_tab, width=250, padding=10); controls.pack(side="right", fill="y")
        ttk.Label(controls, text="360° model", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Button(controls, text="↶ Rotiraj lijevo", command=lambda: self.rotate(-15)).pack(fill="x", pady=2)
        ttk.Button(controls, text="↷ Rotiraj desno", command=lambda: self.rotate(15)).pack(fill="x", pady=2)
        ttk.Button(controls, text="Uđi u kuću", style="Primary.TButton", command=lambda: self.tabs.select(self.house_tab)).pack(fill="x", pady=10)
        ttk.Label(controls, text="Slojevi prikaza").pack(anchor="w")
        for text, key in (("Sve", "all"), ("Konstrukcija", "structure"), ("Grijanje", "heating"), ("Ventilacija", "ventilation"), ("Hlađenje", "cooling"), ("Svjetlo", "light")):
            ttk.Button(controls, text=text, command=lambda k=key: self.set_overlay(k)).pack(fill="x", pady=1)
        self.view_status = ttk.Label(controls, text="", wraplength=220, style="Sub.TLabel"); self.view_status.pack(anchor="w", pady=10)

        self._build_rooms(); self._build_calc(); self._build_mep()

    def _build_rooms(self) -> None:
        left = ttk.Frame(self.house_tab); left.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(left, text="Etaža / prostorija", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.room_box = ttk.Combobox(left, state="readonly", width=28, values=[f"{r['id']} · {r['name']}" for r in self.house.conditioned_rooms])
        self.room_box.pack(fill="x", pady=8); self.room_box.current(0); self.room_box.bind("<<ComboboxSelected>>", self._room_changed)
        ttk.Button(left, text="Prethodna", command=lambda: self._step_room(-1)).pack(fill="x", pady=2)
        ttk.Button(left, text="Sljedeća", command=lambda: self._step_room(1)).pack(fill="x", pady=2)
        ttk.Label(left, text="Namještaj: sofa · sto · stolice · krevet · ormar · zavjese · tepih · biljke", wraplength=230, style="Sub.TLabel").pack(anchor="w", pady=12)
        self.room_info = ttk.Label(left, text="", wraplength=240); self.room_info.pack(anchor="w")
        self.room_canvas = tk.Canvas(self.house_tab, bg="#F8FAFC", highlightthickness=0); self.room_canvas.pack(side="left", fill="both", expand=True)

    def _build_calc(self) -> None:
        self.calc_text = tk.Text(self.calc_tab, bg="#0B1220", fg="#DCE7F7", relief="flat", font=("Consolas", 11), padx=16, pady=16)
        self.calc_text.pack(fill="both", expand=True)
        self._set_calc_text()

    def _build_mep(self) -> None:
        frame = ttk.Frame(self.mep_tab); frame.pack(fill="x")
        ttk.Button(frame, text="Grijanje", command=lambda: self.set_overlay("heating")).pack(side="left", padx=2)
        ttk.Button(frame, text="Ventilacija", command=lambda: self.set_overlay("ventilation")).pack(side="left", padx=2)
        ttk.Button(frame, text="Hlađenje", command=lambda: self.set_overlay("cooling")).pack(side="left", padx=2)
        ttk.Button(frame, text="Svjetlo", command=lambda: self.set_overlay("light")).pack(side="left", padx=2)
        self.mep_text = tk.Text(self.mep_tab, height=20, bg="#FFFFFF", fg=self.TEXT, relief="flat", font=("Consolas", 11), padx=14, pady=14)
        self.mep_text.pack(fill="both", expand=True, pady=8)
        self._set_mep_text()

    def _set_calc_text(self) -> None:
        s = self.house.summary()
        lines = [
            "LAT-CES REFERENTNA KUĆA — DEMO PRORAČUN",
            "=" * 54,
            f"Površina:                 {s.floor_area_m2:9.1f} m²",
            f"Volumen:                  {s.volume_m3:9.1f} m³",
            f"Krovna površina:         {s.roof_area_m2:9.1f} m²",
            f"Vanjski zidovi:          {s.wall_area_m2:9.1f} m²",
            f"Zidni blokovi (procjena): {s.blocks:8.0f} kom",
            f"Beton ploča (procjena):   {s.slab_concrete_m3:8.2f} m³",
            "",
            f"Toplotno opterećenje:     {s.heating_load_w/1000:8.2f} kW",
            f"Ukupan maseni protok:     {s.heating_mass_flow_kg_s:8.4f} kg/s",
            f"Ventilacija @ 0.85 ACH:   {s.ventilation_m3_h:8.1f} m³/h",
            f"Procjena rasvjete:        {s.lighting_w:8.1f} W",
            "",
            "Napomena: demo parametri su projektni ulazi, ne normativno odobrenje.",
            "Konačan proračun koristi odabrane norme, nacionalne dodatke i verificirane materijale."
        ]
        self.calc_text.insert("1.0", "\n".join(lines)); self.calc_text.configure(state="disabled")

    def _set_mep_text(self) -> None:
        s = self.house.summary(); circuits = self.house.heating_circuits()
        lines = [
            "MEP / KOMFORNI PREGLED",
            f"Grijanje ukupno: {s.heating_load_w/1000:.2f} kW",
            f"Ventilacija: {s.ventilation_m3_h:.0f} m³/h @ 0.85 ACH",
            f"Projektna brzina zraka u završnim elementima: {self.house.data['ventilation']['design_velocity_m_s']:.2f} m/s",
            "",
            "Krugovi grijanja:"
        ]
        for c in circuits:
            lines.append(f"- {c.circuit_id}: {c.type}, {c.heat_load_w/1000:.2f} kW, {c.mass_flow_kg_s:.4f} kg/s, ΔT={c.delta_t_k:.1f} K")
        lines += [
            "", "Osjećaj strujanja:",
            "< 0.10 m/s  → vrlo blago;", "0.10–0.20 m/s → umjereno;", "> 0.20 m/s → povećan rizik osjećaja propuha.",
            "Ovo su podesivi komforni pokazatelji, ne medicinski/normativni pragovi.",
            "", "Priroda / dnevno svjetlo:",
            "Model poredi ciljane nivoe osvjetljenja i brzinu zraka sa konfigurabilnim prirodnim/komfornim referencama."
        ]
        self.mep_text.insert("1.0", "\n".join(lines)); self.mep_text.configure(state="disabled")

    def _draw(self) -> None:
        self.canvas.delete("all")
        w = max(self.canvas.winfo_width(), 700); h = max(self.canvas.winfo_height(), 500)
        cx, cy = w * 0.48, h * 0.53; scale = min(w / 24.0, h / 18.0)
        angle = math.radians(self.angle)
        lx, wy = 12 * scale, 10 * scale
        # pseudo-axonometric envelope for deterministic 360° interaction
        front = (math.cos(angle), math.sin(angle)); side = (-math.sin(angle), math.cos(angle))
        levels_h = 2.8 * 3 * scale * 0.45
        points = []
        for x, y in [(-lx/2,-wy/2),(lx/2,-wy/2),(lx/2,wy/2),(-lx/2,wy/2)]:
            sx = cx + x*front[0] + y*side[0]; sy = cy + x*front[1] + y*side[1]
            points.append((sx, sy))
        roof_peak = levels_h * 0.42
        roof = [(points[3][0],points[3][1]-levels_h),(points[2][0],points[2][1]-levels_h),(cx, min(points[0][1],points[1][1])-levels_h-roof_peak)]
        for i, col in enumerate(("#D6DEE9", "#C7D2E0", "#B7C6D8")):
            off = i * 5
            poly = [(x, y-i*4) for x,y in points]
            self.canvas.create_polygon(poly, fill=col, outline="#64748B", width=2)
        if self.overlay in {"heating", "all"}:
            for y in range(0, 5):
                yy = cy - y*34
                self.canvas.create_line(cx-lx*0.28, yy, cx+lx*0.28, yy+12, fill="#DC2626", width=3)
        if self.overlay in {"ventilation", "all"}:
            for dx in (-100, -25, 50, 125):
                self.canvas.create_line(cx+dx, cy, cx+dx+35, cy-25, arrow="last", fill="#0EA5A4", width=2)
        if self.overlay in {"cooling", "all"}:
            self.canvas.create_oval(cx-90, cy-60, cx-40, cy-10, outline="#2563EB", width=3)
            self.canvas.create_text(cx-65, cy-35, text="18/21°C", fill="#2563EB", font=("Segoe UI", 9, "bold"))
        if self.overlay in {"light", "all"}:
            for dx in (-90, 0, 90):
                self.canvas.create_oval(cx+dx-8, cy-150, cx+dx+8, cy-134, fill="#F59E0B", outline="")
        self.canvas.create_polygon(*roof, fill="#7C8798", outline="#374151", width=3)
        self.canvas.create_text(20, 20, text=f"REFERENTNA KUĆA · 360° · {self.angle:.0f}°", anchor="nw", fill=self.TEXT, font=("Segoe UI", int(14*self.font_scale), "bold"))
        self.canvas.create_text(20, 48, text="Prikaz je demonstracijski; stvarni solveri rade iz BuildingModel podataka.", anchor="nw", fill=self.MUTED, font=("Segoe UI", int(10*self.font_scale)))
        self.view_status.configure(text=f"Sloj: {self.overlay}\nP+2 · dvovodni krov\nToplotno: {self.house.summary().heating_load_w/1000:.2f} kW\nVentilacija: {self.house.summary().ventilation_m3_h:.0f} m³/h")

    def _draw_room(self) -> None:
        self.room_canvas.delete("all")
        room = next(r for r in self.house.conditioned_rooms if r["id"] == self.room_id)
        w = max(self.room_canvas.winfo_width(), 650); h = max(self.room_canvas.winfo_height(), 500)
        pad = 70; x0, y0 = pad, 80; x1, y1 = w-pad, h-pad
        self.room_canvas.create_rectangle(x0, y0, x1, y1, fill="#F9F7F1", outline="#64748B", width=3)
        # furniture primitives
        self.room_canvas.create_rectangle(x0+70, y0+70, x0+260, y0+150, fill="#B88A63", outline="#6B4F3A")
        self.room_canvas.create_rectangle(x1-280, y1-130, x1-80, y1-55, fill="#64748B", outline="#334155")
        self.room_canvas.create_oval(x0+300, y0+90, x0+430, y0+220, fill="#A8D5BA", outline="#4F7C62")
        self.room_canvas.create_rectangle(x1-110, y0+55, x1-70, y0+220, fill="#D7C3A5", outline="#8B7355")
        # MEP overlays
        self.room_canvas.create_line(x0+50, y1-85, x1-60, y1-85, fill="#DC2626", width=4)
        self.room_canvas.create_line(x0+50, y1-105, x1-60, y1-105, fill="#2563EB", width=3)
        self.room_canvas.create_line((x0+x1)/2, y0+35, (x0+x1)/2, y1-30, arrow="last", fill="#0EA5A4", width=3)
        self.room_canvas.create_text(x0+18, y0+18, text=room["name"], anchor="nw", fill=self.TEXT, font=("Segoe UI", 16, "bold"))
        self.room_canvas.create_text(x0+18, y0+43, text=f"{room['area_m2']:.1f} m² · {room['floor_finish']} · {room['orientation']}", anchor="nw", fill=self.MUTED)
        self.room_canvas.create_text(x0+55, y1-65, text="TOPLA", fill="#B91C1C", font=("Segoe UI", 9, "bold"))
        self.room_canvas.create_text(x0+55, y1-108, text="HLADNA", fill="#1D4ED8", font=("Segoe UI", 9, "bold"))
        self.room_canvas.create_text((x0+x1)/2+10, y0+40, text="DOVOD / IZVOD ZRAKA", fill="#0F766E", font=("Segoe UI", 9, "bold"))
        self.room_info.configure(text=f"Etaža: {next(l['name'] for l in self.house.levels if room['id'] in [x['id'] for x in l['rooms']])}\nPovršina: {room['area_m2']:.1f} m²\nPod: {room['floor_finish']}\nOrijentacija: {room['orientation']}\nNamještaj: izložbeni set\nZavjese: prirodna tkanina\nMEP: podno/radijator + ventilacija")

    def rotate(self, amount: float) -> None:
        self.angle = (self.angle + amount) % 360; self._draw()

    def set_overlay(self, value: str) -> None:
        self.overlay = value; self.tabs.select(self.view_tab); self._draw()

    def _room_changed(self, _event=None) -> None:
        idx = self.room_box.current(); self.room_id = self.house.conditioned_rooms[idx]["id"]; self._draw_room()

    def _step_room(self, step: int) -> None:
        idx = self.room_box.current(); idx = (idx + step) % len(self.house.conditioned_rooms); self.room_box.current(idx); self.room_id = self.house.conditioned_rooms[idx]["id"]; self._draw_room()

    def _font(self, amount: float) -> None:
        self.font_scale = max(0.8, min(1.6, self.font_scale + amount)); self._draw()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen; self.attributes("-fullscreen", self.fullscreen)

    def _exit_fullscreen(self) -> None:
        self.fullscreen = False; self.attributes("-fullscreen", False)

    def _responsive_refresh(self) -> None:
        if self.winfo_width() > 0: self._draw_room()


def main() -> None:
    app = ReferenceHouseShowroom(); app.after(150, app._draw_room); app.mainloop()


if __name__ == "__main__":
    main()
