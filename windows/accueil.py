# -*- coding: utf-8 -*-
from __future__ import annotations

import tkinter as tk

from mode_draft import ASSETS, COLORS, PokemonStatDraft
from mode_guesser import StatGuesser

def fit_window(w):
    w.update_idletasks(); sw,sh=w.winfo_screenwidth(),w.winfo_screenheight(); h=min(1040,sh-70); width=min(650,max(560,int(h*9/16)))
    w.geometry(f"{width}x{h}+{max(0,(sw-width)//2)}+0"); w.minsize(560,820); w.resizable(False,False)

class PokeStatChallenge(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("PokéStat Challenge"); self.configure(bg=COLORS["bg"]); self.child=None; self.language="fr"; fit_window(self); self.show_home()
    def set_language(self, language):
        self.language = language
        self.show_home()
    def clear(self):
        for x in self.winfo_children(): x.destroy()
    def show_home(self):
        if self.child and self.child.winfo_exists(): self.child.destroy()
        self.child=None; self.deiconify(); self.clear(); fit_window(self)
        head=tk.Frame(self,bg=COLORS["bg"],pady=32); head.pack(fill="x")
        try:
            self.logo=tk.PhotoImage(file=str(ASSETS/"pokemon_logo.png")); tk.Label(head,image=self.logo,bg=COLORS["bg"]).pack()
        except tk.TclError: pass
        tk.Label(head,text="POKÉSTAT CHALLENGE",bg=COLORS["bg"],fg="white",font=("Segoe UI",27,"bold")).pack(pady=(8,2))
        tk.Label(head,text="Choisis ton mode de jeu" if self.language=="fr" else "Choose your game mode",bg=COLORS["bg"],fg="#94a3b8",font=("Segoe UI",12)).pack()
        lang=tk.Frame(self,bg=COLORS["bg"]); lang.pack(fill="x",pady=(0,8))
        tk.Label(lang,text="LANGUE" if self.language=="fr" else "LANGUAGE",bg=COLORS["bg"],fg="#94a3b8",font=("Segoe UI",8,"bold")).pack()
        row=tk.Frame(lang,bg=COLORS["bg"]); row.pack(pady=(4,0))
        tk.Button(row,text="FRANÇAIS",command=lambda:self.set_language("fr"),bg=COLORS["blue"] if self.language=="fr" else COLORS["panel"],fg="white",relief="flat",bd=0,padx=18,pady=6,font=("Segoe UI",9,"bold")).pack(side="left",padx=4)
        tk.Button(row,text="ENGLISH",command=lambda:self.set_language("en"),bg=COLORS["blue"] if self.language=="en" else COLORS["panel"],fg="white",relief="flat",bd=0,padx=18,pady=6,font=("Segoe UI",9,"bold")).pack(side="left",padx=4)
        body=tk.Frame(self,bg=COLORS["bg"],padx=28); body.pack(fill="both",expand=True)
        if self.language=="fr":
            draft=("DRAFT DE STATS","Attribue une statistique à chacun des six Pokémon,\npuis réalise le meilleur total possible.","JOUER AU DRAFT")
            guess=("STAT GUESSER","Retrouve les six Base Stats avec le nombre de tentatives de ton choix,\ngrâce aux bornes qui se resserrent.","JOUER AU STAT GUESSER")
        else:
            draft=("STAT DRAFT","Assign one stat to each of six Pokémon,\nthen build the best total possible.","PLAY STAT DRAFT")
            guess=("STAT GUESSER","Find all six Base Stats with the number of attempts you choose,\nusing the narrowing bounds.","PLAY STAT GUESSER")
        self.card(body,"⚄",draft[0],draft[1],draft[2],COLORS["red"],self.open_draft).pack(fill="x",pady=(8,16))
        self.card(body,"◉",guess[0],guess[1],guess[2],COLORS["blue"],self.open_guesser).pack(fill="x")
        tk.Button(self,text="QUITTER",command=self.destroy,bg="#334155",fg="white",relief="flat",bd=0,padx=25,pady=10,font=("Segoe UI",9,"bold")).pack(pady=25)
    def card(self,parent,icon,title,text,button,color,command):
        f=tk.Frame(parent,bg="white",padx=24,pady=20)
        tk.Label(f,text=icon,bg="white",font=("Segoe UI Symbol",34,"bold")).pack()
        tk.Label(f,text=title,bg="white",fg=COLORS["dark"],font=("Segoe UI",18,"bold")).pack(pady=(5,8))
        tk.Label(f,text=text,bg="white",fg=COLORS["muted"],justify="center",font=("Segoe UI",10),anchor="center").pack(fill="x",padx=8,pady=(0,16))
        tk.Button(f,text=button,command=command,bg=color,fg="white",activebackground=color,activeforeground="white",relief="flat",bd=0,pady=13,font=("Segoe UI",11,"bold"),cursor="hand2").pack(fill="x")
        return f
    def open_draft(self):
        self.withdraw(); self.child=PokemonStatDraft(self,on_home=self.show_home,language=self.language); fit_window(self.child)
    def open_guesser(self):
        self.withdraw(); self.child=StatGuesser(self,self.show_home,self.language)
        self.child.update_idletasks(); fit_window(self.child)
        self.child.after(80,lambda:fit_window(self.child) if self.child and self.child.winfo_exists() else None)


if __name__ == "__main__":
    PokeStatChallenge().mainloop()
