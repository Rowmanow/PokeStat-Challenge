# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
import re
from mode_stat_rush import StatRush
from mode_draft import COLORS
from affichage_pc import apply_pc_window, place_webcam_slot


class StatRushPC(StatRush):
    def __init__(self, master=None, on_home=None, language="fr", webcam_aspect="4:3"):
        self.webcam_aspect = webcam_aspect
        super().__init__(master, on_home, language)
        self._fit_window()

    def _fit_window(self):
        """Match the PC home window exactly, including its desktop position."""
        self.update_idletasks()
        master = self.master
        if master is not None:
            master.update_idletasks()
            match = re.match(
                r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)",
                master.winfo_geometry(),
            )
            if match:
                width, height, x, y = map(int, match.groups())
                self.geometry(f"{width}x{height}+{x}+{y}")
                self.minsize(width, height)
                self.maxsize(width, height)
                self.resizable(False, False)
                place_webcam_slot(self, self.language, self.webcam_aspect)
                self.lift()
                return

        apply_pc_window(self, "PokéStat Challenge - Stat Rush")
        place_webcam_slot(self, self.language, self.webcam_aspect)

    def _build_ui(self):
        top = tk.Frame(self, bg=COLORS["bg"], height=260)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Button(top, text=self.tr("home"), command=self.go_home,
                  bg=COLORS["panel"], fg="white", relief="flat", bd=0,
                  padx=14, pady=8, font=("Segoe UI",10,"bold")).place(x=18,y=18)
        tk.Label(top, text=self.tr("title"), bg=COLORS["bg"], fg="white",
                 font=("Segoe UI",21,"bold")).place(x=250,y=28)

        settings = tk.Frame(top, bg=COLORS["panel"], padx=12, pady=10,
                            width=880, height=155)
        settings.place(x=18, y=88)
        settings.grid_propagate(False)
        for c in range(5):
            settings.columnconfigure(c, weight=1, uniform="rush_pc")
        labels = [self.tr("rule"), self.tr("hint"), self.tr("types"),
                  self.tr("generations"), self.tr("forms")]
        for c, text in enumerate(labels):
            tk.Label(settings, text=text, bg=COLORS["panel"], fg="#94a3b8",
                     font=("Segoe UI",8,"bold")).grid(
                         row=0,column=c,sticky="w",padx=(0 if c==0 else 7,0))
        self.rule_button = tk.Button(settings, command=self._cycle_rule, bg="white",
                                     fg=COLORS["dark"], relief="flat", bd=0,
                                     pady=8, font=("Segoe UI",8,"bold"))
        self.rule_button.grid(row=1,column=0,sticky="ew")
        self.hint_button = tk.Button(settings, command=self._toggle_hint, bg="white",
                                     fg=COLORS["dark"], relief="flat", bd=0,
                                     pady=8, font=("Segoe UI",8,"bold"))
        self.hint_button.grid(row=1,column=1,sticky="ew",padx=(7,0))
        self.type_button = tk.Button(settings, command=self.open_type_filter, bg="white",
                                     fg=COLORS["dark"], relief="flat", bd=0,
                                     pady=8, font=("Segoe UI",8,"bold"))
        self.type_button.grid(row=1,column=2,sticky="ew",padx=(7,0))
        self.gen_button = tk.Button(settings, command=self.open_generation_filter, bg="white",
                                    fg=COLORS["dark"], relief="flat", bd=0,
                                    pady=8, font=("Segoe UI",8,"bold"))
        self.gen_button.grid(row=1,column=3,sticky="ew",padx=(7,0))
        self.form_button = tk.Button(settings, command=self.open_form_filter, bg="white",
                                     fg=COLORS["dark"], relief="flat", bd=0,
                                     pady=8, font=("Segoe UI",8,"bold"))
        self.form_button.grid(row=1,column=4,sticky="ew",padx=(7,0))
        self.settings_start_button = tk.Button(
            settings,
            text=("APPLIQUER LES RÈGLES ET DÉMARRER" if self.language == "fr"
                  else "APPLY RULES AND START"),
            command=self.start_series, bg=COLORS["red"], fg="white",
            relief="flat", bd=0, pady=10, font=("Segoe UI",10,"bold"))
        self.settings_start_button.grid(row=2,column=0,columnspan=5,
                                        sticky="ew",pady=(12,0))

        main = tk.Frame(self, bg=COLORS["bg"], padx=18, pady=10)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=3, uniform="rush_main")
        main.columnconfigure(1, weight=2, uniform="rush_main")
        main.rowconfigure(0, weight=1)

        card = tk.Frame(main, bg="white", padx=14, pady=10,
                        highlightbackground="#dbe3ee", highlightthickness=1)
        card.grid(row=0,column=0,sticky="nsew",padx=(0,8))
        self.name_label = tk.Label(card,bg="white",fg=COLORS["dark"],
                                   font=("Segoe UI",24,"bold"))
        self.name_label.pack()
        self.types_frame = tk.Frame(card,bg="white",height=34)
        self.types_frame.pack(fill="x",pady=(4,2))
        self.types_frame.pack_propagate(False)
        image_box = tk.Frame(card,bg="white",height=195)
        image_box.pack(fill="x", expand=False)
        image_box.pack_propagate(False)
        self.image_label = tk.Label(image_box,bg="white",fg=COLORS["muted"],text="?")
        self.image_label.pack(fill="both",expand=True)
        self.prompt_label = tk.Label(card,bg="white",fg=COLORS["blue"],
                                     font=("Segoe UI",15,"bold"))
        self.prompt_label.pack(pady=(5,1))
        self.hint_label = tk.Label(card,bg="white",fg=COLORS["muted"],
                                   font=("Segoe UI",9,"bold"))
        self.hint_label.pack()
        # Indice Stat Rush PC très visible
        self.hint_label.config(bg=COLORS["gold"], fg=COLORS["dark"], font=("Segoe UI", 12, "bold"), padx=18, pady=7, relief="flat", bd=0)
        self.hint_label.pack_configure(fill="x", padx=75, pady=(8, 5))

        side = tk.Frame(main,bg=COLORS["panel"],padx=16,pady=12,
                        highlightbackground="#334155",highlightthickness=1)
        side.grid(row=0,column=1,sticky="nsew",padx=(8,0))
        side.columnconfigure(0,weight=1)
        score = tk.Frame(side,bg=COLORS["panel"])
        score.grid(row=0,column=0,sticky="ew",pady=(0,8))
        score.columnconfigure(0,weight=1)
        score.columnconfigure(1,weight=1)
        self.streak_label = tk.Label(score,bg=COLORS["panel"],fg=COLORS["gold"],
                                     font=("Segoe UI",14,"bold"))
        self.streak_label.grid(row=0,column=0,sticky="w")
        self.record_label = tk.Label(score,bg=COLORS["panel"],fg="white",
                                     font=("Segoe UI",12,"bold"))
        self.record_label.grid(row=0,column=1,sticky="e")

        self.stat_buttons = {}
        from mode_stat_rush import STAT_ORDER
        for i,key in enumerate(STAT_ORDER):
            button = tk.Button(
                side, command=lambda k=key:self._toggle_stat(k), relief="flat", bd=0,
                bg="#334155", fg="white", activebackground=COLORS["blue"],
                activeforeground="white", pady=7, font=("Segoe UI",10,"bold"),
                cursor="hand2", anchor="w", padx=18)
            button.grid(row=1+i,column=0,sticky="ew",pady=3)
            self.stat_buttons[key] = button

        self.status_label = tk.Label(
            side,bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",9,"bold"),
            wraplength=410,justify="center")
        self.status_label.grid(row=7,column=0,sticky="ew",pady=(5,3))

        self.action_button = tk.Button(
            side, command=self.start_series,
            text=("DÉMARRER LA SÉRIE" if self.language == "fr" else "START SERIES"),
            bg=COLORS["red"],fg="white",activebackground=COLORS["red"],
            activeforeground="white",relief="flat",bd=0,pady=10,
            font=("Segoe UI",11,"bold"),cursor="hand2")
        self.action_button.grid(row=8,column=0,sticky="ew",pady=(3,0))
        self._refresh_settings()

    def _show_hint_widget(self):
        if not self.hint_label.winfo_manager():
            self.hint_label.pack(fill="x", padx=75, pady=(8, 5))
        else:
            self.hint_label.pack_configure(fill="x", padx=75, pady=(8, 5))

    def _display_image(self, raw):
        self.sprite=None
        if not raw: self.image_label.config(image="",text="?"); return
        try:
            import io
            from PIL import Image, ImageTk
            image=Image.open(io.BytesIO(raw)).convert("RGBA")
            box=image.getchannel("A").getbbox()
            if box: image=image.crop(box)
            image.thumbnail((600, 185), Image.Resampling.LANCZOS)
            self.sprite=ImageTk.PhotoImage(image); self.image_label.config(image=self.sprite,text="")
        except (OSError,ValueError,tk.TclError): self.image_label.config(image="",text="?")
