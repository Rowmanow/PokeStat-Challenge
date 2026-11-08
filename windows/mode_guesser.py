# -*- coding: utf-8 -*-
from __future__ import annotations

import io
import random
import threading
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from mode_draft import (
    API,
    COLORS,
    TYPE_KEYS,
    TYPE_LABELS,
    TYPE_COLORS,
    TYPE_ICONS,
    special_form_generation,
    get_json,
    get_bytes,
)

GUESSER_I18N = {
    "fr": {
        "home":"← ACCUEIL", "types":"TYPES", "generations":"GÉNÉRATIONS", "forms":"FORMES", "attempts":"TENTATIVES",
        "all_types":"TOUS LES TYPES", "all_generations":"TOUTES LES GÉNÉRATIONS", "both":"STANDARD + MÉGA",
        "stat":"STATISTIQUE", "low":"BASSE", "guess":"ESSAI", "high":"HAUTE", "submit":"VALIDER", "new_game":"NOUVELLE PARTIE",
        "ready":"Prêt à jouer ?", "click_new":"Clique sur NOUVELLE PARTIE", "no_game":"Aucune partie en cours",
        "configure":"Choisis tes filtres, puis démarre une nouvelle partie.", "loading":"Chargement...", "preparing":"Préparation des Pokémon compatibles...",
        "attempt":"Tentative {n} / {max}", "play":"Devine les six statistiques !", "bounds":"Bornes mises à jour. Continue !",
        "victory":"✓ VICTOIRE", "defeat":"✕ DÉFAITE", "won":"Toutes les statistiques ont été trouvées en {n} tentative(s) !",
        "lost":"Fin de partie · distance finale : {distance}", "enter":"Entre une valeur de 1 à 255 pour {stat}.",
        "changed":"Filtres modifiés. Clique sur NOUVELLE PARTIE.", "type_filter":"Filtre par type", "types_allowed":"Types autorisés",
        "generation_filter":"Filtre par génération", "generations_allowed":"Générations autorisées", "generation":"Génération",
        "all":"TOUT", "none":"AUCUN", "apply":"APPLIQUER", "type_required":"Type requis", "select_type":"Sélectionne au moins un type.",
        "generation_required":"Génération requise", "select_generation":"Sélectionne au moins une génération.",
        "form_filter":"Filtre par forme", "forms_allowed":"Formes autorisées", "standard_only":"FORMES STANDARD UNIQUEMENT",
        "mega_only":"MÉGA-ÉVOLUTIONS UNIQUEMENT", "both_only":"STANDARD + MÉGA-ÉVOLUTIONS", "standard":"FORMES STANDARD",
        "mega":"MÉGA UNIQUEMENT", "choices":"CHOIX", "filters":"Filtres", "no_match":"Aucun Pokémon ne correspond à ces filtres.",
        "prepare_error":"Impossible de préparer cette sélection.", "error":"Erreur", "load_error":"Impossible de charger le Pokémon."
    },
    "en": {
        "home":"← HOME", "types":"TYPES", "generations":"GENERATIONS", "forms":"FORMS", "attempts":"ATTEMPTS",
        "all_types":"ALL TYPES", "all_generations":"ALL GENERATIONS", "both":"STANDARD + MEGA",
        "stat":"STAT", "low":"LOW", "guess":"GUESS", "high":"HIGH", "submit":"SUBMIT", "new_game":"NEW GAME",
        "ready":"Ready to play?", "click_new":"Click NEW GAME", "no_game":"No game in progress",
        "configure":"Choose your filters, then start a new game.", "loading":"Loading...", "preparing":"Preparing compatible Pokémon...",
        "attempt":"Attempt {n} / {max}", "play":"Guess all six stats!", "bounds":"Bounds updated. Keep going!",
        "victory":"✓ VICTORY", "defeat":"✕ DEFEAT", "won":"All stats were found in {n} attempt(s)!",
        "lost":"Game over · final distance: {distance}", "enter":"Enter a value from 1 to 255 for {stat}.",
        "changed":"Filters updated. Click NEW GAME.", "type_filter":"Type filter", "types_allowed":"Allowed types",
        "generation_filter":"Generation filter", "generations_allowed":"Allowed generations", "generation":"Generation",
        "all":"ALL", "none":"NONE", "apply":"APPLY", "type_required":"Type required", "select_type":"Select at least one type.",
        "generation_required":"Generation required", "select_generation":"Select at least one generation.",
        "form_filter":"Form filter", "forms_allowed":"Allowed forms", "standard_only":"STANDARD FORMS ONLY",
        "mega_only":"MEGA EVOLUTIONS ONLY", "both_only":"STANDARD + MEGA EVOLUTIONS", "standard":"STANDARD FORMS",
        "mega":"MEGA ONLY", "choices":"CHOICES", "filters":"Filters", "no_match":"No Pokémon matches these filters.",
        "prepare_error":"Unable to prepare this selection.", "error":"Error", "load_error":"Unable to load the Pokémon."
    }
}
GUESSER_STATS = {
    "fr":{"hp":"HP","attack":"Attaque","special-attack":"Attaque spéciale","defense":"Défense","special-defense":"Défense spéciale","speed":"Vitesse"},
    "en":{"hp":"HP","attack":"Attack","special-attack":"Special Attack","defense":"Defense","special-defense":"Special Defense","speed":"Speed"}
}

STATS=[("hp","HP","♥"),("attack","Attaque","⚔"),("special-attack","Attaque spéciale","✦"),("defense","Défense","◐"),("special-defense","Défense spéciale","♟"),("speed","Vitesse","ϟ")]

class StatGuesser(tk.Toplevel):
    def __init__(self,master,on_home,language="fr"):
        super().__init__(master); self.on_home=on_home; self.language=language; self.title("PokéStat Challenge - Stat Guesser"); self.configure(bg=COLORS["bg"]); self.protocol("WM_DELETE_WINDOW",self.go_home)
        self.target={}; self.bounds={}; self.entries={}; self.bound_labels={}; self.tries=1; self.finished=False; self.sprite=None
        self.selected_types=set(TYPE_KEYS); self.selected_generations=set(range(1,10)); self.form_mode="both"; self.pool=[]
        self.max_attempts=10; self.attempts_var=tk.StringVar(value="10")
        self.build(); self.prepare_idle_screen()
    def tr(self, key, **kwargs):
        return GUESSER_I18N[self.language][key].format(**kwargs)
    def stat_name(self, key):
        return GUESSER_STATS[self.language][key]
    def go_home(self): self.destroy(); self.on_home()
    def build(self):
        header=tk.Frame(self,bg=COLORS["bg"],height=66); header.pack(fill="x"); header.pack_propagate(False)
        tk.Button(header,text=self.tr("home"),command=self.go_home,bg=COLORS["panel"],fg="white",relief="flat",bd=0,padx=10,pady=7,font=("Segoe UI",9,"bold")).place(x=14,rely=.5,anchor="w")
        tk.Label(header,text="POKÉSTAT CHALLENGE · GUESSER",bg=COLORS["bg"],fg="white",font=("Segoe UI",15,"bold")).place(relx=.57,rely=.5,anchor="center")
        body=tk.Frame(self,bg=COLORS["bg"],padx=13); body.pack(fill="both",expand=True)
        filters=tk.Frame(body,bg=COLORS["panel"],padx=12,pady=6); filters.pack(fill="x",pady=(0,10))
        filters.columnconfigure(0,weight=1); filters.columnconfigure(1,weight=1)
        tk.Label(filters,text=self.tr("types"),bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",8,"bold")).grid(row=0,column=0,sticky="w")
        tk.Label(filters,text=self.tr("generations"),bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",8,"bold")).grid(row=0,column=1,sticky="w",padx=(8,0))
        self.type_button=tk.Button(filters,text=self.tr("all_types"),command=self.open_type_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=7,font=("Segoe UI",9,"bold")); self.type_button.grid(row=1,column=0,sticky="ew",pady=(3,0))
        self.gen_button=tk.Button(filters,text=self.tr("all_generations"),command=self.open_generation_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=7,font=("Segoe UI",9,"bold")); self.gen_button.grid(row=1,column=1,sticky="ew",padx=(8,0),pady=(3,0))
        tk.Label(filters,text=self.tr("forms"),bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",8,"bold")).grid(row=2,column=0,sticky="w",pady=(7,0))
        tk.Label(filters,text=self.tr("attempts"),bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",8,"bold")).grid(row=2,column=1,sticky="w",padx=(8,0),pady=(7,0))
        self.form_button=tk.Button(filters,text=self.tr("both"),command=self.open_form_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=7,font=("Segoe UI",9,"bold")); self.form_button.grid(row=3,column=0,sticky="ew",pady=(3,0))
        attempts_box=tk.Frame(filters,bg="white",height=34)
        attempts_box.grid(row=3,column=1,sticky="ew",padx=(8,0),pady=(3,0))
        attempts_box.grid_propagate(False)
        attempts_box.columnconfigure(1,weight=1)
        tk.Button(attempts_box,text="−",command=lambda:self.change_attempts(-1),bg="#e2e8f0",fg=COLORS["dark"],activebackground="#cbd5e1",activeforeground=COLORS["dark"],relief="flat",bd=0,width=3,font=("Segoe UI",11,"bold")).grid(row=0,column=0,sticky="ns")
        self.attempts_entry=tk.Entry(attempts_box,textvariable=self.attempts_var,justify="center",bg="white",fg=COLORS["dark"],relief="flat",bd=0,font=("Segoe UI",10,"bold"),validate="key")
        self.attempts_entry.config(validatecommand=(self.register(self.validate_attempts_input),"%P"))
        self.attempts_entry.grid(row=0,column=1,sticky="nsew",ipady=6)
        tk.Button(attempts_box,text="+",command=lambda:self.change_attempts(1),bg="#e2e8f0",fg=COLORS["dark"],activebackground="#cbd5e1",activeforeground=COLORS["dark"],relief="flat",bd=0,width=3,font=("Segoe UI",11,"bold")).grid(row=0,column=2,sticky="ns")
        card=tk.Frame(body,bg="white",padx=12,pady=7); card.pack(fill="x",pady=(0,10))
        self.name=tk.Label(card,text="",bg="white",fg=COLORS["dark"],font=("Segoe UI",20,"bold")); self.name.pack()
        self.types_frame=tk.Frame(card,bg="white",height=34)
        self.types_frame.pack(fill="x",pady=(1,2)); self.types_frame.pack_propagate(False)
        image_box=tk.Frame(card,bg="white",width=500,height=165); image_box.pack(); image_box.pack_propagate(False)
        self.image=tk.Label(image_box,bg="white"); self.image.pack(fill="both",expand=True)
        self.bst=tk.Label(card,text="",bg="white",fg=COLORS["green"],font=("Segoe UI",13,"bold")); self.bst.pack()
        self.attempt=tk.Label(card,text="",bg="white",fg=COLORS["muted"],font=("Segoe UI",10,"bold")); self.attempt.pack(pady=(3,0))
        stats=tk.Frame(body,bg=COLORS["panel"],padx=14,pady=5); stats.pack(fill="x")
        for c,t in enumerate((self.tr("stat"),self.tr("low"),self.tr("guess"),self.tr("high"))):
            tk.Label(stats,text=t,bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",8,"bold")).grid(row=0,column=c,sticky="w" if c==0 else "")
        stats.columnconfigure(0,weight=1)
        for r,(key,label,icon) in enumerate(STATS,1):
            tk.Label(stats,text=f"{icon}  {self.stat_name(key)}",bg=COLORS["panel"],fg="white",font=("Segoe UI",10,"bold"),anchor="w").grid(row=r,column=0,sticky="ew",pady=3)
            lo=tk.Label(stats,text="—",bg=COLORS["panel"],fg=COLORS["gold"],width=5,font=("Segoe UI",10,"bold")); lo.grid(row=r,column=1)
            cell=tk.Frame(stats,bg="#475569",padx=2,pady=2); cell.grid(row=r,column=2,padx=10,pady=2)
            e=tk.Entry(cell,width=6,justify="center",font=("Segoe UI",12,"bold"),relief="flat",bd=0,bg="white",fg=COLORS["dark"],insertbackground=COLORS["dark"],highlightthickness=0); e.pack(ipady=3)
            hi=tk.Label(stats,text="—",bg=COLORS["panel"],fg=COLORS["gold"],width=5,font=("Segoe UI",10,"bold")); hi.grid(row=r,column=3)
            self.entries[key]=e; self.bound_labels[key]=(lo,hi)
        self.status=tk.Label(body,text="",bg=COLORS["bg"],fg="#94a3b8",font=("Segoe UI",9)); self.status.pack(pady=(4,2))
        self.validate=tk.Button(body,text=self.tr("submit"),command=self.check,bg=COLORS["gold"],fg=COLORS["dark"],relief="flat",bd=0,pady=10,font=("Segoe UI",12,"bold")); self.validate.pack(fill="x",pady=(2,2))
        tk.Button(body,text=self.tr("new_game"),command=self.new_game,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=9,font=("Segoe UI",11,"bold")).pack(fill="x",pady=(2,3))
        self.bind("<Return>",lambda _:self.check())
    def validate_attempts_input(self, value):
        return value == "" or (value.isdigit() and len(value) <= 2)

    def change_attempts(self, delta):
        try:
            current=int(self.attempts_var.get())
        except ValueError:
            current=10
        self.attempts_var.set(str(max(1,min(20,current+delta))))

    def prepare_idle_screen(self):
        self.target={}; self.finished=False; self.sprite=None
        self.name.config(text=self.tr("ready"))
        self.show_type_badges([])
        self.image.config(image=""); self.bst.config(text=self.tr("click_new")); self.attempt.config(text=self.tr("no_game"))
        self.validate.config(text=self.tr("submit"),state="disabled",bg=COLORS["gold"],fg=COLORS["dark"])
        for key,_,_ in STATS:
            self.entries[key].config(state="disabled",disabledbackground="#e2e8f0",disabledforeground="#64748b"); self.entries[key].delete(0,"end")
            self.bound_labels[key][0].config(text="—",fg=COLORS["gold"]); self.bound_labels[key][1].config(text="—",fg=COLORS["gold"])
        self.status.config(text=self.tr("configure"),fg="#94a3b8")

    def show_modal_popup(self, popup):
        popup.withdraw(); popup.update_idletasks()
        width=popup.winfo_reqwidth(); height=popup.winfo_reqheight()
        x=self.winfo_rootx()+max(0,(self.winfo_width()-width)//2)
        y=self.winfo_rooty()+115
        x=min(max(10,x),max(10,popup.winfo_screenwidth()-width-10))
        y=min(max(10,y),max(10,popup.winfo_screenheight()-height-40))
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.deiconify(); popup.lift(self); popup.focus_force(); popup.grab_set()

    def open_type_filter(self):
        self.open_filter(self.tr("type_filter"),self.tr("types_allowed"),[(k,TYPE_LABELS[self.language].get(k,k.title())) for k in TYPE_KEYS],self.selected_types,self.apply_type_filter)
    def open_generation_filter(self):
        roman={1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX"}
        self.open_filter(self.tr("generation_filter"),self.tr("generations_allowed"),[(n,f"{self.tr("generation")} {roman[n]}") for n in range(1,10)],self.selected_generations,self.apply_generation_filter)
    def open_filter(self,title,heading,items,selected,callback):
        popup=tk.Toplevel(self); popup.title(title); popup.configure(bg=COLORS["bg"]); popup.transient(self); popup.resizable(False,False); popup.withdraw()
        tk.Label(popup,text=heading,bg=COLORS["bg"],fg="white",font=("Segoe UI",15,"bold")).pack(padx=22,pady=(18,10))
        box=tk.Frame(popup,bg=COLORS["panel"],padx=14,pady=12); box.pack(padx=18)
        variables={}
        for i,(key,label) in enumerate(items):
            var=tk.BooleanVar(value=key in selected); variables[key]=var
            tk.Checkbutton(box,text=label,variable=var,bg=COLORS["panel"],fg="white",selectcolor=COLORS["dark"],activebackground=COLORS["panel"],activeforeground="white",font=("Segoe UI",9,"bold")).grid(row=i//2,column=i%2,sticky="w",padx=8,pady=4)
        actions=tk.Frame(popup,bg=COLORS["bg"]); actions.pack(fill="x",padx=18,pady=14)
        tk.Button(actions,text=self.tr("all"),command=lambda:[v.set(True) for v in variables.values()],bg="#334155",fg="white",relief="flat",bd=0,padx=14,pady=8).pack(side="left")
        tk.Button(actions,text=self.tr("none"),command=lambda:[v.set(False) for v in variables.values()],bg="#334155",fg="white",relief="flat",bd=0,padx=14,pady=8).pack(side="left",padx=6)
        tk.Button(actions,text=self.tr("apply"),command=lambda:callback(popup,variables),bg=COLORS["blue"],fg="white",relief="flat",bd=0,padx=18,pady=8,font=("Segoe UI",9,"bold")).pack(side="right")
        self.show_modal_popup(popup)
    def apply_type_filter(self,popup,variables):
        selected={k for k,v in variables.items() if v.get()}
        if not selected: messagebox.showwarning(self.tr("type_required"),self.tr("select_type"),parent=popup); return
        self.selected_types=selected; self.pool=[]; self.update_filter_buttons(); popup.destroy(); self.status.config(text=self.tr("changed"),fg=COLORS["gold"])
    def apply_generation_filter(self,popup,variables):
        selected={k for k,v in variables.items() if v.get()}
        if not selected: messagebox.showwarning(self.tr("generation_required"),self.tr("select_generation"),parent=popup); return
        self.selected_generations=selected; self.pool=[]; self.update_filter_buttons(); popup.destroy(); self.status.config(text=self.tr("changed"),fg=COLORS["gold"])
    def open_form_filter(self):
        popup=tk.Toplevel(self); popup.title(self.tr("form_filter")); popup.configure(bg=COLORS["bg"]); popup.transient(self); popup.resizable(False,False); popup.withdraw()
        tk.Label(popup,text=self.tr("forms_allowed"),bg=COLORS["bg"],fg="white",font=("Segoe UI",15,"bold")).pack(padx=28,pady=(20,12))
        value=tk.StringVar(value=self.form_mode)
        box=tk.Frame(popup,bg=COLORS["panel"],padx=18,pady=14); box.pack(padx=20)
        choices=[("standard",self.tr("standard_only")),("mega",self.tr("mega_only")),("both",self.tr("both_only"))]
        for key,label in choices:
            tk.Radiobutton(box,text=label,variable=value,value=key,bg=COLORS["panel"],fg="white",selectcolor=COLORS["dark"],activebackground=COLORS["panel"],activeforeground="white",font=("Segoe UI",9,"bold"),anchor="w").pack(fill="x",pady=5)
        tk.Button(popup,text=self.tr("apply"),command=lambda:self.apply_form_filter(popup,value.get()),bg=COLORS["blue"],fg="white",relief="flat",bd=0,padx=24,pady=9,font=("Segoe UI",9,"bold")).pack(pady=16)
        self.show_modal_popup(popup)
    def apply_form_filter(self,popup,value):
        self.form_mode=value; self.pool=[]; self.update_filter_buttons(); popup.destroy()
        self.status.config(text=self.tr("changed"),fg=COLORS["gold"])

    def update_filter_buttons(self):
        tt=self.tr("all_types") if len(self.selected_types)==len(TYPE_KEYS) else (" / ".join(TYPE_LABELS[self.language].get(k,k).upper() for k in sorted(self.selected_types)) if len(self.selected_types)<=2 else f"TYPES : {len(self.selected_types)} {self.tr('choices')}")
        gt=self.tr("all_generations") if len(self.selected_generations)==9 else ("GEN : "+", ".join(map(str,sorted(self.selected_generations))) if len(self.selected_generations)<=3 else f"GEN : {len(self.selected_generations)} {self.tr('choices')}")
        form_text={"standard":self.tr("standard"),"mega":self.tr("mega"),"both":self.tr("both")}[self.form_mode]
        self.type_button.config(text=tt); self.gen_button.config(text=gt); self.form_button.config(text=form_text)
    def new_game(self):
        try:
            requested_attempts=int(self.attempts_var.get())
        except ValueError:
            requested_attempts=10
        self.max_attempts=max(1,min(20,requested_attempts))
        self.attempts_var.set(str(self.max_attempts))
        self.target={}; self.bounds={k:{"min":None,"max":None} for k,_,_ in STATS}; self.tries=1; self.finished=False
        self.name.config(text=self.tr("loading")); self.show_type_badges([]); self.image.config(image=""); self.bst.config(text="BST : ?"); self.attempt.config(text=self.tr("attempt", n=1, max=self.max_attempts)); self.validate.config(text=self.tr("submit"),state="disabled",bg=COLORS["gold"],fg=COLORS["dark"])
        for k,_,_ in STATS:
            self.entries[k].config(state="normal",bg="white",fg="black"); self.entries[k].delete(0,"end"); self.bound_labels[k][0].config(text="—",fg=COLORS["gold"]); self.bound_labels[k][1].config(text="—",fg=COLORS["gold"])
        self.status.config(text=self.tr("preparing"),fg="#94a3b8"); threading.Thread(target=self.load_filter_pool,daemon=True).start()
    def load_filter_pool(self):
        try:
            generations=set()
            for n in self.selected_generations:
                d=get_json(f"{API}/generation/{n}",f"generation_{n}.json"); generations.update(x["name"] for x in d.get("pokemon_species",[]))
            typed=set()
            for t in self.selected_types:
                d=get_json(f"{API}/type/{t}",f"type_{t}.json"); typed.update(x["pokemon"]["name"] for x in d.get("pokemon",[]))
            standard_pool=generations & typed
            all_forms=get_json(f"{API}/pokemon?limit=100000&offset=0","pokemon_all_forms.json")
            mega_pool={item["name"] for item in all_forms.get("results",[])
                       if "-mega" in item["name"] and item["name"] in typed
                       and special_form_generation(item["name"]) in self.selected_generations}
            if self.form_mode=="standard": self.pool=sorted(standard_pool)
            elif self.form_mode=="mega": self.pool=sorted(mega_pool)
            else: self.pool=sorted(standard_pool | mega_pool)
            if not self.pool: raise ValueError(self.tr("no_match"))
            self.load_pokemon()
        except Exception as exc: self.after(0,lambda:messagebox.showerror(self.tr("filters"),f"{self.tr("prepare_error")}\n\n{exc}",parent=self))
    def load_pokemon(self):
        try:
            api_name=random.choice(self.pool); data=get_json(f"{API}/pokemon/{api_name}",f"pokemon_{api_name}.json"); species=get_json(data["species"]["url"],f"species_{data['species']['name']}.json")
            language_code = "fr" if self.language == "fr" else "en"
            localized_name = next(
                (item["name"] for item in species.get("names", [])
                 if item["language"]["name"] == language_code),
                data["name"].replace("-", " ").title(),
            )
            if "-mega" in api_name:
                suffix = " X" if api_name.endswith("-mega-x") else " Y" if api_name.endswith("-mega-y") else ""
                localized_name = (
                    f"Méga-{localized_name}{suffix}"
                    if self.language == "fr"
                    else f"Mega {localized_name}{suffix}"
                )
            target={x["stat"]["name"]:x["base_stat"] for x in data["stats"]}; types=[x["type"]["name"] for x in data["types"]]
            url=data.get("sprites",{}).get("other",{}).get("official-artwork",{}).get("front_default") or data.get("sprites",{}).get("front_default"); raw=get_bytes(url,f"guesser_{api_name}.png") if url else None
            self.after(0,lambda:self.apply_pokemon(localized_name,target,types,raw))
        except Exception as exc: self.after(0,lambda:messagebox.showerror(self.tr("error"),f"{self.tr("load_error")}\n\n{exc}",parent=self))
    def show_type_badges(self,types):
        for widget in self.types_frame.winfo_children(): widget.destroy()
        if not types: return
        group=tk.Frame(self.types_frame,bg="white"); group.place(relx=.5,rely=.5,anchor="center")
        for type_name in types:
            color=TYPE_COLORS.get(type_name,COLORS["muted"])
            badge=tk.Frame(group,bg=color,padx=8,pady=4); badge.pack(side="left",padx=4)
            tk.Label(badge,text=TYPE_ICONS.get(type_name,"●"),bg=color,fg="white",font=("Segoe UI Symbol",12,"bold")).pack(side="left",padx=(0,5))
            tk.Label(badge,text=TYPE_LABELS[self.language].get(type_name,type_name.title()).upper(),bg=color,fg="white",font=("Segoe UI",8,"bold")).pack(side="left")
    def apply_pokemon(self,name,target,types,raw):
        self.target=target; self.name.config(text=name); self.show_type_badges(types); self.bst.config(text=f"BST : {sum(target.values())}")
        if raw:
            im = Image.open(io.BytesIO(raw)).convert("RGBA")

            # Remove transparent margins supplied by some official artworks.
            alpha_box = im.getchannel("A").getbbox()
            if alpha_box:
                im = im.crop(alpha_box)

            # Normalize by visible height only. Wide Pokémon can use almost the
            # full card width instead of being reduced by a narrow width limit.
            target_height = 158
            if im.height > 0:
                scale = target_height / im.height
                target_width = max(1, round(im.width * scale))
                im = im.resize((target_width, target_height), Image.Resampling.LANCZOS)

            self.sprite = ImageTk.PhotoImage(im)
            self.image.config(image=self.sprite)
        self.status.config(text=self.tr("play"),fg="#94a3b8"); self.validate.config(text=self.tr("submit"),state="normal",bg=COLORS["gold"],fg=COLORS["dark"]); self.entries["hp"].focus_set()
    def check(self):
        if self.finished or not self.target:return
        guess={}
        for k,label,_ in STATS:
            e=self.entries[k]
            if str(e.cget("state"))=="disabled": guess[k]=self.target[k]; continue
            try:v=int(e.get())
            except ValueError:v=0
            if not 1<=v<=255:self.status.config(text=self.tr("enter", stat=self.stat_name(k)),fg=COLORS["red"]);e.focus_set();return
            guess[k]=v
        for k,_,_ in STATS:
            e=self.entries[k];v=guess[k];t=self.target[k]
            if str(e.cget("state"))=="disabled":continue
            if v<t:self.bounds[k]["min"]=v if self.bounds[k]["min"] is None else max(v,self.bounds[k]["min"])
            elif v>t:self.bounds[k]["max"]=v if self.bounds[k]["max"] is None else min(v,self.bounds[k]["max"])
            else:e.config(state="disabled",disabledbackground=COLORS["green"],disabledforeground="white");self.bounds[k]={"min":v,"max":v}
            lo,hi=self.bound_labels[k]
            if v==t:lo.config(text="✓",fg=COLORS["green"]);hi.config(text="✓",fg=COLORS["green"])
            else:lo.config(text=self.bounds[k]["min"] or "—");hi.config(text=self.bounds[k]["max"] or "—")
        if all(str(self.entries[k].cget("state"))=="disabled" for k,_,_ in STATS):self.finish(True,guess);return
        if self.tries>=self.max_attempts:self.finish(False,guess);return
        self.tries+=1;self.attempt.config(text=self.tr("attempt", n=self.tries, max=self.max_attempts));self.status.config(text=self.tr("bounds"),fg="#94a3b8")
    def finish(self,win,guess):
        self.finished=True
        if win:
            self.validate.config(text=self.tr("victory"),state="disabled",bg=COLORS["green"],fg="white",disabledforeground="white")
            self.status.config(text=self.tr("won", n=self.tries),fg=COLORS["green"])
        else:
            self.validate.config(text=self.tr("defeat"),state="disabled",bg=COLORS["red"],fg="white",disabledforeground="white")
            distance=sum(abs(guess[k]-self.target[k]) for k,_,_ in STATS)
            self.status.config(text=self.tr("lost", distance=distance),fg=COLORS["red"])
