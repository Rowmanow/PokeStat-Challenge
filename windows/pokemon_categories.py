# -*- coding: utf-8 -*-
"""Filtres de catégories communs à Draft, Guesser et Stat Rush."""
from __future__ import annotations

import concurrent.futures
import re
import tkinter as tk

CATEGORY_ALL = "all"
CATEGORY_LEGENDARY_MYTHICAL = "legendary_mythical"
CATEGORY_STARTER_FAMILIES = "starter_families"
CATEGORY_FOSSILS = "fossils"
CATEGORY_PSEUDO_LEGENDARY = "pseudo_legendary"
CATEGORY_BABY = "baby"
CATEGORY_SINGLE_STAGE = "single_stage"

CATEGORY_ORDER = (
    CATEGORY_ALL,
    CATEGORY_LEGENDARY_MYTHICAL,
    CATEGORY_STARTER_FAMILIES,
    CATEGORY_FOSSILS,
    CATEGORY_PSEUDO_LEGENDARY,
    CATEGORY_BABY,
    CATEGORY_SINGLE_STAGE,
)

CATEGORY_LABELS = {
    "fr": {
        CATEGORY_ALL: "TOUS",
        CATEGORY_LEGENDARY_MYTHICAL: "LÉGENDAIRES + FABULEUX",
        CATEGORY_STARTER_FAMILIES: "FAMILLES DE STARTERS",
        CATEGORY_FOSSILS: "FOSSILES",
        CATEGORY_PSEUDO_LEGENDARY: "FAMILLES PSEUDO-LÉGENDAIRES",
        CATEGORY_BABY: "BÉBÉS POKÉMON",
        CATEGORY_SINGLE_STAGE: "SANS ÉVOLUTION",
        "title": "CATÉGORIES", "filter_title": "Filtre des catégories",
        "apply": "APPLIQUER", "none": "AUCUN", "count": "{n} CATÉGORIES",
    },
    "en": {
        CATEGORY_ALL: "ALL",
        CATEGORY_LEGENDARY_MYTHICAL: "LEGENDARY + MYTHICAL",
        CATEGORY_STARTER_FAMILIES: "STARTER FAMILIES",
        CATEGORY_FOSSILS: "FOSSILS",
        CATEGORY_PSEUDO_LEGENDARY: "PSEUDO-LEGENDARY FAMILIES",
        CATEGORY_BABY: "BABY POKÉMON",
        CATEGORY_SINGLE_STAGE: "SINGLE-STAGE POKÉMON",
        "title": "CATEGORIES", "filter_title": "Category filter",
        "apply": "APPLY", "none": "NONE", "count": "{n} CATEGORIES",
    },
}

# Familles complètes. Les Méga héritent automatiquement de l'espèce indiquée par PokéAPI.
STARTER_FAMILY_SPECIES = set("""
pichu pikachu raichu eevee vaporeon jolteon flareon espeon umbreon leafeon glaceon sylveon
bulbasaur ivysaur venusaur charmander charmeleon charizard squirtle wartortle blastoise
chikorita bayleef meganium cyndaquil quilava typhlosion totodile croconaw feraligatr
treecko grovyle sceptile torchic combusken blaziken mudkip marshtomp swampert
turtwig grotle torterra chimchar monferno infernape piplup prinplup empoleon
snivy servine serperior tepig pignite emboar oshawott dewott samurott
chespin quilladin chesnaught fennekin braixen delphox froakie frogadier greninja
rowlet dartrix decidueye litten torracat incineroar popplio brionne primarina
grookey thwackey rillaboom scorbunny raboot cinderace sobble drizzile inteleon
sprigatito floragato meowscarada fuecoco crocalor skeledirge quaxly quaxwell quaquaval
""".split())

FOSSIL_SPECIES = set("""
omanyte omastar kabuto kabutops aerodactyl lileep cradily anorith armaldo
cranidos rampardos shieldon bastiodon tirtouga carracosta archen archeops
tyrunt tyrantrum amaura aurorus dracozolt arctozolt dracovish arctovish
""".split())

PSEUDO_LEGENDARY_SPECIES = set("""
dratini dragonair dragonite larvitar pupitar tyranitar bagon shelgon salamence
beldum metang metagross gible gabite garchomp deino zweilous hydreigon
goomy sliggoo goodra jangmo-o hakamo-o kommo-o dreepy drakloak dragapult
frigibax arctibax baxcalibur
""".split())


def _chain_species(node):
    if not node:
        return set()
    result = {node.get("species", {}).get("name")}
    for child in node.get("evolves_to", []):
        result.update(_chain_species(child))
    result.discard(None)
    return result


def _cache_name_from_url(prefix, url):
    match = re.search(r"/(\d+)/?$", url or "")
    return f"{prefix}_{match.group(1)}.json" if match else f"{prefix}.json"


def categories_for_name(name, fetch_json, api):
    pokemon = fetch_json(f"{api}/pokemon/{name}", f"pokemon_{name}.json")
    species_name = pokemon.get("species", {}).get("name", name)
    species = fetch_json(f"{api}/pokemon-species/{species_name}",
                         f"species_{species_name}.json")
    categories = set()
    if species.get("is_legendary") or species.get("is_mythical"):
        categories.add(CATEGORY_LEGENDARY_MYTHICAL)
    if species.get("is_baby"):
        categories.add(CATEGORY_BABY)
    if species_name in STARTER_FAMILY_SPECIES:
        categories.add(CATEGORY_STARTER_FAMILIES)
    if species_name in FOSSIL_SPECIES:
        categories.add(CATEGORY_FOSSILS)
    if species_name in PSEUDO_LEGENDARY_SPECIES:
        categories.add(CATEGORY_PSEUDO_LEGENDARY)
    evolution_url = species.get("evolution_chain", {}).get("url")
    if evolution_url:
        chain_data = fetch_json(evolution_url, _cache_name_from_url("evolution_chain", evolution_url))
        if len(_chain_species(chain_data.get("chain", {}))) == 1:
            categories.add(CATEGORY_SINGLE_STAGE)
    return categories


def filter_pool_by_categories(names, selected_categories, fetch_json, api):
    names = list(dict.fromkeys(names))
    selected = set(selected_categories or {CATEGORY_ALL})
    if CATEGORY_ALL in selected or not selected:
        return names

    manual_selected = selected & {
        CATEGORY_STARTER_FAMILIES, CATEGORY_FOSSILS, CATEGORY_PSEUDO_LEGENDARY
    }
    dynamic_selected = selected & {
        CATEGORY_LEGENDARY_MYTHICAL, CATEGORY_BABY, CATEGORY_SINGLE_STAGE
    }

    def manual_species_name(name):
        # Les seules formes supplémentaires actuellement proposées sont les Méga.
        return re.sub(r"-mega(?:-[xyz])?$", "", name)

    def accepted(name):
        species_name = manual_species_name(name)
        if CATEGORY_STARTER_FAMILIES in manual_selected and species_name in STARTER_FAMILY_SPECIES:
            return True
        if CATEGORY_FOSSILS in manual_selected and species_name in FOSSIL_SPECIES:
            return True
        if CATEGORY_PSEUDO_LEGENDARY in manual_selected and species_name in PSEUDO_LEGENDARY_SPECIES:
            return True
        if not dynamic_selected:
            return False
        return bool(categories_for_name(name, fetch_json, api) & dynamic_selected)

    accepted_by_name = {}
    workers = min(8, max(1, len(names)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(accepted, name): name for name in names}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                accepted_by_name[name] = future.result()
            except Exception:
                accepted_by_name[name] = False
    return [name for name in names if accepted_by_name.get(name)]


class CategoryFilterMixin:
    def category_tr(self, key):
        language = getattr(self, "language", "fr")
        return CATEGORY_LABELS.get(language, CATEGORY_LABELS["fr"])[key]

    def category_button_text(self):
        selected = set(getattr(self, "selected_categories", {CATEGORY_ALL}))
        if CATEGORY_ALL in selected or not selected:
            return self.category_tr(CATEGORY_ALL)
        if len(selected) == 1:
            return self.category_tr(next(iter(selected)))
        return self.category_tr("count").format(n=len(selected))

    def open_category_filter(self):
        colors = getattr(self, "COLORS", None)
        if colors is None:
            # Tous les modes importent COLORS dans leur module ; recherche via globals de classe.
            colors = {"bg":"#0f172a", "panel":"#1e293b", "dark":"#0f172a", "blue":"#2563eb"}
        popup = tk.Toplevel(self)
        popup.title(self.category_tr("filter_title"))
        popup.configure(bg=colors["bg"])
        popup.transient(self); popup.grab_set(); popup.resizable(False, False)
        box = tk.Frame(popup, bg=colors["panel"], padx=18, pady=14)
        box.pack(padx=18, pady=(18, 8))
        current = set(getattr(self, "selected_categories", {CATEGORY_ALL}))
        variables = {key: tk.BooleanVar(value=key in current) for key in CATEGORY_ORDER}

        def on_toggle(key):
            if key == CATEGORY_ALL and variables[key].get():
                for other in CATEGORY_ORDER[1:]: variables[other].set(False)
            elif key != CATEGORY_ALL and variables[key].get():
                variables[CATEGORY_ALL].set(False)
            if not any(v.get() for v in variables.values()):
                variables[CATEGORY_ALL].set(True)

        for row, key in enumerate(CATEGORY_ORDER):
            tk.Checkbutton(box, text=self.category_tr(key), variable=variables[key],
                           command=lambda k=key: on_toggle(k), bg=colors["panel"], fg="white",
                           selectcolor=colors["dark"], activebackground=colors["panel"],
                           activeforeground="white", anchor="w",
                           font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=4)

        def apply():
            selected = {key for key, var in variables.items() if var.get()}
            if not selected: selected = {CATEGORY_ALL}
            self.selected_categories = selected
            popup.destroy()
            if hasattr(self, "category_button"):
                self.category_button.config(text=self.category_button_text())
            self._category_filter_changed()

        actions = tk.Frame(popup, bg=colors["bg"]); actions.pack(fill="x", padx=18, pady=(0, 15))
        tk.Button(actions, text=self.category_tr(CATEGORY_ALL),
                  command=lambda: [variables[k].set(k == CATEGORY_ALL) for k in CATEGORY_ORDER],
                  bg="#334155", fg="white", relief="flat", bd=0, padx=12, pady=7).pack(side="left")
        tk.Button(actions, text=self.category_tr("none"),
                  command=lambda: [variables[k].set(False) for k in CATEGORY_ORDER],
                  bg="#334155", fg="white", relief="flat", bd=0, padx=12, pady=7).pack(side="left", padx=5)
        tk.Button(actions, text=self.category_tr("apply"), command=apply,
                  bg=colors["blue"], fg="white", relief="flat", bd=0,
                  padx=18, pady=8, font=("Segoe UI", 9, "bold")).pack(side="right")
        popup.update_idletasks()
        x = self.winfo_rootx() + max(20, (self.winfo_width()-popup.winfo_reqwidth())//2)
        y = self.winfo_rooty() + 80
        popup.geometry(f"{popup.winfo_reqwidth()}x{popup.winfo_reqheight()}+{x}+{y}")

    def _category_filter_changed(self):
        if hasattr(self, "_invalidate_preload"): self._invalidate_preload()
        if hasattr(self, "_reset_pool"): self._reset_pool()
        if hasattr(self, "pool"): self.pool = []
        if hasattr(self, "update_filter_buttons"): self.update_filter_buttons()
        if hasattr(self, "_refresh_settings"): self._refresh_settings()
