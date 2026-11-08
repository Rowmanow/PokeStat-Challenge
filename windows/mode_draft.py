# -*- coding: utf-8 -*-
"""PokéStat Challenge - multilingual edition."""
from __future__ import annotations

import base64
import concurrent.futures
import json
import itertools
import io
import random
import re
import threading
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

API = "https://pokeapi.co/api/v2"
APP_DIR = Path(__file__).resolve().parent
CACHE = APP_DIR / "cache"
ASSETS = APP_DIR / "assets"
CACHE.mkdir(exist_ok=True)

COLORS = {
    "bg": "#0f172a", "panel": "#172033", "card": "#ffffff", "soft": "#f1f5f9",
    "text": "#e2e8f0", "dark": "#0f172a", "muted": "#64748b", "line": "#dbe3ee",
    "red": "#ef4444", "red_hover": "#dc2626", "blue": "#2563eb", "green": "#16a34a",
    "locked": "#e8eef6", "gold": "#f59e0b",
}
STAT_ORDER = ["hp", "attack", "special-attack", "defense", "special-defense", "speed"]
TYPE_KEYS = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
             "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]

STAT_LABELS = {
    "fr": {"hp": "HP", "attack": "Attaque", "special-attack": "Attaque spéciale",
           "defense": "Défense", "special-defense": "Défense spéciale", "speed": "Vitesse"},
    "en": {"hp": "HP", "attack": "Attack", "special-attack": "Special Attack",
           "defense": "Defense", "special-defense": "Special Defense", "speed": "Speed"},
}
TYPE_LABELS = {
    "fr": {"normal": "Normal", "fire": "Feu", "water": "Eau", "electric": "Électrik",
           "grass": "Plante", "ice": "Glace", "fighting": "Combat", "poison": "Poison",
           "ground": "Sol", "flying": "Vol", "psychic": "Psy", "bug": "Insecte",
           "rock": "Roche", "ghost": "Spectre", "dragon": "Dragon", "dark": "Ténèbres",
           "steel": "Acier", "fairy": "Fée"},
    "en": {"normal": "Normal", "fire": "Fire", "water": "Water", "electric": "Electric",
           "grass": "Grass", "ice": "Ice", "fighting": "Fighting", "poison": "Poison",
           "ground": "Ground", "flying": "Flying", "psychic": "Psychic", "bug": "Bug",
           "rock": "Rock", "ghost": "Ghost", "dragon": "Dragon", "dark": "Dark",
           "steel": "Steel", "fairy": "Fairy"},
}
TYPE_COLORS = {"normal": "#94a3b8", "fire": "#f97316", "water": "#3b82f6", "electric": "#eab308",
    "grass": "#22c55e", "ice": "#38bdf8", "fighting": "#dc2626", "poison": "#a855f7",
    "ground": "#b7791f", "flying": "#60a5fa", "psychic": "#ec4899", "bug": "#84cc16",
    "rock": "#a16207", "ghost": "#7c3aed", "dragon": "#4f46e5", "dark": "#334155",
    "steel": "#64748b", "fairy": "#f472b6"}
FORM_FILTER_TEXT = {
    "fr": {"title":"FORMES", "all":"STANDARD + MÉGA", "standard":"STANDARD", "mega":"MÉGA UNIQUEMENT",
           "popup":"Filtre des formes", "heading":"Formes autorisées", "standard_choice":"FORMES STANDARD UNIQUEMENT",
           "mega_choice":"MÉGA-ÉVOLUTIONS UNIQUEMENT", "all_choice":"STANDARD + MÉGA-ÉVOLUTIONS", "apply":"APPLIQUER"},
    "en": {"title":"FORMS", "all":"STANDARD + MEGA", "standard":"STANDARD", "mega":"MEGA ONLY",
           "popup":"Form filter", "heading":"Allowed forms", "standard_choice":"STANDARD FORMS ONLY",
           "mega_choice":"MEGA EVOLUTIONS ONLY", "all_choice":"STANDARD + MEGA EVOLUTIONS", "apply":"APPLY"},
}

TYPE_ICONS = {"normal": "●", "fire": "♨", "water": "◆", "electric": "ϟ", "grass": "♣",
    "ice": "✦", "fighting": "✹", "poison": "☠", "ground": "▰", "flying": "➤",
    "psychic": "◉", "bug": "✣", "rock": "⬟", "ghost": "◖", "dragon": "♢",
    "dark": "☾", "steel": "⚙", "fairy": "★"}

TEXT = {
 "fr": {"types":"TYPES","generations":"GÉNÉRATIONS","language":"LANGUE","mode":"MODE","target":"OBJECTIF","game":"PARTIE",
 "types_all":"TYPES : TOUS","gen_all":"GÉN. : TOUTES","start":"LANCER","restart":"LANCER","launch":"DÉMARRER",
 "high":"Au-dessus de","low":"En dessous de","closest":"Au plus proche de","random_target":"ALÉA","current":"POKÉMON ACTUEL","ready":"Prêt à jouer ?",
 "team":"COMPOSITION DE L'ÉQUIPE","recap":"RÉCAPITULATIF","choose":"CHOISIR","selected":"VALIDÉE",
 "configure":"Configure la partie, puis clique sur Démarrer.","loading_list":"Chargement de la liste des Pokémon...",
 "preparing":"Préparation du tirage de 10 Pokémon...","shuffling":"Mélange en cours...","drawing":"Tirage aléatoire en cours...",
 "drawn":"Pokémon tiré ! Mode connaissances : valeurs masquées.","my_team":"MON ÉQUIPE","best":"MEILLEUR POSSIBLE",
 "minimum":"MINIMUM POSSIBLE","total":"TOTAL","global_gap":"ÉCART GLOBAL","optimal_team":"ÉQUIPE OPTIMALE",
 "my_choice":"MON CHOIX","optimal_combo":"Combo optimal","same_combo":"✓ CHOIX IDENTIQUE AU COMBO",
 "different":"Répartition différente","best_stat":"Meilleure stat","lowest":"Plus faible","gap":"écart",
 "close":"FERMER","image_unavailable":"IMAGE\nINDISPONIBLE","all_check":"TOUT COCHER","all_uncheck":"TOUT DÉCOCHER","validate":"VALIDER",
 "allowed_types":"TYPES AUTORISÉS","allowed_gen":"GÉNÉRATIONS AUTORISÉES","select_types":"Un Pokémon peut correspondre à n'importe lequel des types cochés.",
 "select_gen":"Sélectionne une ou plusieurs générations.","generation":"Génération","filter_type":"Filtre par type","filter_gen":"Filtre par génération",
 "victory":"VICTOIRE !","defeat":"DÉFAITE","target_gap":"ÉCART À L’OBJECTIF","closest_best":"PLUS PROCHE POSSIBLE","final":"Total final","open_recap":"Ouvre le récapitulatif ou recommence.",
 "not_enough":"Pas assez de Pokémon","not_enough_msg":"Ce filtre ne contient pas assez de Pokémon.","error":"Erreur","connection":"Erreur de connexion.",
 "connection_msg":"Impossible de récupérer les données.","type_required":"Type requis","gen_required":"Génération requise","select_one_type":"Sélectionne au moins un type.",
 "select_one_gen":"Sélectionne au moins une génération.","bad_target":"Objectif incorrect","bad_target_msg":"Saisis un objectif entier supérieur à 0.","choices":"CHOIX","preload":"CHARGER","preloading":"CHARGEMENT...","loaded":"PRÊT","reload":"RECHARGER","preload_first":"Charge les Pokémon avant de démarrer.","preload_done":"Pokémon chargés : la partie peut démarrer."},
 "en": {"types":"TYPES","generations":"GENERATIONS","language":"LANGUAGE","mode":"MODE","target":"TARGET","game":"GAME",
 "types_all":"TYPES: ALL","gen_all":"GEN: ALL","start":"LAUNCH","restart":"LAUNCH","launch":"START","high":"Above","low":"Below","closest":"Closest to","random_target":"RANDOM",
 "current":"CURRENT POKÉMON","ready":"Ready to play?","team":"TEAM COMPOSITION","recap":"SUMMARY","choose":"CHOOSE","selected":"SELECTED",
 "configure":"Configure the game, then click Start.","loading_list":"Loading Pokémon list...","preparing":"Preparing the 10-Pokémon draw...",
 "shuffling":"Shuffling...","drawing":"Random draw in progress...","drawn":"Pokémon drawn! Knowledge mode: values hidden.",
 "my_team":"MY TEAM","best":"BEST POSSIBLE","minimum":"MINIMUM POSSIBLE","total":"TOTAL","global_gap":"OVERALL GAP","optimal_team":"OPTIMAL TEAM",
 "my_choice":"MY CHOICE","optimal_combo":"Optimal combo","same_combo":"✓ SAME CHOICE AS COMBO","different":"Different assignment",
 "best_stat":"Best stat","lowest":"Lowest","gap":"gap","close":"CLOSE","image_unavailable":"IMAGE\nUNAVAILABLE","all_check":"SELECT ALL",
 "all_uncheck":"CLEAR ALL","validate":"APPLY","allowed_types":"ALLOWED TYPES","allowed_gen":"ALLOWED GENERATIONS",
 "select_types":"A Pokémon may match any selected type.","select_gen":"Select one or more generations.","generation":"Generation",
 "filter_type":"Type filter","filter_gen":"Generation filter","victory":"VICTORY!","defeat":"DEFEAT","target_gap":"TARGET GAP","closest_best":"CLOSEST POSSIBLE","final":"Final total",
 "open_recap":"Open the summary or restart.","not_enough":"Not enough Pokémon","not_enough_msg":"This filter does not contain enough Pokémon.",
 "error":"Error","connection":"Connection error.","connection_msg":"Unable to retrieve data.","type_required":"Type required",
 "gen_required":"Generation required","select_one_type":"Select at least one type.","select_one_gen":"Select at least one generation.",
 "bad_target":"Invalid target","bad_target_msg":"Enter an integer target greater than 0.","choices":"SELECTED","preload":"LOAD","preloading":"LOADING...","loaded":"READY","reload":"RELOAD","preload_first":"Load the Pokémon before starting.","preload_done":"Pokémon loaded: the game can start."}
}

# Special forms intentionally allowed in the shuffle. Purely cosmetic forms,
# Gigantamax, weather, seasonal, Unown and capped Pikachu forms are excluded.
REGIONAL_GENERATIONS = {"alola": 7, "galar": 8, "hisui": 8, "paldea": 9}
ROTOM_FORMS = {"rotom-heat", "rotom-wash", "rotom-frost", "rotom-fan", "rotom-mow"}
ORICORIO_FORMS = {"oricorio-pom-pom", "oricorio-pau", "oricorio-sensu"}
BATTLE_FORM_GENERATIONS = {
    "deoxys-attack": 3, "deoxys-defense": 3, "deoxys-speed": 3,
    "wormadam-sandy": 4, "wormadam-trash": 4, "giratina-origin": 4, "shaymin-sky": 4,
    "darmanitan-zen": 5, "tornadus-therian": 5, "thundurus-therian": 5,
    "landorus-therian": 5, "kyurem-black": 5, "kyurem-white": 5, "meloetta-pirouette": 5,
    "meowstic-female": 6, "aegislash-blade": 6, "zygarde-10": 6, "zygarde-complete": 6,
    "hoopa-unbound": 6, "greninja-ash": 6, "pumpkaboo-small": 6, "pumpkaboo-large": 6,
    "pumpkaboo-super": 6, "gourgeist-small": 6, "gourgeist-large": 6, "gourgeist-super": 6,
    "lycanroc-dusk": 7, "wishiwashi-school": 7, "minior-red-meteor": 7, "minior-red": 7,
    "necrozma-dusk": 7, "necrozma-dawn": 7, "necrozma-ultra": 7,
    "indeedee-female": 8, "basculegion-female": 8, "eiscue-noice": 8,
    "zacian-crowned": 8, "zamazenta-crowned": 8, "eternatus-eternamax": 8,
    "urshifu-rapid-strike": 8, "calyrex-ice": 8, "calyrex-shadow": 8,
    "oinkologne-female": 9, "palafin-hero": 9, "ursaluna-bloodmoon": 9,
    "ogerpon-wellspring-mask": 9, "ogerpon-hearthflame-mask": 9,
    "ogerpon-cornerstone-mask": 9, "terapagos-terastal": 9, "terapagos-stellar": 9,
}
EXCLUDED_FORM_TOKENS = ("gmax", "gigantamax", "cap", "cosplay", "rock-star", "belle",
                        "pop-star", "phd", "libre", "starter", "totem")
EXCLUDED_FORM_PREFIXES = ("unown-", "castform-", "cherrim-", "deerling-", "sawsbuck-")
FORM_FALLBACK_LABELS = {
    "fr": {"alola": "d’Alola", "galar": "de Galar", "hisui": "de Hisui", "paldea": "de Paldea",
           "mega": "Méga", "mega-x": "Méga X", "mega-y": "Méga Y", "heat": "Chaleur",
           "wash": "Lavage", "frost": "Froid", "fan": "Hélice", "mow": "Tonte",
           "pom-pom": "Pom-Pom", "pau": "Hula", "sensu": "Buyō"},
    "en": {"alola": "Alolan", "galar": "Galarian", "hisui": "Hisuian", "paldea": "Paldean",
           "mega": "Mega", "mega-x": "Mega X", "mega-y": "Mega Y", "heat": "Heat",
           "wash": "Wash", "frost": "Frost", "fan": "Fan", "mow": "Mow",
           "pom-pom": "Pom-Pom", "pau": "Pa'u", "sensu": "Sensu"},
}


def special_form_generation(name: str):
    if any(token in name for token in EXCLUDED_FORM_TOKENS) or name.startswith(EXCLUDED_FORM_PREFIXES):
        return None
    if "-mega" in name:
        return 6
    for region, generation in REGIONAL_GENERATIONS.items():
        if f"-{region}" in name:
            return generation
    if name in ROTOM_FORMS:
        return 4
    if name in ORICORIO_FORMS:
        return 7
    return BATTLE_FORM_GENERATIONS.get(name)


def fallback_form_names(api_name: str, base_fr: str, base_en: str):
    if api_name.startswith("rotom-"):
        form = api_name.split("-", 1)[1]
        return {"fr": f"{base_fr} {FORM_FALLBACK_LABELS['fr'].get(form, pretty_name(form))}",
                "en": f"{FORM_FALLBACK_LABELS['en'].get(form, pretty_name(form))} {base_en}"}
    if api_name.startswith("oricorio-"):
        form = api_name.split("-", 1)[1]
        return {"fr": f"{base_fr} Style {FORM_FALLBACK_LABELS['fr'].get(form, pretty_name(form))}",
                "en": f"{FORM_FALLBACK_LABELS['en'].get(form, pretty_name(form))} Style {base_en}"}
    mega_match = re.search(r"-(mega(?:-x|-y)?)$", api_name)
    if mega_match:
        form = mega_match.group(1)
        return {"fr": f"{FORM_FALLBACK_LABELS['fr'][form]}-{base_fr}",
                "en": f"{FORM_FALLBACK_LABELS['en'][form]} {base_en}"}
    for region in REGIONAL_GENERATIONS:
        token = f"-{region}"
        if token in api_name:
            extra = api_name.split(token, 1)[1].strip("-")
            fr = f"{base_fr} {FORM_FALLBACK_LABELS['fr'][region]}"
            en = f"{FORM_FALLBACK_LABELS['en'][region]} {base_en}"
            if extra:
                fr += f" ({pretty_name(extra)})"
                en += f" ({pretty_name(extra)})"
            return {"fr": fr, "en": en}
    species_slug = api_name.split("-", 1)[0]
    label = pretty_name(api_name[len(species_slug):].strip("-"))
    return {"fr": f"{base_fr} ({label})", "en": f"{base_en} ({label})"}


def get_json(url: str, cache_name: str) -> dict:
    path = CACHE / cache_name
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    request = urllib.request.Request(url, headers={"User-Agent": "PokemonStatDraft/2.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.load(response)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def pretty_name(name: str) -> str:
    # Supprime tout suffixe anglais entre parentheses pour garder un nom stable.
    clean = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
    return clean.replace("-", " ").title()


def get_bytes(url: str, cache_name: str) -> bytes:
    path = CACHE / cache_name
    if path.exists():
        try:
            return path.read_bytes()
        except OSError:
            pass
    request = urllib.request.Request(url, headers={"User-Agent": "PokemonStatDraft/3.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        content = response.read()
    path.write_bytes(content)
    return content


class PokemonStatDraft(tk.Toplevel):
    def __init__(self, master=None, on_home=None, language="fr"):
        super().__init__(master)
        self.on_home = on_home
        self.protocol("WM_DELETE_WINDOW", self._return_home)
        self.title("PokéStat Challenge - Draft")
        self.configure(bg=COLORS["bg"])
        self.minsize(560, 820)
        self.resizable(False, False)
        self.current = None
        self.pool = []
        self.used_pokemon = set()
        self.chosen = {}
        self.chosen_details = {}
        self.sprite = None
        self.recap_images = []
        self.busy = False
        self.language = language if language in ("fr", "en") else "fr"
        self.selected_generations = set(range(1, 10))
        self.selected_types = set(TYPE_KEYS)
        self.form_mode = "all"
        self.game_mode = "high"
        self.preloaded_sequences = []
        self.pending_name_sequences = []
        self.preload_signature = None
        self.next_sequence_loading = False
        self.waiting_for_next = False
        self._configure_styles()
        self._build_ui()
        self._update_language_buttons()
        self.after(80, self._fit_window)

    def _return_home(self):
        callback = self.on_home
        self.destroy()
        if callback:
            callback()

    def tr(self, key):
        return TEXT[self.language][key]

    def stat_label(self, key):
        return STAT_LABELS[self.language][key]

    def type_label(self, key):
        return TYPE_LABELS[self.language].get(key, pretty_name(key))

    def randomize_target(self):
        """Generate any integer target from 250 to 750, inclusive."""
        self.target_var.set(random.randint(250, 750))

    def mode_key(self):
        value = self.mode_var.get()
        if value == self.tr("low"):
            return "low"
        if value == self.tr("closest"):
            return "closest"
        return "high"

    def set_language(self, language):
        if language == self.language:
            return
        old_mode = self.mode_key()
        self.language = language
        self.mode_var.set(self.tr(old_mode))
        self.mode_box.config(values=[self.tr("high"), self.tr("low"), self.tr("closest")])
        self._update_language_buttons()
        self._translate_ui()

    def _update_language_buttons(self):
        pass

    def _translate_ui(self):
        labels = [(self.types_title,"types"),(self.generations_title,"generations"),
                  (self.mode_title,"mode"),(self.target_title,"target"),(self.game_title,"game"),
                  (self.current_title,"current"),(self.team_title,"team")]
        for widget, key in labels: widget.config(text=self.tr(key))
        self.type_button.config(text=self._type_button_text())
        self.generation_button.config(text=self._generation_button_text())
        if hasattr(self, "form_title"):
            self.form_title.config(text=self.form_tr("title"))
        if hasattr(self, "form_button"):
            self.form_button.config(text=self._form_button_text())
        if hasattr(self, "launch_title"):
            self.launch_title.config(text=self.tr("launch"))
        if hasattr(self, "random_target_button"):
            self.random_target_button.config(text=self.tr("random_target"))
        self.start_button.config(text=self.tr("start"))
        if hasattr(self, "preload_button"):
            preload_key = "loaded" if self.preloaded_sequences else "preload"
            self.preload_button.config(text=self.tr(preload_key))
        self.recap_button.config(text=self.tr("recap"))
        for key in STAT_ORDER:
            self.stat_name_labels[key].config(text=self.stat_label(key))
            if key not in self.chosen:
                self.stat_buttons[key].config(text=self.tr("choose"))
            else:
                self.stat_buttons[key].config(text=self.tr("selected"))
        total=sum(self.chosen.values()); self.header_score.config(text=f'{self.tr("total")}  {total}')
        if self.current:
            self._show_current_localized()
        else:
            self.name_label.config(text=self.tr("ready"))
        self.footer_text.config(text=self.tr("configure") if not self.current else self.tr("drawn"))

    def _type_button_text(self):
        if len(self.selected_types)==18: return self.tr("types_all")
        if len(self.selected_types)<=2: return " / ".join(self.type_label(k).upper() for k in sorted(self.selected_types))
        return f'{self.tr("types")} : {len(self.selected_types)} {self.tr("choices")}'

    def form_tr(self, key):
        return FORM_FILTER_TEXT[self.language][key]

    def _form_button_text(self):
        return self.form_tr(self.form_mode)

    def _generation_button_text(self):
        if len(self.selected_generations)==9: return self.tr("gen_all")
        if len(self.selected_generations)<=3: return "GEN: " + ", ".join(map(str,sorted(self.selected_generations)))
        return f'GEN: {len(self.selected_generations)} {self.tr("choices")}'

    def _show_current_localized(self):
        name = self.current["names"].get(self.language) or self.current["names"].get("en")
        size = 18 if len(name)<=18 else 16 if len(name)<=25 else 14 if len(name)<=34 else 12
        self.name_label.config(text=name, font=("Segoe UI",size,"bold"))
        self._show_types(self.current["types"])

    def _fit_window(self):
        """Format vertical 9:16, centre sur l'ecran pour un test type TikTok."""
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        height = min(1040, sh - 70)
        width = min(650, max(560, int(height * 9 / 16)))
        x, y = max(0, (sw - width) // 2), 0
        try:
            self.state("normal")
        except tk.TclError:
            pass
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", padding=8, fieldbackground="white", background="white",
                        foreground=COLORS["dark"], arrowcolor=COLORS["dark"])
        style.map("TCombobox", fieldbackground=[("readonly", "white")],
                  foreground=[("readonly", COLORS["dark"])], background=[("readonly", "white")])
        style.configure("TSpinbox", padding=8, fieldbackground="white", foreground=COLORS["dark"],
                        background="white", arrowcolor=COLORS["dark"])
        style.configure("Game.TCheckbutton", background=COLORS["panel"], foreground=COLORS["text"],
                        font=("Segoe UI", 10, "bold"), padding=5)
        style.map("Game.TCheckbutton", background=[("active", COLORS["panel"])],
                  foreground=[("active", "white")])

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg"], height=82)
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

        tk.Label(header, text="POKÉSTAT CHALLENGE", bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 17, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(header, text="← ACCUEIL", command=self._return_home,
                  bg=COLORS["panel"], fg="white", activebackground=COLORS["blue"],
                  activeforeground="white", relief="flat", bd=0, padx=8, pady=6,
                  font=("Segoe UI", 8, "bold"), cursor="hand2").place(x=12, y=4)

        self.header_score = tk.Label(header, text="TOTAL  0", bg=COLORS["red"], fg="white",
                                     padx=12, pady=8, font=("Segoe UI", 11, "bold"))
        self.header_score.place(relx=1.0, rely=0.5, x=-14, anchor="e")

        body = tk.Frame(self, bg=COLORS["bg"], padx=18, pady=0)
        body.pack(fill="both", expand=True)

        settings = tk.Frame(body, bg=COLORS["panel"], padx=14, pady=12)
        settings.pack(fill="x", pady=(0, 12))
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
                                     values=[self.tr("high"), self.tr("low"), self.tr("closest")], width=10)
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
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=0)
        content.rowconfigure(1, weight=1)

        self.pokemon_card = tk.Frame(content, bg=COLORS["card"], padx=22, pady=11)
        self.pokemon_card.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
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
        self.sprite_box = tk.Frame(self.pokemon_card, bg="white", width=500, height=220)
        self.sprite_box.pack(pady=(0, 0))
        self.sprite_box.pack_propagate(False)
        self.sprite_label = tk.Label(self.sprite_box, bg="white", fg=COLORS["muted"], text="?",
                                     font=("Segoe UI", 55, "bold"), bd=0)
        self.sprite_label.place(x=0, y=0, width=500, height=220)

        stats_card = tk.Frame(content, bg=COLORS["card"], padx=18, pady=16)
        stats_card.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        title_line = tk.Frame(stats_card, bg="white")
        title_line.pack(fill="x", pady=(0, 10))
        self.team_title = tk.Label(title_line, text=self.tr("team"), bg="white", fg=COLORS["dark"],
                 font=("Segoe UI", 14, "bold"))
        self.team_title.pack(side="left")
        self.progress_label = tk.Label(title_line, text="0 / 6", bg=COLORS["soft"], fg=COLORS["blue"],
                                       padx=10, pady=5, font=("Segoe UI", 10, "bold"))
        self.progress_label.pack(side="right")
        self.recap_button = tk.Button(title_line, text=self.tr("recap"), command=self.show_recap,
                                      state="disabled", bg=COLORS["blue"], fg="white",
                                      disabledforeground="#94a3b8", relief="flat", bd=0,
                                      padx=9, pady=5, font=("Segoe UI", 8, "bold"), cursor="arrow")
        self.recap_button.pack(side="right", padx=(0, 7))

        self.stat_rows = {}
        self.stat_name_labels = {}
        self.value_labels = {}
        self.stat_buttons = {}
        for key in STAT_ORDER:
            row = tk.Frame(stats_card, bg=COLORS["soft"], padx=12, pady=6,
                           highlightbackground=COLORS["line"], highlightthickness=1)
            row.pack(fill="x", pady=3)
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
                               cursor="hand2", padx=12, pady=6, font=("Segoe UI", 9, "bold"))
            button.pack(side="right")
            self.stat_rows[key], self.stat_name_labels[key], self.value_labels[key], self.stat_buttons[key] = row, label, value, button

        # Keep the original footer height and dark visual separation, but without visible text.
        footer = tk.Frame(body, bg=COLORS["bg"], height=34)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        self.footer_text = tk.Label(footer, text="", bg=COLORS["bg"], fg=COLORS["bg"])
        self.footer_text.pack(fill="both", expand=True)
        self.status = self.footer_text

    def _setting_label(self, parent, text, column):
        tk.Label(parent, text=text, bg=COLORS["panel"], fg="#94a3b8",
                 font=("Segoe UI", 8, "bold")).grid(row=0, column=column, sticky="w", pady=(0, 4))

    def open_form_filter(self):
        popup = tk.Toplevel(self)
        popup.title(self.form_tr("popup"))
        popup.configure(bg=COLORS["bg"])
        popup.transient(self)
        popup.resizable(False, False)
        popup.withdraw()
        tk.Label(popup, text=self.form_tr("heading"), bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 15, "bold")).pack(padx=28, pady=(20, 12))
        value = tk.StringVar(value=self.form_mode)
        box = tk.Frame(popup, bg=COLORS["panel"], padx=18, pady=14)
        box.pack(padx=20)
        for key, label in [("standard", self.form_tr("standard_choice")),
                           ("mega", self.form_tr("mega_choice")),
                           ("all", self.form_tr("all_choice"))]:
            tk.Radiobutton(box, text=label, variable=value, value=key,
                           bg=COLORS["panel"], fg="white", selectcolor=COLORS["dark"],
                           activebackground=COLORS["panel"], activeforeground="white",
                           anchor="w", font=("Segoe UI", 9, "bold")).pack(fill="x", pady=5)
        tk.Button(popup, text=self.form_tr("apply"),
                  command=lambda: self.apply_form_filter(popup, value.get()),
                  bg=COLORS["blue"], fg="white", relief="flat", bd=0,
                  padx=24, pady=9, font=("Segoe UI", 9, "bold")).pack(pady=16)
        popup.update_idletasks()
        width, height = popup.winfo_reqwidth(), popup.winfo_reqheight()
        x = self.winfo_rootx() + max(0, (self.winfo_width() - width) // 2)
        y = self.winfo_rooty() + 110
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.deiconify(); popup.lift(self); popup.focus_force(); popup.grab_set()

    def apply_form_filter(self, popup, value):
        self.form_mode = value
        self.form_button.config(text=self._form_button_text())
        popup.destroy()
        self._invalidate_preload()

    def open_generation_filter(self):
        roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
                 6: "VI", 7: "VII", 8: "VIII", 9: "IX"}
        items = [(number, f"{self.tr('generation')} {roman[number]}") for number in range(1, 10)]
        self._open_multi_filter(
            title=self.tr("filter_gen"),
            heading=self.tr("allowed_gen"),
            subtitle=self.tr("select_gen"),
            items=items,
            selected=set(self.selected_generations),
            apply_callback=self.apply_generation_filter,
            visible_rows=9,
        )

    def open_type_filter(self):
        items = [(key, self.type_label(key)) for key in TYPE_KEYS]
        self._open_multi_filter(
            title=self.tr("filter_type"),
            heading=self.tr("allowed_types"),
            subtitle=self.tr("select_types"),
            items=items,
            selected=set(self.selected_types),
            apply_callback=self.apply_type_filter,
            visible_rows=10,
        )

    def _open_multi_filter(self, title, heading, subtitle, items, selected,
                           apply_callback, visible_rows):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.configure(bg=COLORS["bg"])
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)

        is_type_filter = len(items) > 10
        width = 430 if is_type_filter else 390
        content_rows = (len(items) + 1) // 2 if is_type_filter else len(items)
        height = min(popup.winfo_screenheight() - 35, 205 + content_rows * 39)
        x = self.winfo_x() + max(0, (self.winfo_width() - width) // 2)
        popup.geometry(f"{width}x{height}+{x}+0")

        tk.Label(popup, text=heading, bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 16, "bold")).pack(pady=(15, 3))
        tk.Label(popup, text=subtitle, bg=COLORS["bg"], fg="#94a3b8",
                 wraplength=390, font=("Segoe UI", 9)).pack(pady=(0, 9))

        vars_by_key = {key: tk.BooleanVar(value=key in selected) for key, _ in items}
        choices = tk.Frame(popup, bg=COLORS["panel"], padx=12, pady=9)
        choices.pack(fill="both", expand=True, padx=18)
        columns = 2 if is_type_filter else 1
        rows_per_column = (len(items) + columns - 1) // columns
        for index, (key, label) in enumerate(items):
            row = index % rows_per_column
            column = index // rows_per_column
            check = tk.Checkbutton(choices, text=label, variable=vars_by_key[key],
                                   bg=COLORS["panel"], fg="white", selectcolor=COLORS["blue"],
                                   activebackground=COLORS["panel"], activeforeground="white",
                                   font=("Segoe UI", 10, "bold"), anchor="w", padx=10, pady=6)
            check.grid(row=row, column=column, sticky="ew", padx=4, pady=1)
        for column in range(columns):
            choices.columnconfigure(column, weight=1, uniform="checks")

        actions = tk.Frame(popup, bg=COLORS["bg"])
        actions.pack(fill="x", padx=18, pady=11)
        tk.Button(actions, text=self.tr("all_check"),
                  command=lambda: [variable.set(True) for variable in vars_by_key.values()],
                  bg="#334155", fg="white", relief="flat", padx=9, pady=8,
                  font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Button(actions, text=self.tr("all_uncheck"),
                  command=lambda: [variable.set(False) for variable in vars_by_key.values()],
                  bg="#334155", fg="white", relief="flat", padx=9, pady=8,
                  font=("Segoe UI", 8, "bold")).pack(side="left", padx=6)
        tk.Button(actions, text=self.tr("validate"),
                  command=lambda: apply_callback(popup, vars_by_key),
                  bg=COLORS["red"], fg="white", relief="flat", padx=15, pady=8,
                  font=("Segoe UI", 9, "bold")).pack(side="right")

    def apply_generation_filter(self, popup, vars_by_key):
        selected = {key for key, variable in vars_by_key.items() if variable.get()}
        if not selected:
            messagebox.showwarning(self.tr("gen_required"), self.tr("select_one_gen"), parent=popup)
            return
        self.selected_generations = selected
        self._invalidate_preload()
        if len(selected) == 9:
            label = self.tr("gen_all")
        elif len(selected) <= 3:
            label = "GEN: " + ", ".join(str(number) for number in sorted(selected))
        else:
            label = self._generation_button_text()
        self.generation_button.config(text=label)
        popup.destroy()

    def apply_type_filter(self, popup, vars_by_key):
        selected = {key for key, variable in vars_by_key.items() if variable.get()}
        if not selected:
            messagebox.showwarning(self.tr("type_required"), self.tr("select_one_type"), parent=popup)
            return
        self.selected_types = selected
        self._invalidate_preload()
        if len(selected) == 18:
            label = self.tr("types_all")
        elif len(selected) <= 2:
            label = " / ".join(self.type_label(key).upper() for key in sorted(selected))
        else:
            label = self._type_button_text()
        self.type_button.config(text=label)
        popup.destroy()

    def _invalidate_preload(self):
        self.preloaded_sequences = []
        self.pending_name_sequences = []
        self.preload_signature = None
        self.next_sequence_loading = False
        self.waiting_for_next = False
        if hasattr(self, "preload_button"):
            self.preload_button.config(text=self.tr("preload"), state="normal", cursor="hand2")
            self.start_button.config(state="disabled", bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"], disabledforeground="#fecaca", cursor="arrow")

    def _current_filter_signature(self):
        return (frozenset(self.selected_types), frozenset(self.selected_generations), self.form_mode)

    def _prepare_sequence(self, names):
        prepared = {}
        workers = min(10, max(1, len(set(names))))
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_by_name = {executor.submit(self._prepare_pokemon, name): name
                              for name in set(names)}
            for future in concurrent.futures.as_completed(future_by_name):
                name = future_by_name[future]
                prepared[name] = future.result()
        return [prepared[name] for name in names]

    def preload_pokemon(self):
        """Prepare only round one; the following rounds stream in the background."""
        if self.busy:
            return
        if not self.selected_generations:
            messagebox.showerror(self.tr("gen_required"), self.tr("select_one_gen"))
            return
        if not self.selected_types:
            messagebox.showerror(self.tr("type_required"), self.tr("select_one_type"))
            return

        selected_types = set(self.selected_types)
        generations = set(self.selected_generations)
        signature = self._current_filter_signature()
        self._invalidate_preload()
        self.preload_button.config(text=self.tr("preloading"), state="disabled", cursor="arrow")

        def job():
            pool = self._load_pool(selected_types, generations)
            if len(pool) < 6:
                raise ValueError(self.tr("not_enough_msg"))

            # Six distinct final Pokémon are fixed now, while preview Pokémon may repeat.
            finals = random.sample(pool, 6)
            name_sequences = []
            for final_name in finals:
                previews = [name for name in pool if name != final_name]
                sequence = random.sample(previews, min(9, len(previews))) + [final_name]
                name_sequences.append(sequence)

            first_sequence = self._prepare_sequence(name_sequences[0])
            return pool, first_sequence, name_sequences[1:], signature

        self._run_async(job, self._preload_complete, error_callback=self._preload_failed)

    def _preload_complete(self, result):
        self.pool, first_sequence, self.pending_name_sequences, self.preload_signature = result
        self.preloaded_sequences = [first_sequence]
        self.preload_button.config(text=self.tr("loaded"), state="disabled", cursor="arrow")
        self.start_button.config(state="normal", bg=COLORS["green"], fg="white", activebackground="#15803d", activeforeground="white", cursor="hand2")

    def _preload_failed(self, exc):
        self._invalidate_preload()
        messagebox.showerror(self.tr("error"), f"{self.tr('connection_msg')}\n\n{exc}")

    def _ensure_next_sequence(self):
        """Keep exactly one future round ready while the player watches the current one."""
        if self.next_sequence_loading or self.preloaded_sequences or not self.pending_name_sequences:
            return
        self.next_sequence_loading = True
        names = list(self.pending_name_sequences[0])

        def complete(sequence):
            self.next_sequence_loading = False
            if self.pending_name_sequences:
                self.pending_name_sequences.pop(0)
            self.preloaded_sequences.append(sequence)
            if self.waiting_for_next:
                self.waiting_for_next = False
                self.next_pokemon()

        def failed(exc):
            self.next_sequence_loading = False
            self.waiting_for_next = False
            messagebox.showerror(self.tr("error"), f"{self.tr('connection_msg')}\n\n{exc}")

        self._run_async(lambda: self._prepare_sequence(names), complete,
                        quiet=True, error_callback=failed)

    def start_game(self):
        if self.busy:
            return
        if not self.preloaded_sequences or self.preload_signature != self._current_filter_signature():
            messagebox.showinfo(self.tr("game"), self.tr("preload_first"))
            self.start_button.config(state="disabled", bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"], disabledforeground="#fecaca", cursor="arrow")
            self.preload_button.config(text=self.tr("preload"), state="normal", cursor="hand2")
            return
        if not self.selected_generations:
            messagebox.showerror(self.tr("gen_required"), self.tr("select_one_gen"))
            return
        if not self.selected_types:
            messagebox.showerror(self.tr("type_required"), self.tr("select_one_type"))
            return
        try:
            if int(self.target_var.get()) <= 0:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror(self.tr("bad_target"), self.tr("bad_target_msg"))
            return
        self.chosen.clear()
        self.chosen_details.clear()
        self.recap_button.config(state="disabled", bg=COLORS["blue"], cursor="arrow")
        self.used_pokemon.clear()
        self.current = None
        self.start_button.config(text=self.tr("start"), bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"], disabledforeground="#fecaca")
        self.header_score.config(bg=COLORS["red"])
        self._refresh_board()
        self.status.config(text="")
        self.game_mode = self.mode_key()
        self.preload_button.config(state="disabled", cursor="arrow")
        self.start_button.config(state="disabled", bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"], disabledforeground="#fecaca", cursor="arrow")
        self.next_pokemon()

    def _load_pool(self, selected_types, generations):
        generation_names = set()
        for number in sorted(generations):
            data = get_json(f"{API}/generation/{number}", f"generation_{number}.json")
            generation_names.update(item["name"] for item in data.get("pokemon_species", []))

        type_names = set()
        for selected_type in sorted(selected_types):
            type_data = get_json(f"{API}/type/{selected_type}", f"type_{selected_type}.json")
            type_names.update(item["pokemon"]["name"] for item in type_data["pokemon"])

        standard_pool = generation_names & type_names
        pokemon_index = get_json(f"{API}/pokemon?limit=100000&offset=0", "pokemon_all_forms.json")
        mega_pool = {
            item["name"] for item in pokemon_index.get("results", [])
            if "-mega" in item["name"]
            and special_form_generation(item["name"]) in generations
            and item["name"] in type_names
        }
        if self.form_mode == "standard":
            return sorted(standard_pool)
        if self.form_mode == "mega":
            return sorted(mega_pool)
        return sorted(standard_pool | mega_pool)

    def _pool_loaded(self, pool):
        self.pool = pool
        if len(pool) < 6:
            messagebox.showerror(self.tr("not_enough"), self.tr("not_enough_msg"))
            return
        self.next_pokemon()

    def next_pokemon(self):
        if not self.preloaded_sequences:
            # Usually invisible: only used when a player chooses faster than the background load.
            self.waiting_for_next = True
            self.current = None
            self.name_label.config(text=self.tr("preloading"))
            self._show_types([])
            self._set_buttons(False)
            self._ensure_next_sequence()
            return

        pokemon_sequence = self.preloaded_sequences.pop(0)
        self.name_label.config(text=self.tr("shuffling"))
        self._show_types([])
        self._set_buttons(False)
        self._start_shuffle(pokemon_sequence)

        # Start preparing the following round during this shuffle and the thinking time.
        self._ensure_next_sequence()

    def _prepare_pokemon(self, name):
        data = get_json(f"{API}/pokemon/{name}", f"pokemon_{name}.json")
        stats = {item["stat"]["name"]: item["base_stat"] for item in data["stats"]}
        english_name = pretty_name(data["name"])
        species_name = data.get("species", {}).get("name", name)
        species = get_json(f"{API}/pokemon-species/{species_name}", f"species_{species_name}.json")
        french_name = next((item["name"] for item in species.get("names", [])
                            if item.get("language", {}).get("name") == "fr"), english_name)
        official_english = next((item["name"] for item in species.get("names", [])
                                 if item.get("language", {}).get("name") == "en"), english_name)
        localized_names = {"fr": french_name, "en": official_english}
        if special_form_generation(name) is not None:
            localized_names = fallback_form_names(name, french_name, official_english)
            try:
                form_name = data.get("forms", [{}])[0].get("name", name)
                form_data = get_json(f"{API}/pokemon-form/{form_name}", f"form_{form_name}.json")
                form_names = {item.get("language", {}).get("name"): item.get("name")
                              for item in form_data.get("names", []) if item.get("name")}
                localized_names["fr"] = form_names.get("fr", localized_names["fr"])
                localized_names["en"] = form_names.get("en", localized_names["en"])
            except Exception:
                pass
        sprites = data.get("sprites", {})
        sprite_url = (
            sprites.get("other", {}).get("official-artwork", {}).get("front_default")
            or sprites.get("other", {}).get("home", {}).get("front_default")
            or sprites.get("front_default")
        )
        sprite_raw = get_bytes(sprite_url, f"artwork_{name}.png") if sprite_url else None
        return {
            "api_name": name,
            "names": localized_names,
            "stats": stats,
            "types": [item["type"]["name"] for item in data["types"]],
            "sprite_raw": sprite_raw,
        }

    def _start_shuffle(self, pokemon_sequence):
        self.status.config(text="")
        self._shuffle_frame(pokemon_sequence, 0)

    def _shuffle_frame(self, pokemon_sequence, index):
        pokemon = pokemon_sequence[index]
        display_name = pokemon["names"].get(self.language) or pokemon["names"]["en"]
        length = len(display_name)
        font_size = 18 if length <= 18 else 16 if length <= 25 else 14 if length <= 34 else 12
        self.name_label.config(text=display_name, font=("Segoe UI", font_size, "bold"))
        self._show_types(pokemon["types"])
        self._display_sprite_bytes(pokemon["sprite_raw"])
        delays = [90, 90, 100, 100, 110, 120, 140, 170, 220, 0]
        if index < len(pokemon_sequence) - 1:
            self.after(delays[index], lambda: self._shuffle_frame(pokemon_sequence, index + 1))
        else:
            self.current = pokemon
            self.used_pokemon.add(pokemon["api_name"])
            self._refresh_current_stats()
            self._set_buttons(True)
            text = self.tr("drawn")
            self.status.config(text="")

    def _display_sprite_bytes(self, raw):
        """Affiche chaque sprite dans un cadre visuel constant, sans variation de taille."""
        self.sprite = None
        if not raw:
            self.sprite_label.config(image="", text="?")
            return
        try:
            # Pillow allows transparent-margin cropping and smoother scaling.
            image = Image.open(io.BytesIO(raw)).convert("RGBA")
            alpha_box = image.getchannel("A").getbbox()
            if alpha_box:
                image = image.crop(alpha_box)

            # Normalize visible height. Wide Pokémon can use the available width.
            target_height = 205
            if image.height > 0:
                scale = target_height / image.height
                target_width = max(1, round(image.width * scale))
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

            self.sprite = ImageTk.PhotoImage(image)
            self.sprite_label.config(image=self.sprite, text="")
        except tk.TclError:
            self.sprite_label.config(
                image="", text=self.tr("image_unavailable").replace("\n", " "))

    def _show_types(self, types):
        for widget in self.types_frame.winfo_children():
            widget.destroy()
        if not types:
            return

        # Le groupe complet est centre, qu'il contienne un ou deux types.
        group = tk.Frame(self.types_frame, bg="white")
        group.place(relx=0.5, rely=0.5, anchor="center")
        for type_name in types:
            color = TYPE_COLORS.get(type_name, COLORS["muted"])
            badge = tk.Frame(group, bg=color, padx=8, pady=4)
            badge.pack(side="left", padx=4)
            tk.Label(badge, text=TYPE_ICONS.get(type_name, "●"),
                     bg=color, fg="white",
                     font=("Segoe UI Symbol", 12, "bold")).pack(side="left", padx=(0, 5))
            tk.Label(badge, text=self.type_label(type_name).upper(),
                     bg=color, fg="white",
                     font=("Segoe UI", 8, "bold")).pack(side="left")

    def _refresh_current_stats(self):
        for key in STAT_ORDER:
            if key in self.chosen:
                self.value_labels[key].config(text=str(self.chosen[key]), fg=COLORS["dark"])
            elif self.current:
                shown = "?"
                self.value_labels[key].config(text=shown, fg=COLORS["muted"])
            else:
                self.value_labels[key].config(text="—", fg=COLORS["muted"])

    def choose_stat(self, key):
        if not self.current or key in self.chosen or self.busy:
            return
        value = self.current["stats"][key]
        self.chosen[key] = value
        self.chosen_details[key] = {
            "names": dict(self.current["names"]),
            "types": list(self.current["types"]),
            "value": value,
            "chosen_stat": key,
            "all_stats": dict(self.current["stats"]),
            "sprite_raw": self.current.get("sprite_raw"),
        }
        self._refresh_board()
        if len(self.chosen) == 6:
            self.finish_game()
        else:
            self.next_pokemon()

    def _refresh_board(self):
        total = sum(self.chosen.values())
        self.header_score.config(text=f"{self.tr('total')}  {total}")
        self.progress_label.config(text=f"{len(self.chosen)} / 6")
        for key in STAT_ORDER:
            row, value, button = self.stat_rows[key], self.value_labels[key], self.stat_buttons[key]
            if key in self.chosen:
                row.config(bg=COLORS["locked"])
                for child in row.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=COLORS["locked"])
                value.config(text=str(self.chosen[key]), fg=COLORS["dark"])
                button.config(text=self.tr("selected"), state="disabled", bg=COLORS["locked"])
            else:
                row.config(bg=COLORS["soft"])
                for child in row.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=COLORS["soft"])
                value.config(text="—", fg=COLORS["muted"])
                button.config(text=self.tr("choose"), state="disabled", bg=COLORS["blue"])
        self._refresh_current_stats()

    def finish_game(self):
        total, target = sum(self.chosen.values()), int(self.target_var.get())
        mode = self.mode_key()
        target_gap = abs(total - target)
        if mode == "closest":
            won = target_gap <= 20
        elif mode == "high":
            won = total >= target
        else:
            won = total <= target
        verdict = self.tr("victory") if won else self.tr("defeat")
        # Keep the score badge compact so it never covers the Recap button.
        # Detailed result information is shown in the status line and recap.
        result_symbol = "✓" if won else "✕"
        self.header_score.config(
            text=f"{result_symbol}  {self.tr('total')} {total}",
            bg=COLORS["green"] if won else COLORS["red"],
        )
        if mode == "closest":
            self.status.config(
                text=f"{verdict} · {self.tr('target_gap')} : {target_gap}",
                fg=COLORS["green"] if won else COLORS["red"],
            )
        else:
            self.status.config(
                text=verdict,
                fg=COLORS["green"] if won else COLORS["red"],
            )
        self._set_buttons(False)
        self.recap_button.config(state="normal", bg=COLORS["blue"], cursor="hand2")
        self.preload_signature = None
        self.preloaded_sequences = []
        self.pending_name_sequences = []
        self.waiting_for_next = False
        self.preload_button.config(text=self.tr("reload"), state="normal", cursor="hand2")
        self.start_button.config(text=self.tr("start"), state="disabled", bg=COLORS["red"], fg="white", activebackground=COLORS["red_hover"], disabledforeground="#fecaca", cursor="arrow")

    def _calculate_optimal_team(self):
        """Teste les 720 répartitions valides des six stats entre les six Pokémon."""
        pokemon_details = [self.chosen_details[key] for key in STAT_ORDER]
        mode = self.game_mode
        target = int(self.target_var.get())
        best_total = None
        best_assignment = None
        best_distance = None

        # Une permutation attribue exactement une stat à chaque Pokémon,
        # et utilise chacune des six catégories une seule fois.
        for assignment in itertools.permutations(STAT_ORDER):
            total = sum(detail["all_stats"][stat_key]
                        for detail, stat_key in zip(pokemon_details, assignment))
            if mode == "closest":
                distance = abs(total - target)
                better = (best_distance is None or distance < best_distance or
                          (distance == best_distance and total > best_total))
            elif mode == "low":
                distance = None
                better = best_total is None or total < best_total
            else:
                distance = None
                better = best_total is None or total > best_total
            if better:
                best_total = total
                best_assignment = assignment
                best_distance = distance

        return pokemon_details, best_assignment, best_total

    def show_recap(self):
        """Compare l'équipe créée à la meilleure composition globale possible."""
        if len(self.chosen_details) != 6:
            return

        pokemon_details, optimal_assignment, optimal_total = self._calculate_optimal_team()
        player_total = sum(self.chosen.values())
        low_mode = self.game_mode == "low"
        closest_mode = self.game_mode == "closest"
        target = int(self.target_var.get())
        if closest_mode:
            gap = abs(player_total - target)
        else:
            gap = player_total - optimal_total if low_mode else optimal_total - player_total

        popup = tk.Toplevel(self)
        popup.title(self.tr("recap"))
        popup.configure(bg=COLORS["bg"])
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)

        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        self.update_idletasks()

        # Le récapitulatif ne dépasse jamais la largeur de la fenêtre principale.
        main_width = max(520, self.winfo_width())
        width = min(main_width, screen_w - 30)
        height = min(940, screen_h - 10)
        x = max(0, self.winfo_x() + (self.winfo_width() - width) // 2)
        popup.geometry(f"{width}x{height}+{x}+0")

        header = tk.Frame(popup, bg=COLORS["bg"], padx=12, pady=9)
        header.pack(fill="x")
        header.columnconfigure(0, weight=1, uniform="scores")
        header.columnconfigure(1, weight=1, uniform="scores")

        left_score = tk.Frame(header, bg=COLORS["panel"], padx=10, pady=8)
        left_score.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        right_score = tk.Frame(header, bg=COLORS["panel"], padx=10, pady=8)
        right_score.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        tk.Label(left_score, text=self.tr("my_team"), bg=COLORS["panel"], fg="white",
                 font=("Segoe UI", 16, "bold")).pack()
        tk.Label(left_score, text=f"{self.tr('total')} : {player_total}", bg=COLORS["panel"],
                 fg=COLORS["gold"], font=("Segoe UI", 11, "bold")).pack()

        optimal_title = (self.tr("closest_best") if closest_mode
                         else self.tr("minimum") if low_mode else self.tr("best"))
        tk.Label(right_score, text=optimal_title, bg=COLORS["panel"], fg="white",
                 font=("Segoe UI", 16, "bold")).pack()
        tk.Label(right_score, text=f"{self.tr('total')} : {optimal_total}", bg=COLORS["panel"],
                 fg=COLORS["green"], font=("Segoe UI", 11, "bold")).pack()
        gap_text = (f"{self.tr('target_gap')} : {gap}" if closest_mode
                    else self.tr("optimal_team") if gap == 0
                    else f"{self.tr('global_gap')} : {gap}")
        tk.Label(right_score, text=gap_text, bg=COLORS["panel"],
                 fg=COLORS["green"] if gap == 0 else COLORS["red"],
                 font=("Segoe UI", 8, "bold")).pack(pady=(2, 0))

        list_frame = tk.Frame(popup, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=12)
        self.recap_images = []

        available = max(510, height - 170)
        card_height = max(92, min(122, available // 6 - 3))
        image_size = min(74, card_height - 10)

        for chosen_key, detail, optimal_key in zip(STAT_ORDER, pokemon_details, optimal_assignment):
            card = tk.Frame(list_frame, bg="white", height=card_height, padx=8, pady=5)
            card.pack(fill="x", pady=3)
            card.pack_propagate(False)

            image_box = tk.Frame(card, bg="white", width=82, height=card_height - 10)
            image_box.pack(side="left")
            image_box.pack_propagate(False)
            image_label = tk.Label(image_box, bg="white", fg=COLORS["muted"],
                                   text=self.tr("image_unavailable"),
                                   font=("Segoe UI", 7, "bold"), justify="center")
            image_label.place(relx=0.5, rely=0.5, anchor="center",
                              width=82, height=card_height - 10)
            raw = detail.get("sprite_raw")
            if raw:
                try:
                    recap_source = Image.open(io.BytesIO(raw)).convert("RGBA")
                    alpha_box = recap_source.getchannel("A").getbbox()
                    if alpha_box:
                        recap_source = recap_source.crop(alpha_box)
                    recap_source.thumbnail((image_size, image_size), Image.Resampling.LANCZOS)
                    recap_image = ImageTk.PhotoImage(recap_source)
                    image_label.config(image=recap_image, text="")
                    self.recap_images.append(recap_image)
                except (tk.TclError, OSError, ValueError):
                    pass

            choice_box = tk.Frame(card, bg=COLORS["soft"], width=112,
                                  height=card_height - 12)
            choice_box.pack(side="right", padx=(6, 0))
            choice_box.pack_propagate(False)
            tk.Label(choice_box,
                     text=f"{self.tr('my_choice')}\n{self.stat_label(chosen_key)}\n{detail['value']}",
                     bg=COLORS["soft"], fg=COLORS["blue"], justify="center",
                     wraplength=104, font=("Segoe UI", 9, "bold")).pack(
                         expand=True, fill="both")

            info = tk.Frame(card, bg="white")
            info.pack(side="left", fill="both", expand=True, padx=(8, 2))
            tk.Label(info, text=detail["names"].get(self.language) or detail["names"]["en"], bg="white", fg=COLORS["dark"],
                     anchor="w", font=("Segoe UI", 11, "bold")).pack(fill="x")
            tk.Label(info, text=" / ".join(self.type_label(t) for t in detail["types"]), bg="white",
                     fg=COLORS["muted"], anchor="w",
                     font=("Segoe UI", 8)).pack(fill="x")

            # 1) Optimum global : meilleure répartition valide sur les six Pokémon.
            optimal_value = detail["all_stats"][optimal_key]
            same_choice = chosen_key == optimal_key
            tk.Label(info,
                     text=f"{self.tr('optimal_combo')} : {self.stat_label(optimal_key)} ({optimal_value})",
                     bg="white", fg=COLORS["dark"], anchor="w", justify="left",
                     wraplength=280, font=("Segoe UI", 8, "bold")).pack(
                         fill="x", pady=(2, 0))

            # 2) Optimum individuel : meilleure ou plus faible stat propre au Pokémon.
            if closest_mode:
                local_value = optimal_value
                local_keys = [optimal_key]
                local_label = self.tr("closest_best")
            else:
                local_value = (min(detail["all_stats"].values()) if low_mode
                               else max(detail["all_stats"].values()))
                local_keys = [stat_key for stat_key, stat_value in detail["all_stats"].items()
                              if stat_value == local_value]
                local_label = self.tr("lowest") if low_mode else self.tr("best_stat")
            local_names = " / ".join(self.stat_label(stat_key) for stat_key in local_keys)
            local_gap = (detail["value"] - local_value if low_mode
                         else local_value - detail["value"])
            if chosen_key in local_keys:
                local_gap_text = f"{self.tr('gap')} 0"
            else:
                local_gap_text = f"{self.tr('gap')} +{local_gap}" if low_mode else f"{self.tr('gap')} -{local_gap}"
            tk.Label(info,
                     text=self.tr("same_combo") if same_choice else self.tr("different"),
                     bg="white", fg=COLORS["green"] if same_choice else COLORS["red"],
                     anchor="w", font=("Segoe UI", 7, "bold")).pack(fill="x")

            local_line = tk.Label(
                info,
                text=f"{local_label} : {local_names} ({local_value}) • {local_gap_text}",
                bg="white", fg=COLORS["muted"], anchor="w", justify="left",
                wraplength=280, font=("Segoe UI", 8, "bold"), pady=1)
            local_line.pack(fill="x", pady=(0, 2))

        tk.Button(popup, text=self.tr("close"), command=popup.destroy,
                  bg=COLORS["red"], fg="white",
                  activebackground=COLORS["red_hover"], activeforeground="white",
                  relief="flat", bd=0, padx=28, pady=8,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(pady=6)

    def _set_buttons(self, enabled):
        for key, button in self.stat_buttons.items():
            if enabled and key not in self.chosen:
                button.config(state="normal", bg=COLORS["blue"], fg="white", cursor="hand2")
            else:
                button.config(state="disabled", cursor="arrow")

    def _run_async(self, job, callback, quiet=False, error_callback=None):
        if not quiet:
            self.busy = True
        def worker():
            try:
                result = job()
                self.after(0, lambda: done(result))
            except Exception as exc:
                self.after(0, lambda: failed(exc))
        def done(result):
            if not quiet:
                self.busy = False
            callback(result)
        def failed(exc):
            if not quiet:
                self.busy = False
                self.status.config(text="")
            if error_callback:
                error_callback(exc)
            else:
                messagebox.showerror(self.tr("error"), f"{self.tr('connection_msg')}\n\n{exc}")
        threading.Thread(target=worker, daemon=True).start()


