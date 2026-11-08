# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk

DESKTOP_WIDTH = 1280
DESKTOP_HEIGHT = 720
MIN_WIDTH = 1152
MIN_HEIGHT = 648
WEBCAM_SLOT_WIDTH = 320
WEBCAM_SLOT_HEIGHT = 240
WEBCAM_RIGHT = 20
WEBCAM_TOP = 18


def apply_pc_window(window, title=None):
    if title:
        window.title(title)
    window.update_idletasks()
    sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
    width = min(DESKTOP_WIDTH, max(MIN_WIDTH, sw - 80))
    height = min(DESKTOP_HEIGHT, max(MIN_HEIGHT, sh - 100))
    x = max(0, (sw - width) // 2)
    y = max(0, (sh - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.minsize(MIN_WIDTH, MIN_HEIGHT)
    window.resizable(True, True)
    window.bind("<F11>", lambda _e: toggle_fullscreen(window))
    window.bind("<Escape>", lambda _e: window.attributes("-fullscreen", False))


def toggle_fullscreen(window):
    window.attributes("-fullscreen", not bool(window.attributes("-fullscreen")))


def place_webcam_slot(window, language="fr", aspect="4:3"):
    """Fixed top-right OBS slot. The outer 320x240 reservation never moves."""
    old = getattr(window, "_webcam_slot", None)
    if old and old.winfo_exists():
        old.destroy()

    outer = tk.Frame(window, bg="#0f172a", width=WEBCAM_SLOT_WIDTH,
                     height=WEBCAM_SLOT_HEIGHT)
    outer.place(relx=1.0, x=-WEBCAM_RIGHT, y=WEBCAM_TOP, anchor="ne")
    outer.pack_propagate(False)

    video_height = 240 if aspect == "4:3" else 180
    video = tk.Frame(outer, bg="#111827", width=320, height=video_height,
                     highlightbackground="#64748b", highlightthickness=2)
    video.place(x=0, y=0)
    video.pack_propagate(False)
    title = "ZONE WEBCAM" if language == "fr" else "WEBCAM AREA"
    tk.Label(video, text=title, bg="#111827", fg="#94a3b8",
             font=("Segoe UI", 12, "bold")).place(relx=.5, rely=.44, anchor="center")
    tk.Label(video, text=f"{aspect}  •  320 × {video_height}", bg="#111827",
             fg="#64748b", font=("Segoe UI", 9)).place(relx=.5, rely=.59, anchor="center")
    window._webcam_slot = outer
    outer.lift()
    return outer
