# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from mode_draft import *
from affichage_pc import apply_pc_window, place_webcam_slot


class PokemonStatDraftPC(PokemonStatDraft):
    def __init__(self, master=None, on_home=None, language="fr", webcam_aspect="4:3"):
        self.webcam_aspect = webcam_aspect
        super().__init__(master, on_home, language)
        apply_pc_window(self, "PokéStat Challenge - Draft")
        place_webcam_slot(self, self.language, self.webcam_aspect)

    def _fit_window(self):
        apply_pc_window(self, "PokéStat Challenge - Draft")
        place_webcam_slot(self, self.language, self.webcam_aspect)

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg"], height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Three independent positions: logo left, title at the exact center, total right.
        # Changing the logo or score width can no longer move the central title.
        try:
            self.header_logo = tk.PhotoImage(file=str(ASSETS / "pokemon_logo.png"))
            tk.Label(header, image=self.header_logo, bg=COLORS["bg"], bd=0).place(
                x=18, rely=0.5, anchor="w")
        except tk.TclError:
            tk.Label(header, text="POKÉMON", bg=COLORS["bg"], fg=COLORS["gold"],
                     font=("Segoe UI Black", 11, "bold")).place(x=18, rely=0.5, anchor="w")

        # Center within the usable game area (left of the fixed 320 px webcam slot).
        title_zone = tk.Frame(header, bg=COLORS["bg"], width=900, height=72)
        title_zone.place(x=0, y=0)
        title_zone.pack_propagate(False)
        tk.Label(title_zone, text="POKÉSTAT CHALLENGE - DRAFT", bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 17, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(header, text="← ACCUEIL", command=self._return_home,
                  bg=COLORS["panel"], fg="white", activebackground=COLORS["blue"],
                  activeforeground="white", relief="flat", bd=0, padx=8, pady=6,
                  font=("Segoe UI", 8, "bold"), cursor="hand2").place(x=12, y=4)

        self.header_score = tk.Label(header, text="TOTAL  0", bg=COLORS["red"], fg="white",
                                     padx=12, pady=8, font=("Segoe UI", 11, "bold"))
        self.header_score.place_forget()

        body = tk.Frame(self, bg=COLORS["bg"], padx=18, pady=0)
        body.pack(fill="both", expand=True)

        settings = tk.Frame(body, bg=COLORS["panel"], padx=14, pady=12)
        settings.place(x=0, y=0, width=900, height=175)
        self.mode_var = tk.StringVar(value=self.tr("high"))
        self.target_var = tk.IntVar(value=600)

        # Two balanced rows of three controls.
        for col in range(3):
            settings.columnconfigure(col, weight=1, uniform="menu")

        # Compact settings: three filters on the first row, then game controls.
        for col in range(4):
            settings.columnconfigure(col, weight=1, uniform="compact")

        self.types_title = tk.Label(settings, text=self.tr("types"), bg=COLORS["panel"], fg="#94a3b8",
                                    font=("Segoe UI", 8, "bold"))
        self.types_title.grid(row=0, column=0, sticky="w")
        self.generations_title = tk.Label(settings, text=self.tr("generations"), bg=COLORS["panel"], fg="#94a3b8",
                                          font=("Segoe UI", 8, "bold"))
        self.generations_title.grid(row=0, column=1, sticky="w", padx=(6, 0))
        self.form_title = tk.Label(settings, text=self.form_tr("title"), bg=COLORS["panel"], fg="#94a3b8",
                                   font=("Segoe UI", 8, "bold"))
        self.form_title.grid(row=0, column=2, sticky="w", padx=(6, 0))

        self.type_button = tk.Button(settings, text=self.tr("types_all"), command=self.open_type_filter,
                                     bg=COLORS["blue"], fg="white", activebackground="#1d4ed8",
                                     activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                     padx=3, pady=8, font=("Segoe UI", 8, "bold"))
        self.type_button.grid(row=1, column=0, sticky="ew", pady=(3, 8))
        self.generation_button = tk.Button(settings, text=self.tr("gen_all"), command=self.open_generation_filter,
                                           bg=COLORS["blue"], fg="white", activebackground="#1d4ed8",
                                           activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                           padx=3, pady=8, font=("Segoe UI", 8, "bold"))
        self.generation_button.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(3, 8))
        self.form_button = tk.Button(settings, text=self._form_button_text(), command=self.open_form_filter,
                                     bg="#334155", fg="white", activebackground="#475569",
                                     activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                     padx=3, pady=8, font=("Segoe UI", 8, "bold"))
        self.form_button.grid(row=1, column=2, sticky="ew", padx=(6, 0), pady=(3, 8))

        self.mode_title = tk.Label(settings, text=self.tr("mode"), bg=COLORS["panel"], fg="#94a3b8",
                                   font=("Segoe UI", 8, "bold"))
        self.mode_title.grid(row=2, column=0, sticky="w")
        self.target_title = tk.Label(settings, text=self.tr("target"), bg=COLORS["panel"], fg="#94a3b8",
                                     font=("Segoe UI", 8, "bold"))
        self.target_title.grid(row=2, column=1, sticky="w", padx=(6, 0))
        self.game_title = tk.Label(settings, text=self.tr("game"), bg=COLORS["panel"], fg="#94a3b8",
                                   font=("Segoe UI", 8, "bold"))
        self.game_title.grid(row=2, column=2, sticky="w", padx=(6, 0))
        self.launch_title = tk.Label(settings, text=self.tr("launch"), bg=COLORS["panel"], fg="#94a3b8",
                                     font=("Segoe UI", 8, "bold"))
        self.launch_title.grid(row=2, column=3, sticky="w", padx=(6, 0))

        self.mode_box = ttk.Combobox(settings, textvariable=self.mode_var, state="readonly",
                                     values=[self.tr("high"), self.tr("low"), self.tr("closest")], width=14)
        self.mode_box.grid(row=3, column=0, sticky="ew", pady=(3, 0))
        target_box = tk.Frame(settings, bg=COLORS["panel"])
        target_box.grid(row=3, column=1, sticky="ew", padx=(6, 0), pady=(3, 0))
        target_box.columnconfigure(0, weight=1)
        ttk.Spinbox(target_box, from_=1, to=1500, textvariable=self.target_var,
                    width=5).grid(row=0, column=0, sticky="ew")
        self.random_target_button = tk.Button(
            target_box, text=self.tr("random_target"), command=self.randomize_target,
            bg="#334155", fg="white", activebackground="#475569",
            activeforeground="white", relief="flat", bd=0, cursor="hand2",
            padx=5, pady=4, font=("Segoe UI", 7, "bold"),
        )
        self.random_target_button.grid(row=0, column=1, sticky="ns", padx=(4, 0))
        self.preload_button = tk.Button(settings, text=self.tr("preload"), command=self.preload_pokemon,
                                        bg=COLORS["blue"], fg="white", activebackground="#1d4ed8",
                                        activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                        padx=3, pady=8, font=("Segoe UI", 8, "bold"))
        self.preload_button.grid(row=3, column=2, sticky="ew", padx=(6, 0), pady=(3, 0))
        self.start_button = tk.Button(settings, text=self.tr("start"), command=self.start_game,
                                      state="disabled", bg=COLORS["red"], fg="white",
                                      disabledforeground="#fecaca", activebackground=COLORS["red_hover"],
                                      activeforeground="white", relief="flat", bd=0, cursor="arrow",
                                      padx=3, pady=8, font=("Segoe UI", 8, "bold"))
        self.start_button.grid(row=3, column=3, sticky="ew", padx=(6, 0), pady=(3, 0))

        content = tk.Frame(body, bg=COLORS["bg"])
        content.place(x=0, y=210, relwidth=1.0, relheight=1.0, height=-218)
        content.columnconfigure(0, weight=3, uniform="pc")
        content.columnconfigure(1, weight=2, uniform="pc")
        content.rowconfigure(0, weight=1)

        self.pokemon_card = tk.Frame(content, bg=COLORS["card"], padx=18, pady=8)
        self.pokemon_card.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        self.current_title = tk.Label(self.pokemon_card, text=self.tr("current"), bg="white", fg=COLORS["muted"],
                 font=("Segoe UI", 9, "bold"))
        self.current_title.pack()
        self.name_label = tk.Label(self.pokemon_card, text=self.tr("ready"), bg="white", fg=COLORS["dark"],
                                   font=("Segoe UI", 18, "bold"), anchor="center")
        self.name_label.pack(pady=(4, 1))
        self.types_frame = tk.Frame(self.pokemon_card, bg="white", width=360, height=34)
        self.types_frame.pack(pady=(0, 2))
        self.types_frame.pack_propagate(False)

        # Zone d'image strictement fixe : aucun sprite ne peut modifier la géométrie.
        self.sprite_box = tk.Frame(self.pokemon_card, bg="white", width=650, height=255)
        self.sprite_box.pack(pady=(0, 0))
        self.sprite_box.pack_propagate(False)
        self.sprite_label = tk.Label(self.sprite_box, bg="white", fg=COLORS["muted"], text="?",
                                     font=("Segoe UI", 55, "bold"), bd=0)
        self.sprite_label.place(x=0, y=0, width=650, height=255)

        stats_card = tk.Frame(content, bg=COLORS["card"], padx=14, pady=10)
        stats_card.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        title_line = tk.Frame(stats_card, bg="white")
        title_line.pack(fill="x", pady=(0, 10))
        self.team_title = tk.Label(title_line, text=("COMPOSITION" if self.language == "fr" else "TEAM"), bg="white", fg=COLORS["dark"],
                 font=("Segoe UI", 12, "bold"))
        self.team_title.pack(side="left")
        self.progress_label = tk.Label(title_line, text="0 / 6", bg=COLORS["soft"], fg=COLORS["blue"],
                                       padx=10, pady=5, font=("Segoe UI", 10, "bold"))
        self.progress_label.pack(side="right")
        self.header_score = tk.Label(title_line, text="TOTAL  0", bg=COLORS["red"], fg="white",
                                     width=12, padx=7, pady=7, font=("Segoe UI", 9, "bold"))
        self.header_score.pack(side="right", padx=(6, 0))

        self.recap_button = tk.Button(title_line, text=("RÉCAP" if self.language == "fr" else "RECAP"), command=self.show_recap,
                                      state="disabled", bg=COLORS["blue"], fg="white",
                                      disabledforeground="#94a3b8", relief="flat", bd=0,
                                      padx=7, pady=5, font=("Segoe UI", 8, "bold"), cursor="arrow")
        self.recap_button.pack(side="right", padx=(0, 7))

        self.stat_rows = {}
        self.stat_name_labels = {}
        self.value_labels = {}
        self.stat_buttons = {}
        for key in STAT_ORDER:
            row = tk.Frame(stats_card, bg=COLORS["soft"], padx=10, pady=4,
                           highlightbackground=COLORS["line"], highlightthickness=1)
            row.pack(fill="x", pady=2)
            label = tk.Label(row, text=self.stat_label(key), bg=COLORS["soft"], fg=COLORS["dark"],
                             width=17, anchor="w", font=("Segoe UI", 10, "bold"))
            label.pack(side="left")
            value = tk.Label(row, text="—", bg=COLORS["soft"], fg=COLORS["muted"],
                             width=8, font=("Segoe UI", 10, "bold"))
            value.pack(side="left", expand=True)
            button = tk.Button(row, text=self.tr("choose"), command=lambda k=key: self.choose_stat(k),
                               state="disabled", bg=COLORS["blue"], fg="white",
                               activebackground="#1d4ed8", activeforeground="white",
                               disabledforeground="#94a3b8", relief="flat", bd=0,
                               cursor="hand2", padx=10, pady=5, font=("Segoe UI", 9, "bold"))
            button.pack(side="right")
            self.stat_rows[key], self.stat_name_labels[key], self.value_labels[key], self.stat_buttons[key] = row, label, value, button

        # Keep the original footer height and dark visual separation, but without visible text.
        footer = tk.Frame(body, bg=COLORS["bg"], height=1)
        footer.place_forget()
        footer.pack_propagate(False)
        self.footer_text = tk.Label(footer, text="", bg=COLORS["bg"], fg=COLORS["bg"])
        self.footer_text.pack(fill="both", expand=True)
        self.status = self.footer_text

    def show_recap(self):
        """PC recap at the exact same size and position as the game window."""
        if len(self.chosen_details) != 6:
            return

        import io
        from PIL import Image, ImageTk

        pokemon_details, optimal_assignment, optimal_total = self._calculate_optimal_team()
        player_total = sum(self.chosen.values())
        low_mode = self.game_mode == "low"
        closest_mode = self.game_mode == "closest"
        target = int(self.target_var.get())
        if closest_mode:
            gap = abs(player_total - target)
            optimal_gap = abs(optimal_total - target)
        else:
            gap = player_total - optimal_total if low_mode else optimal_total - player_total
            optimal_gap = 0

        popup = tk.Toplevel(self)
        popup.title(self.tr("recap"))
        popup.configure(bg=COLORS["bg"])
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)

        # Use exactly the same client size and desktop coordinates as Draft.
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        # winfo_x/y can briefly report 0,0 for a managed Toplevel on Windows.
        # winfo_rootx/y reflect the actual client position visible on screen.
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.update_idletasks()

        place_webcam_slot(popup, self.language, self.webcam_aspect)

        # Summary stays left of the fixed webcam reservation.
        score_area = tk.Frame(popup, bg=COLORS["bg"])
        score_area.place(x=18, y=78, width=880, height=118)
        score_area.columnconfigure(0, weight=1, uniform="scores")
        score_area.columnconfigure(1, weight=1, uniform="scores")
        score_area.rowconfigure(0, weight=1)

        left_score = tk.Frame(score_area, bg=COLORS["panel"], padx=12, pady=10)
        left_score.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        right_score = tk.Frame(score_area, bg=COLORS["panel"], padx=12, pady=10)
        right_score.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        tk.Label(left_score, text=self.tr("my_team"), bg=COLORS["panel"], fg="white",
                 font=("Segoe UI", 15, "bold")).pack()
        tk.Label(left_score, text=f"{self.tr('total')} : {player_total}",
                 bg=COLORS["panel"], fg=COLORS["gold"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(4, 0))

        optimal_title = (self.tr("closest_best") if closest_mode
                         else self.tr("minimum") if low_mode else self.tr("best"))
        tk.Label(right_score, text=optimal_title, bg=COLORS["panel"], fg="white",
                 font=("Segoe UI", 15, "bold")).pack()
        tk.Label(right_score, text=f"{self.tr('total')} : {optimal_total}",
                 bg=COLORS["panel"], fg=COLORS["green"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(4, 0))
        if closest_mode:
            gap_text = f"{self.tr('target_gap')} : {optimal_gap}"
        else:
            gap_text = self.tr("optimal_team") if gap == 0 else f"{self.tr('global_gap')} : {gap}"
        tk.Label(right_score, text=gap_text, bg=COLORS["panel"],
                 fg=COLORS["green"] if gap == 0 else COLORS["red"],
                 font=("Segoe UI", 8, "bold")).pack(pady=(3, 0))

        # Explicit fixed positions avoid overlap and guarantee six visible results.
        cards = tk.Frame(popup, bg=COLORS["bg"])
        cards.place(x=18, y=270, width=max(900, width - 36), height=350)
        self.recap_images = []

        area_width = max(900, width - 36)
        column_gap = 10
        card_width = (area_width - column_gap) // 2
        card_height = 108
        row_gap = 8

        for index in range(6):
            chosen_key = STAT_ORDER[index]
            detail = pokemon_details[index]
            optimal_key = optimal_assignment[index]
            row = index // 2
            column = index % 2
            card_x = column * (card_width + column_gap)
            card_y = row * (card_height + row_gap)

            card = tk.Frame(cards, bg="white", padx=7, pady=6,
                            highlightbackground=COLORS["line"], highlightthickness=1)
            card.place(x=card_x, y=card_y, width=card_width, height=card_height)

            image_box = tk.Frame(card, bg="white", width=82, height=94)
            image_box.pack(side="left")
            image_box.pack_propagate(False)
            image_label = tk.Label(image_box, bg="white", fg=COLORS["muted"],
                                   text=self.tr("image_unavailable"),
                                   font=("Segoe UI", 7, "bold"), justify="center")
            image_label.pack(fill="both", expand=True)

            raw = detail.get("sprite_raw")
            if raw:
                try:
                    source = Image.open(io.BytesIO(raw)).convert("RGBA")
                    alpha_box = source.getchannel("A").getbbox()
                    if alpha_box:
                        source = source.crop(alpha_box)
                    source.thumbnail((76, 86), Image.Resampling.LANCZOS)
                    recap_image = ImageTk.PhotoImage(source)
                    image_label.config(image=recap_image, text="")
                    self.recap_images.append(recap_image)
                except (OSError, ValueError, tk.TclError):
                    pass

            choice = tk.Frame(card, bg=COLORS["soft"], width=102, height=94)
            choice.pack(side="right", padx=(6, 0))
            choice.pack_propagate(False)
            tk.Label(choice,
                     text=f"{self.tr('my_choice')}\n{self.stat_label(chosen_key)}\n{detail['value']}",
                     bg=COLORS["soft"], fg=COLORS["blue"], justify="center",
                     wraplength=94, font=("Segoe UI", 8, "bold")).pack(expand=True, fill="both")

            info = tk.Frame(card, bg="white")
            info.pack(side="left", fill="both", expand=True, padx=(7, 2))
            tk.Label(info,
                     text=detail["names"].get(self.language) or detail["names"]["en"],
                     bg="white", fg=COLORS["dark"], anchor="w",
                     font=("Segoe UI", 10, "bold")).pack(fill="x")
            tk.Label(info,
                     text=" / ".join(self.type_label(t) for t in detail["types"]),
                     bg="white", fg=COLORS["muted"], anchor="w",
                     font=("Segoe UI", 7)).pack(fill="x")

            optimal_value = detail["all_stats"][optimal_key]
            same_choice = chosen_key == optimal_key
            tk.Label(info,
                     text=f"{self.tr('optimal_combo')} : {self.stat_label(optimal_key)} ({optimal_value})",
                     bg="white", fg=COLORS["dark"], anchor="w", justify="left",
                     wraplength=250, font=("Segoe UI", 8, "bold")).pack(fill="x", pady=(2, 0))
            tk.Label(info,
                     text=(self.tr("same_combo") if same_choice else self.tr("different")),
                     bg="white", fg=COLORS["green"] if same_choice else COLORS["red"],
                     anchor="w", font=("Segoe UI", 7, "bold")).pack(fill="x", pady=(1, 0))

            all_stats = detail["all_stats"]
            if closest_mode:
                local_value = optimal_value
                local_key = optimal_key
                local_label = self.tr("closest_best")
                local_gap = abs(detail["value"] - optimal_value)
            else:
                local_value = min(all_stats.values()) if low_mode else max(all_stats.values())
                local_keys = [key for key, value in all_stats.items() if value == local_value]
                local_key = local_keys[0]
                local_label = self.tr("lowest") if low_mode else self.tr("best_stat")
                local_gap = detail["value"] - local_value if low_mode else local_value - detail["value"]
            tk.Label(info,
                     text=f"{local_label} : {self.stat_label(local_key)} ({local_value}) · {self.tr('gap')} {local_gap}",
                     bg="white", fg=COLORS["muted"], anchor="w", justify="left",
                     wraplength=250, font=("Segoe UI", 7)).pack(fill="x", pady=(1, 0))

        tk.Button(popup, text=self.tr("close"), command=popup.destroy,
                  bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"],
                  activeforeground="white", relief="flat", bd=0,
                  padx=34, pady=9, font=("Segoe UI", 9, "bold")).place(
                      relx=.5, rely=1.0, y=-12, anchor="s")

        popup.lift(self)
        popup.focus_force()

