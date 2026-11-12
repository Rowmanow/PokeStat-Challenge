# -*- coding: utf-8 -*-
from __future__ import annotations

import io
import json
import random
import re
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from PIL import Image, ImageTk

from mode_draft import (
    API, COLORS, TYPE_KEYS, TYPE_LABELS, TYPE_COLORS, TYPE_ICONS,
    STAT_ORDER, STAT_LABELS, special_form_generation, get_json, get_bytes,
    pretty_name, fallback_form_names,
)

RUSH_TEXT = {
    "fr": {
        "home": "← ACCUEIL", "title": "POKÉSTAT CHALLENGE · STAT RUSH",
        "types": "TYPES", "generations": "GÉNÉRATIONS", "forms": "FORMES",
        "rule": "RÈGLE", "hint": "INDICE DE RÉPONSES",
        "all_types": "TOUS LES TYPES", "all_generations": "TOUTES LES GÉNÉRATIONS",
        "both": "STANDARD + MÉGA", "standard": "STANDARD UNIQUEMENT", "mega": "MÉGA UNIQUEMENT",
        "highest": "MEILLEURE STAT", "lowest": "PLUS FAIBLE STAT", "mixed": "MIXTE ALÉATOIRE",
        "shown": "AFFICHÉ", "hidden": "MASQUÉ", "start": "DÉMARRER", "validate": "VALIDER",
        "next": "POKÉMON SUIVANT", "ready": "Prêt à lancer une série ?", "waiting": "EN ATTENTE D’UNE NOUVELLE PARTIE",
        "find_highest": "↑  TROUVE LA MEILLEURE STAT  ↑", "find_lowest": "↓  TROUVE LA PLUS FAIBLE STAT  ↓",
        "one_expected": "1 RÉPONSE ATTENDUE", "many_expected": "{n} RÉPONSES ATTENDUES",
        "streak": "SÉRIE", "record": "RECORD", "correct": "✓ CORRECT",
        "wrong": "✕ MAUVAISE RÉPONSE", "final": "SÉRIE FINALE : {n}",
        "new_record": "NOUVEAU RECORD !", "loading": "Chargement du Pokémon...",
        "select": "Sélectionne au moins une statistique.", "no_match": "Aucun Pokémon ne correspond à ces filtres.",
        "error": "Erreur", "retry": "REJOUER", "answer": "RÉPONSE",
        "type_filter": "Filtre par type", "gen_filter": "Filtre par génération",
        "forms_filter": "Filtre des formes", "apply": "APPLIQUER", "all": "TOUT", "none": "AUCUN",
        "generation": "Génération", "rules": "RÈGLES", "settings": "PARAMÈTRES",
    },
    "en": {
        "home": "← HOME", "title": "POKÉSTAT CHALLENGE · STAT RUSH",
        "types": "TYPES", "generations": "GENERATIONS", "forms": "FORMS",
        "rule": "RULE", "hint": "ANSWER HINT",
        "all_types": "ALL TYPES", "all_generations": "ALL GENERATIONS",
        "both": "STANDARD + MEGA", "standard": "STANDARD ONLY", "mega": "MEGA ONLY",
        "highest": "HIGHEST STAT", "lowest": "LOWEST STAT", "mixed": "RANDOM MIX",
        "shown": "SHOWN", "hidden": "HIDDEN", "start": "START", "validate": "SUBMIT",
        "next": "NEXT POKÉMON", "ready": "Ready to start a streak?", "waiting": "WAITING FOR A NEW GAME",
        "find_highest": "↑  FIND THE HIGHEST STAT  ↑", "find_lowest": "↓  FIND THE LOWEST STAT  ↓",
        "one_expected": "1 ANSWER EXPECTED", "many_expected": "{n} ANSWERS EXPECTED",
        "streak": "STREAK", "record": "RECORD", "correct": "✓ CORRECT",
        "wrong": "✕ WRONG ANSWER", "final": "FINAL STREAK: {n}",
        "new_record": "NEW RECORD!", "loading": "Loading Pokémon...",
        "select": "Select at least one stat.", "no_match": "No Pokémon matches these filters.",
        "error": "Error", "retry": "PLAY AGAIN", "answer": "ANSWER",
        "type_filter": "Type filter", "gen_filter": "Generation filter",
        "forms_filter": "Form filter", "apply": "APPLY", "all": "ALL", "none": "NONE",
        "generation": "Generation", "rules": "RULES", "settings": "SETTINGS",
    },
}

STAT_ICONS = {"hp": "♥", "attack": "⚔", "special-attack": "✦", "defense": "◐", "special-defense": "♟", "speed": "ϟ"}


def _save_dir() -> Path:
    root = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    path = root / "save"
    path.mkdir(exist_ok=True)
    return path


class StatRush(tk.Toplevel):
    def __init__(self, master=None, on_home=None, language="fr"):
        super().__init__(master)
        self.on_home = on_home
        self.language = language if language in ("fr", "en") else "fr"
        self.title("PokéStat Challenge - Stat Rush")
        self.configure(bg=COLORS["bg"])
        self.protocol("WM_DELETE_WINDOW", self.go_home)
        self.selected_types = set(TYPE_KEYS)
        self.selected_generations = set(range(1, 10))
        self.form_mode = "both"
        self.rule_mode = "mixed"
        self.hint_enabled = True
        self.current_rule = "highest"
        self.current = None
        self.expected = set()
        self.selected = set()
        self.remaining_names = []
        self.streak = 0
        self.finished = False
        self.busy = False
        self.sprite = None
        self.next_after_id = None
        self.stat_buttons = {}
        self.records = self._load_records()
        self._build_ui()
        self._prepare_idle()
        self.after(80, self._fit_window)

    def tr(self, key, **kwargs):
        return RUSH_TEXT[self.language][key].format(**kwargs)

    def stat_label(self, key):
        return STAT_LABELS[self.language][key]

    def type_label(self, key):
        return TYPE_LABELS[self.language].get(key, pretty_name(key))

    def go_home(self):
        callback = self.on_home
        self.destroy()
        if callback:
            callback()

    def _fit_window(self):
        """Use exactly the same size and desktop position as the home window."""
        self.update_idletasks()
        master = self.master
        if master is not None:
            master.update_idletasks()
            geometry = master.winfo_geometry()
            match = re.match(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", geometry)
            if match:
                width, height, x, y = map(int, match.groups())
                self.geometry(f"{width}x{height}+{x}+{y}")
                self.minsize(width, height)
                self.maxsize(width, height)
                self.resizable(False, False)
                self.lift()
                return

        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        height = min(1040, sh - 70)
        width = min(650, max(560, int(height * 9 / 16)))
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(width, height)
        self.maxsize(width, height)
        self.resizable(False, False)

    def _load_records(self):
        path = _save_dir() / "stat_rush_records.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def _record_key(self):
        return f"{self.rule_mode}_{'shown' if self.hint_enabled else 'hidden'}"

    def _record(self):
        return int(self.records.get(self._record_key(), 0))

    def _save_record(self):
        self.records[self._record_key()] = max(self._record(), self.streak)
        (_save_dir() / "stat_rush_records.json").write_text(
            json.dumps(self.records, ensure_ascii=False, indent=2), encoding="utf-8")

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg"], height=66)
        header.pack(fill="x"); header.pack_propagate(False)
        tk.Button(header, text=self.tr("home"), command=self.go_home, bg=COLORS["panel"], fg="white",
                  relief="flat", bd=0, padx=10, pady=7, font=("Segoe UI", 9, "bold")).place(x=14, rely=.5, anchor="w")
        tk.Label(header, text=self.tr("title"), bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 15, "bold")).place(relx=.58, rely=.5, anchor="center")

        body = tk.Frame(self, bg=COLORS["bg"], padx=13)
        body.pack(fill="both", expand=True)
        settings = tk.Frame(body, bg=COLORS["panel"], padx=10, pady=8)
        settings.pack(fill="x", pady=(0, 8))
        for c in range(2): settings.columnconfigure(c, weight=1, uniform="rush")

        self._setting_label(settings, self.tr("rule"), 0, 0)
        self._setting_label(settings, self.tr("hint"), 0, 1)
        self.rule_button = tk.Button(settings, command=self._cycle_rule, bg="white", fg=COLORS["dark"], relief="flat", bd=0, pady=7, font=("Segoe UI", 8, "bold"))
        self.rule_button.grid(row=1, column=0, sticky="ew", padx=(0, 4))
        self.hint_button = tk.Button(settings, command=self._toggle_hint, bg="white", fg=COLORS["dark"], relief="flat", bd=0, pady=7, font=("Segoe UI", 8, "bold"))
        self.hint_button.grid(row=1, column=1, sticky="ew", padx=(4, 0))

        self._setting_label(settings, self.tr("types"), 2, 0)
        self._setting_label(settings, self.tr("generations"), 2, 1)
        self.type_button = tk.Button(settings, command=self.open_type_filter, bg="white", fg=COLORS["dark"], relief="flat", bd=0, pady=7, font=("Segoe UI", 8, "bold"))
        self.type_button.grid(row=3, column=0, sticky="ew", padx=(0, 4))
        self.gen_button = tk.Button(settings, command=self.open_generation_filter, bg="white", fg=COLORS["dark"], relief="flat", bd=0, pady=7, font=("Segoe UI", 8, "bold"))
        self.gen_button.grid(row=3, column=1, sticky="ew", padx=(4, 0))

        self._setting_label(settings, self.tr("forms"), 4, 0)
        self.form_button = tk.Button(settings, command=self.open_form_filter, bg="white", fg=COLORS["dark"], relief="flat", bd=0, pady=7, font=("Segoe UI", 8, "bold"))
        self.form_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        score = tk.Frame(body, bg=COLORS["panel"], padx=12, pady=7)
        score.pack(fill="x", pady=(0, 8))
        self.streak_label = tk.Label(score, bg=COLORS["panel"], fg=COLORS["gold"], font=("Segoe UI", 12, "bold"))
        self.streak_label.pack(side="left")
        self.record_label = tk.Label(score, bg=COLORS["panel"], fg="white", font=("Segoe UI", 11, "bold"))
        self.record_label.pack(side="right")

        card = tk.Frame(body, bg="white", padx=12, pady=8)
        card.pack(fill="x", pady=(0, 8))
        self.name_label = tk.Label(card, bg="white", fg=COLORS["dark"], font=("Segoe UI", 20, "bold"))
        self.name_label.pack()
        self.types_frame = tk.Frame(card, bg="white", height=32)
        self.types_frame.pack(fill="x", pady=(1, 2)); self.types_frame.pack_propagate(False)
        image_box = tk.Frame(card, bg="white", width=370, height=145)
        image_box.pack(); image_box.pack_propagate(False)
        self.image_label = tk.Label(image_box, bg="white", fg=COLORS["muted"], text="?", font=("Segoe UI", 50, "bold"))
        self.image_label.pack(fill="both", expand=True)
        self.prompt_label = tk.Label(card, bg="white", fg=COLORS["blue"], font=("Segoe UI", 14, "bold"))
        self.prompt_label.pack(pady=(4, 0))
        self.hint_label = tk.Label(card, bg=COLORS["gold"], fg=COLORS["dark"], font=("Segoe UI", 10, "bold"), padx=12, pady=4)
        self.hint_label.pack(pady=(2, 0))

        answers = tk.Frame(body, bg=COLORS["panel"], padx=10, pady=8)
        answers.pack(fill="both", expand=True)
        answers.columnconfigure(0, weight=1)
        for i, key in enumerate(STAT_ORDER):
            button = tk.Button(answers, command=lambda k=key: self._toggle_stat(k), relief="flat", bd=0,
                               bg="#334155", fg="white", activebackground=COLORS["blue"], activeforeground="white",
                               pady=9, font=("Segoe UI", 9, "bold"), cursor="hand2")
            button.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
            self.stat_buttons[key] = button

        self.status_label = tk.Label(body, bg=COLORS["bg"], fg="#94a3b8", font=("Segoe UI", 10, "bold"))
        self.status_label.pack(pady=(5, 2))
        self.action_button = tk.Button(body, command=self.start_series, bg=COLORS["red"], fg="white",
                                       relief="flat", bd=0, pady=11, font=("Segoe UI", 11, "bold"))
        self.action_button.pack(fill="x", pady=(2, 7))
        self._refresh_settings()

    def _setting_label(self, parent, text, row, column):
        tk.Label(parent, text=text, bg=COLORS["panel"], fg="#94a3b8",
                 font=("Segoe UI", 8, "bold")).grid(row=row, column=column, sticky="w", padx=(0 if column == 0 else 4, 0), pady=(3, 2))

    def _rule_text(self): return self.tr(self.rule_mode)
    def _hint_text(self): return self.tr("shown" if self.hint_enabled else "hidden")
    def _form_text(self): return self.tr(self.form_mode)

    def _refresh_settings(self):
        self.rule_button.config(text=self._rule_text())
        self.hint_button.config(text=self._hint_text())
        self.type_button.config(text=self.tr("all_types") if len(self.selected_types) == len(TYPE_KEYS) else f"{len(self.selected_types)} {self.tr('types')}")
        self.gen_button.config(text=self.tr("all_generations") if len(self.selected_generations) == 9 else ", ".join(map(str, sorted(self.selected_generations))))
        self.form_button.config(text=self._form_text())
        self._refresh_score()

    def _refresh_score(self):
        self.streak_label.config(text=f"{self.tr('streak')} : {self.streak}")
        self.record_label.config(text=f"{self.tr('record')} : {self._record()}")

    def _cycle_rule(self):
        modes = ["highest", "lowest", "mixed"]
        self.rule_mode = modes[(modes.index(self.rule_mode) + 1) % len(modes)]
        self._reset_pool(); self._refresh_settings()

    def _toggle_hint(self):
        self.hint_enabled = not self.hint_enabled
        self._refresh_settings(); self._update_hint()

    def _reset_pool(self):
        self.remaining_names = []

    def _prepare_idle(self):
        self.finished = False; self.current = None; self.selected.clear(); self.expected.clear()
        self.name_label.config(text=self.tr("ready")); self.image_label.config(image="", text="?")
        self._show_types([]); self.prompt_label.config(text="STAT RUSH"); self._update_hint()
        self.status_label.config(text=""); self.action_button.config(text=self.tr("start"), command=self.start_series, state="normal")
        self._set_stat_state(False); self._set_settings_state(True); self._refresh_score()

    def start_series(self):
        if self.busy: return
        self._cancel_scheduled_next()
        self._set_settings_state(False)
        self.streak = 0; self.finished = False; self.remaining_names = []
        self._refresh_score(); self._next_pokemon()

    def _next_pokemon(self):
        if self.finished or self.busy: return
        self.busy = True; self.selected.clear(); self.expected.clear()
        self._reset_button_colors(); self._set_stat_state(False)
        self.action_button.config(state="disabled", text=self.tr("validate"))
        self.status_label.config(text=self.tr("loading"), fg="#94a3b8")
        threading.Thread(target=self._load_next_worker, daemon=True).start()

    def _load_next_worker(self):
        try:
            if not self.remaining_names:
                self.remaining_names = self._build_pool()
                random.shuffle(self.remaining_names)
            while self.remaining_names:
                name = self.remaining_names.pop()
                pokemon = self._prepare_pokemon(name)
                # Mew-like profiles are excluded: all six stats are identical.
                if len(set(pokemon["stats"].values())) == 1:
                    continue
                self.after(0, lambda p=pokemon: self._apply_pokemon(p))
                return
            raise ValueError(self.tr("no_match"))
        except Exception as exc:
            self.after(0, lambda e=exc: self._load_failed(e))

    def _load_failed(self, exc):
        self.busy = False
        self.status_label.config(text=str(exc), fg=COLORS["red"])
        self.action_button.config(text=self.tr("retry"), command=self.start_series,
                                  state="normal", bg=COLORS["red"], fg="white")
        self._set_settings_state(True)

    def _build_pool(self):
        generation_names = set()
        for number in self.selected_generations:
            data = get_json(f"{API}/generation/{number}", f"generation_{number}.json")
            generation_names.update(x["name"] for x in data.get("pokemon_species", []))
        typed = set()
        for type_name in self.selected_types:
            data = get_json(f"{API}/type/{type_name}", f"type_{type_name}.json")
            typed.update(x["pokemon"]["name"] for x in data.get("pokemon", []))
        standard = generation_names & typed
        all_forms = get_json(f"{API}/pokemon?limit=100000&offset=0", "pokemon_all_forms.json")
        mega = {item["name"] for item in all_forms.get("results", []) if "-mega" in item["name"] and item["name"] in typed and special_form_generation(item["name"]) in self.selected_generations}
        pool = standard if self.form_mode == "standard" else mega if self.form_mode == "mega" else standard | mega
        if not pool: raise ValueError(self.tr("no_match"))
        return list(pool)

    def _prepare_pokemon(self, name):
        data = get_json(f"{API}/pokemon/{name}", f"pokemon_{name}.json")
        stats = {x["stat"]["name"]: x["base_stat"] for x in data["stats"]}
        species_name = data.get("species", {}).get("name", name)
        species = get_json(f"{API}/pokemon-species/{species_name}", f"species_{species_name}.json")
        en = next((x["name"] for x in species.get("names", []) if x.get("language", {}).get("name") == "en"), pretty_name(species_name))
        fr = next((x["name"] for x in species.get("names", []) if x.get("language", {}).get("name") == "fr"), en)
        names = {"fr": fr, "en": en}
        if special_form_generation(name) is not None:
            names = fallback_form_names(name, fr, en)
            try:
                form_name = data.get("forms", [{}])[0].get("name", name)
                form_data = get_json(f"{API}/pokemon-form/{form_name}", f"form_{form_name}.json")
                localized = {x.get("language", {}).get("name"): x.get("name") for x in form_data.get("names", []) if x.get("name")}
                names["fr"] = localized.get("fr", names["fr"]); names["en"] = localized.get("en", names["en"])
            except Exception:
                pass
        sprites = data.get("sprites", {})
        url = sprites.get("other", {}).get("official-artwork", {}).get("front_default") or sprites.get("other", {}).get("home", {}).get("front_default") or sprites.get("front_default")
        raw = get_bytes(url, f"rush_artwork_{name}.png") if url else None
        return {"api_name": name, "names": names, "stats": stats, "types": [x["type"]["name"] for x in data["types"]], "raw": raw}

    def _apply_pokemon(self, pokemon):
        self.busy = False; self.current = pokemon
        self.current_rule = random.choice(["highest", "lowest"]) if self.rule_mode == "mixed" else self.rule_mode
        extreme = max(pokemon["stats"].values()) if self.current_rule == "highest" else min(pokemon["stats"].values())
        self.expected = {key for key, value in pokemon["stats"].items() if value == extreme}
        name = pokemon["names"].get(self.language) or pokemon["names"]["en"]
        self.name_label.config(text=name); self._show_types(pokemon["types"]); self._display_image(pokemon["raw"])
        self.prompt_label.config(text=self.tr("find_highest" if self.current_rule == "highest" else "find_lowest"))
        self._update_hint(); self.status_label.config(text=""); self._set_stat_state(True)
        self.action_button.config(text=self.tr("validate"), command=self.validate_answer, state="normal", bg=COLORS["gold"], fg=COLORS["dark"])

    def _show_hint_widget(self):
        if not self.hint_label.winfo_manager():
            self.hint_label.pack(pady=(2, 0))

    def _hide_hint_widget(self):
        if self.hint_label.winfo_manager():
            self.hint_label.pack_forget()

    def _update_hint(self):
        if not self.hint_enabled:
            self.hint_label.config(text="")
            self._hide_hint_widget()
            return

        self._show_hint_widget()
        text = self.tr("waiting") if not self.expected else (
            self.tr("one_expected") if len(self.expected) == 1
            else self.tr("many_expected", n=len(self.expected))
        )
        self.hint_label.config(text=text, bg=COLORS["gold"], fg=COLORS["dark"])

    def _display_image(self, raw):
        self.sprite = None
        if not raw: self.image_label.config(image="", text="?"); return
        try:
            image = Image.open(io.BytesIO(raw)).convert("RGBA")
            box = image.getchannel("A").getbbox()
            if box: image = image.crop(box)
            image.thumbnail((360, 135), Image.Resampling.LANCZOS)
            self.sprite = ImageTk.PhotoImage(image); self.image_label.config(image=self.sprite, text="")
        except (OSError, ValueError, tk.TclError):
            self.image_label.config(image="", text="?")

    def _show_types(self, types):
        for w in self.types_frame.winfo_children(): w.destroy()
        if not types: return
        group = tk.Frame(self.types_frame, bg="white"); group.place(relx=.5, rely=.5, anchor="center")
        for type_name in types:
            color = TYPE_COLORS.get(type_name, COLORS["muted"])
            badge = tk.Frame(group, bg=color, padx=7, pady=3); badge.pack(side="left", padx=3)
            tk.Label(badge, text=f"{TYPE_ICONS.get(type_name, '●')}  {self.type_label(type_name).upper()}", bg=color, fg="white", font=("Segoe UI", 8, "bold")).pack()

    def _toggle_stat(self, key):
        if self.busy or self.finished or not self.current: return
        if key in self.selected: self.selected.remove(key)
        else: self.selected.add(key)
        self.stat_buttons[key].config(bg=COLORS["blue"] if key in self.selected else "#334155")

    def validate_answer(self):
        if not self.selected:
            self.status_label.config(text=self.tr("select"), fg=COLORS["red"]); return
        correct = self.selected == self.expected
        self._set_stat_state(False)
        for key, button in self.stat_buttons.items():
            value = self.current["stats"][key]
            button.config(text=f"{STAT_ICONS[key]}  {self.stat_label(key)}  ·  {value}")
            if key in self.expected and key in self.selected: button.config(bg=COLORS["green"], fg="white")
            elif key in self.expected: button.config(bg=COLORS["gold"], fg=COLORS["dark"])
            elif key in self.selected: button.config(bg=COLORS["red"], fg="white")
            else: button.config(bg="#475569", fg="white")
        if correct:
            self.streak += 1
            is_record = self.streak > self._record()
            if is_record: self._save_record()
            self._refresh_score(); self.status_label.config(text=self.tr("new_record") if is_record else self.tr("correct"), fg=COLORS["green"])
            self.action_button.config(text=self.tr("next"), command=self._manual_next,
                                      state="normal", bg=COLORS["green"], fg="white")
            self.next_after_id = self.after(1150, self._automatic_next)
        else:
            self.finished = True; self._save_record(); self._refresh_score()
            self.status_label.config(text=f"{self.tr('wrong')} · {self.tr('final', n=self.streak)}", fg=COLORS["red"])
            self.action_button.config(text=self.tr("retry"), command=self.start_series, state="normal", bg=COLORS["red"], fg="white")
            self._set_settings_state(True)

    def _set_settings_state(self, enabled):
        state = "normal" if enabled else "disabled"
        for widget in (self.rule_button, self.hint_button, self.type_button,
                       self.gen_button, self.form_button):
            widget.config(state=state)

    def _cancel_scheduled_next(self):
        if self.next_after_id is not None:
            try:
                self.after_cancel(self.next_after_id)
            except tk.TclError:
                pass
            self.next_after_id = None

    def _manual_next(self):
        self._cancel_scheduled_next()
        self._next_pokemon()

    def _automatic_next(self):
        self.next_after_id = None
        if not self.busy and not self.finished:
            self._next_pokemon()

    def _set_stat_state(self, enabled):
        for button in self.stat_buttons.values(): button.config(state="normal" if enabled else "disabled", cursor="hand2" if enabled else "arrow")

    def _reset_button_colors(self):
        for key, button in self.stat_buttons.items():
            button.config(text=f"{STAT_ICONS[key]}  {self.stat_label(key)}", bg="#334155", fg="white")

    def _filter_popup(self, title, items, selected, apply_callback):
        popup = tk.Toplevel(self); popup.title(title); popup.configure(bg=COLORS["bg"]); popup.transient(self); popup.grab_set(); popup.resizable(False, False)
        box = tk.Frame(popup, bg=COLORS["panel"], padx=14, pady=12); box.pack(padx=18, pady=(18, 8))
        variables = {}
        for i, (key, label) in enumerate(items):
            var = tk.BooleanVar(value=key in selected); variables[key] = var
            tk.Checkbutton(box, text=label, variable=var, bg=COLORS["panel"], fg="white", selectcolor=COLORS["dark"], activebackground=COLORS["panel"], activeforeground="white", font=("Segoe UI", 9, "bold")).grid(row=i//2, column=i%2, sticky="w", padx=8, pady=4)
        actions = tk.Frame(popup, bg=COLORS["bg"]); actions.pack(fill="x", padx=18, pady=(0, 14))
        tk.Button(actions, text=self.tr("all"), command=lambda: [v.set(True) for v in variables.values()], bg="#334155", fg="white", relief="flat", bd=0, padx=10, pady=7).pack(side="left")
        tk.Button(actions, text=self.tr("none"), command=lambda: [v.set(False) for v in variables.values()], bg="#334155", fg="white", relief="flat", bd=0, padx=10, pady=7).pack(side="left", padx=5)
        tk.Button(actions, text=self.tr("apply"), command=lambda: apply_callback(popup, variables), bg=COLORS["blue"], fg="white", relief="flat", bd=0, padx=14, pady=7).pack(side="right")
        popup.update_idletasks(); popup.geometry(f"{popup.winfo_reqwidth()}x{popup.winfo_reqheight()}+{self.winfo_rootx()+80}+{self.winfo_rooty()+100}")

    def open_type_filter(self):
        self._filter_popup(self.tr("type_filter"), [(k, self.type_label(k)) for k in TYPE_KEYS], self.selected_types, self._apply_types)

    def open_generation_filter(self):
        roman = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX"}
        self._filter_popup(self.tr("gen_filter"), [(n, f"{self.tr('generation')} {roman[n]}") for n in range(1,10)], self.selected_generations, self._apply_generations)

    def _apply_types(self, popup, variables):
        values = {k for k,v in variables.items() if v.get()}
        if not values: return
        self.selected_types = values; popup.destroy(); self._reset_pool(); self._refresh_settings()

    def _apply_generations(self, popup, variables):
        values = {k for k,v in variables.items() if v.get()}
        if not values: return
        self.selected_generations = values; popup.destroy(); self._reset_pool(); self._refresh_settings()

    def open_form_filter(self):
        popup = tk.Toplevel(self); popup.title(self.tr("forms_filter")); popup.configure(bg=COLORS["bg"]); popup.transient(self); popup.grab_set(); popup.resizable(False, False)
        value = tk.StringVar(value=self.form_mode)
        box = tk.Frame(popup, bg=COLORS["panel"], padx=18, pady=14); box.pack(padx=18, pady=(18, 8))
        for key in ("standard", "mega", "both"):
            tk.Radiobutton(box, text=self.tr(key), variable=value, value=key, bg=COLORS["panel"], fg="white", selectcolor=COLORS["dark"], activebackground=COLORS["panel"], activeforeground="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=4)
        tk.Button(popup, text=self.tr("apply"), command=lambda: self._apply_form(popup, value.get()), bg=COLORS["blue"], fg="white", relief="flat", bd=0, padx=18, pady=8).pack(pady=(0, 15))
        popup.update_idletasks(); popup.geometry(f"{popup.winfo_reqwidth()}x{popup.winfo_reqheight()}+{self.winfo_rootx()+100}+{self.winfo_rooty()+120}")

    def _apply_form(self, popup, value):
        self.form_mode = value; popup.destroy(); self._reset_pool(); self._refresh_settings()
