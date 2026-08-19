"""Shared LAT-CES desktop visual theme.

The theme is intentionally small so every GUI can consume the same palette
without moving engineering state into presentation code.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


COLORS = {
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#475569",
    "primary": "#2563EB",
    "success": "#16A34A",
    "warning": "#D97706",
    "error": "#DC2626",
    "focus": "#0EA5A4",
    "border": "#CBD5E1",
}


def apply_latces_theme(root: tk.Misc) -> ttk.Style:
    """Apply one consistent Tk/ttk palette and button hierarchy."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=COLORS["background"])
    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TLabelframe", background=COLORS["background"], bordercolor=COLORS["border"])
    style.configure("TLabelframe.Label", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TNotebook", background=COLORS["background"], borderwidth=0)
    style.configure("TNotebook.Tab", padding=(14, 7), foreground=COLORS["muted"])
    style.map("TNotebook.Tab", foreground=[("selected", COLORS["primary"])])
    style.configure("LATCES.Primary.TButton", padding=(12, 7), foreground="#FFFFFF", background=COLORS["primary"])
    style.map("LATCES.Primary.TButton", background=[("active", "#1D4ED8")])
    style.configure("LATCES.Secondary.TButton", padding=(10, 6), foreground=COLORS["text"], background=COLORS["surface"])
    style.configure("LATCES.Danger.TButton", padding=(10, 6), foreground="#FFFFFF", background=COLORS["error"])
    style.configure("LATCES.Status.TLabel", padding=(8, 4), foreground=COLORS["muted"], background=COLORS["surface"])
    style.configure("LATCES.Success.TLabel", padding=(8, 4), foreground=COLORS["success"], background=COLORS["surface"])
    style.configure("LATCES.Warning.TLabel", padding=(8, 4), foreground=COLORS["warning"], background=COLORS["surface"])
    style.configure("LATCES.Error.TLabel", padding=(8, 4), foreground=COLORS["error"], background=COLORS["surface"])
    root.configure(background=COLORS["background"])
    return style


__all__ = ["COLORS", "apply_latces_theme"]
