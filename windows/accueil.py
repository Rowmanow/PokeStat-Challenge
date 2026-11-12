# -*- coding: utf-8 -*-
from __future__ import annotations

import tkinter as tk

from mode_draft import ASSETS, COLORS, PokemonStatDraft
from mode_guesser import StatGuesser
from mode_stat_rush import StatRush

APP_VERSION = "1.2.0"


def fit_window(window):
    window.update_idletasks()
    sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
    height = min(1040, sh - 70)
    width = min(650, max(560, int(height * 9 / 16)))
    window.geometry(f"{width}x{height}+{max(0, (sw-width)//2)}+0")
    window.minsize(560, 820)
    window.resizable(False, False)


class PokeStatChallenge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PokéStat Challenge")
        self.configure(bg=COLORS["bg"])
        self.child = None
        self.language = "fr"
        fit_window(self)
        self.show_home()

    def set_language(self, language):
        self.language = language
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
        fit_window(self)

        header = tk.Frame(self, bg=COLORS["bg"], pady=16)
        header.pack(fill="x")
        try:
            self.logo = tk.PhotoImage(file=str(ASSETS / "pokemon_logo.png"))
            tk.Label(header, image=self.logo, bg=COLORS["bg"]).pack()
        except tk.TclError:
            pass
        tk.Label(header, text="POKÉSTAT CHALLENGE", bg=COLORS["bg"], fg="white",
                 font=("Segoe UI", 25, "bold")).pack(pady=(5, 1))
        subtitle = "Choisis ton mode de jeu" if self.language == "fr" else "Choose your game mode"
        tk.Label(header, text=subtitle, bg=COLORS["bg"], fg="#94a3b8",
                 font=("Segoe UI", 11)).pack()
        tk.Label(header, text=f"VERSION {APP_VERSION}", bg=COLORS["bg"], fg=COLORS["gold"], font=("Segoe UI", 9, "bold")).pack(pady=(4, 0))

        language = tk.Frame(self, bg=COLORS["bg"])
        language.pack(fill="x", pady=(0, 7))
        tk.Label(language, text="LANGUE" if self.language == "fr" else "LANGUAGE",
                 bg=COLORS["bg"], fg="#94a3b8", font=("Segoe UI", 8, "bold")).pack()
        row = tk.Frame(language, bg=COLORS["bg"])
        row.pack(pady=(3, 0))
        tk.Button(row, text="FRANÇAIS", command=lambda: self.set_language("fr"),
                  bg=COLORS["blue"] if self.language == "fr" else COLORS["panel"],
                  fg="white", relief="flat", bd=0, padx=17, pady=5,
                  font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)
        tk.Button(row, text="ENGLISH", command=lambda: self.set_language("en"),
                  bg=COLORS["blue"] if self.language == "en" else COLORS["panel"],
                  fg="white", relief="flat", bd=0, padx=17, pady=5,
                  font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)

        body = tk.Frame(self, bg=COLORS["bg"], padx=22)
        body.pack(fill="both", expand=True)

        if self.language == "fr":
            draft = ("DRAFT DE STATS", "Attribue une statistique à chacun des six Pokémon,\npuis réalise le meilleur total possible.", "JOUER AU DRAFT")
            guess = ("STAT GUESSER", "Retrouve les six Base Stats avec le nombre de tentatives de ton choix,\ngrâce aux bornes qui se resserrent.", "JOUER AU STAT GUESSER")
            rush = ("STAT RUSH", "Trouve la meilleure ou la plus faible statistique\net réalise la plus longue série possible.", "JOUER AU STAT RUSH")
        else:
            draft = ("STAT DRAFT", "Assign one stat to each of six Pokémon,\nthen build the best total possible.", "PLAY STAT DRAFT")
            guess = ("STAT GUESSER", "Find all six Base Stats with the number of attempts you choose,\nusing the narrowing bounds.", "PLAY STAT GUESSER")
            rush = ("STAT RUSH", "Find the highest or lowest stat\nand build the longest streak possible.", "PLAY STAT RUSH")

        self.mode_card(body, "⚄", *draft, COLORS["red"], self.open_draft).pack(fill="x", pady=(4, 8))
        self.mode_card(body, "◉", *guess, COLORS["blue"], self.open_guesser).pack(fill="x", pady=8)
        self.mode_card(body, "⚡", *rush, COLORS["gold"], self.open_rush).pack(fill="x", pady=(8, 4))

        tk.Button(self, text="QUITTER" if self.language == "fr" else "QUIT",
                  command=self.destroy, bg="#334155", fg="white", relief="flat", bd=0,
                  padx=25, pady=8, font=("Segoe UI", 9, "bold")).pack(pady=(10, 12))

    def mode_card(self, parent, icon, title, text, button_text, color, command):
        card = tk.Frame(parent, bg="white", padx=18, pady=10, height=184)
        card.pack_propagate(False)
        tk.Label(card, text=icon, bg="white", fg=COLORS["dark"],
                 font=("Segoe UI Symbol", 24, "bold")).pack()
        tk.Label(card, text=title, bg="white", fg=COLORS["dark"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(2, 3))
        tk.Label(card, text=text, bg="white", fg=COLORS["muted"], justify="center",
                 font=("Segoe UI", 9), height=2).pack(fill="x", padx=6)
        button_fg = COLORS["dark"] if color == COLORS["gold"] else "white"
        tk.Button(card, text=button_text, command=command, bg=color, fg=button_fg,
                  activebackground=color, activeforeground=button_fg, relief="flat", bd=0,
                  pady=8, font=("Segoe UI", 10, "bold"), cursor="hand2").pack(
                      fill="x", side="bottom")
        return card

    def open_draft(self):
        self.withdraw()
        self.child = PokemonStatDraft(self, on_home=self.show_home, language=self.language)
        fit_window(self.child)

    def open_guesser(self):
        self.withdraw()
        self.child = StatGuesser(self, self.show_home, self.language)
        self.child.update_idletasks()
        fit_window(self.child)
        self.child.after(80, lambda: fit_window(self.child)
                         if self.child and self.child.winfo_exists() else None)

    def open_rush(self):
        self.withdraw()
        self.child = StatRush(self, on_home=self.show_home, language=self.language)
        fit_window(self.child)


if __name__ == "__main__":
    PokeStatChallenge().mainloop()
