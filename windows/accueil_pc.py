# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
from mode_draft import ASSETS, COLORS
from mode_draft_pc import PokemonStatDraftPC
from mode_guesser_pc import StatGuesserPC
from affichage_pc import apply_pc_window, place_webcam_slot


class PokeStatChallengePC(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg=COLORS["bg"])
        self.child = None
        self.language = "fr"
        self.webcam_aspect = "4:3"
        apply_pc_window(self, "PokéStat Challenge PC")
        self.show_home()

    def set_language(self, language):
        self.language = language
        self.show_home()

    def set_webcam_aspect(self, aspect):
        self.webcam_aspect = aspect
        self.show_home()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_home(self):
        if self.child and self.child.winfo_exists():
            self.child.destroy()
        self.child = None
        self.deiconify()
        self.clear()
        apply_pc_window(self, "PokéStat Challenge PC")

        # Entire top-right 320x240 block is reserved identically on every page.
        place_webcam_slot(self, self.language, self.webcam_aspect)

        hero = tk.Frame(self, bg=COLORS["bg"], width=900, height=245)
        hero.place(x=20, y=18)
        hero.pack_propagate(False)
        center = tk.Frame(hero, bg=COLORS["bg"])
        center.pack(expand=True)
        try:
            self.logo = tk.PhotoImage(file=str(ASSETS / "pokemon_logo.png"))
            tk.Label(center, image=self.logo, bg=COLORS["bg"]).pack()
        except tk.TclError:
            pass
        tk.Label(center, text="POKÉSTAT CHALLENGE", bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 31, "bold")).pack(pady=(5,2))
        subtitle = "Choisis ton mode de jeu" if self.language == "fr" else "Choose your game mode"
        tk.Label(center, text=subtitle, bg=COLORS["bg"], fg="#94a3b8",
                 font=("Segoe UI", 13)).pack()

        controls = tk.Frame(center, bg=COLORS["bg"])
        controls.pack(pady=(12,0))
        language = tk.Frame(controls, bg=COLORS["bg"])
        language.pack(side="left", padx=18)
        tk.Label(language, text="LANGUE" if self.language=="fr" else "LANGUAGE",
                 bg=COLORS["bg"], fg="#94a3b8", font=("Segoe UI",8,"bold")).pack()
        row = tk.Frame(language, bg=COLORS["bg"]); row.pack(pady=(3,0))
        self.small_button(row,"FRANÇAIS",lambda:self.set_language("fr"),self.language=="fr").pack(side="left",padx=3)
        self.small_button(row,"ENGLISH",lambda:self.set_language("en"),self.language=="en").pack(side="left",padx=3)

        camera = tk.Frame(controls, bg=COLORS["bg"])
        camera.pack(side="left", padx=18)
        cam_title = "FORMAT WEBCAM" if self.language=="fr" else "WEBCAM FORMAT"
        tk.Label(camera,text=cam_title,bg=COLORS["bg"],fg="#94a3b8",font=("Segoe UI",8,"bold")).pack()
        camrow=tk.Frame(camera,bg=COLORS["bg"]); camrow.pack(pady=(3,0))
        self.small_button(camrow,"4:3",lambda:self.set_webcam_aspect("4:3"),self.webcam_aspect=="4:3").pack(side="left",padx=3)
        self.small_button(camrow,"16:9",lambda:self.set_webcam_aspect("16:9"),self.webcam_aspect=="16:9").pack(side="left",padx=3)

        modes = tk.Frame(self, bg=COLORS["bg"])
        modes.place(x=60, y=275, relwidth=.90, height=410)
        modes.columnconfigure(0, weight=1, uniform="modes")
        modes.columnconfigure(1, weight=1, uniform="modes")
        modes.rowconfigure(0, weight=1)
        if self.language == "fr":
            draft=("DRAFT DE STATS","Attribue une statistique à chacun des six Pokémon puis réalise le meilleur total possible.","JOUER AU DRAFT")
            guess=("STAT GUESSER","Retrouve les six Base Stats avec les filtres et le nombre de tentatives de ton choix.","JOUER AU GUESSER")
        else:
            draft=("STAT DRAFT","Assign one stat to each of six Pokémon, then build the best total possible.","PLAY STAT DRAFT")
            guess=("STAT GUESSER","Find all six Base Stats using your chosen filters and attempt count.","PLAY STAT GUESSER")
        self.mode_card(modes,"⚄",*draft,COLORS["red"],self.open_draft).grid(row=0,column=0,sticky="nsew",padx=(0,14))
        self.mode_card(modes,"◉",*guess,COLORS["blue"],self.open_guesser).grid(row=0,column=1,sticky="nsew",padx=(14,0))

    def small_button(self,parent,text,command,active):
        return tk.Button(parent,text=text,command=command,bg=COLORS["blue"] if active else COLORS["panel"],
                         fg="white",relief="flat",bd=0,padx=15,pady=6,font=("Segoe UI",9,"bold"))

    def mode_card(self,parent,icon,title,text,button,color,command):
        frame=tk.Frame(parent,bg="white",padx=30,pady=20)
        tk.Label(frame,text=icon,bg="white",font=("Segoe UI Symbol",40,"bold")).pack()
        tk.Label(frame,text=title,bg="white",fg=COLORS["dark"],font=("Segoe UI",21,"bold")).pack(pady=(6,10))
        tk.Label(frame,text=text,bg="white",fg=COLORS["muted"],wraplength=430,justify="center",
                 font=("Segoe UI",11)).pack(expand=True)
        tk.Button(frame,text=button,command=command,bg=color,fg="white",activebackground=color,
                  activeforeground="white",relief="flat",bd=0,pady=13,
                  font=("Segoe UI",12,"bold")).pack(fill="x",pady=(18,0))
        return frame

    def open_draft(self):
        self.withdraw()
        self.child=PokemonStatDraftPC(self,on_home=self.show_home,language=self.language,
                                      webcam_aspect=self.webcam_aspect)

    def open_guesser(self):
        self.withdraw()
        self.child=StatGuesserPC(self,self.show_home,self.language,
                                 webcam_aspect=self.webcam_aspect)


if __name__ == "__main__":
    PokeStatChallengePC().mainloop()
