# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
from mode_guesser import *
from affichage_pc import apply_pc_window, place_webcam_slot


class StatGuesserPC(StatGuesser):
    def __init__(self, master, on_home, language="fr", webcam_aspect="4:3"):
        self.webcam_aspect = webcam_aspect
        super().__init__(master, on_home, language)
        apply_pc_window(self, "PokéStat Challenge - Stat Guesser")
        place_webcam_slot(self, self.language, self.webcam_aspect)

    def build(self):
        # Fixed 260px top band. The webcam occupies the same top-right coordinates as Home and Draft.
        top = tk.Frame(self, bg=COLORS["bg"], height=260)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Button(top, text=self.tr("home"), command=self.go_home, bg=COLORS["panel"], fg="white",
                  relief="flat", bd=0, padx=14, pady=8,
                  font=("Segoe UI",10,"bold")).place(x=18,y=18)
        tk.Label(top,text="POKÉSTAT CHALLENGE · GUESSER",bg=COLORS["bg"],fg="white",
                 font=("Segoe UI",21,"bold")).place(x=260,y=28)

        filters=tk.Frame(top,bg=COLORS["panel"],padx=12,pady=10,width=880,height=150)
        filters.place(x=18,y=95)
        filters.grid_propagate(False)
        for c in range(4): filters.columnconfigure(c,weight=1,uniform="f")
        labels=[self.tr("types"),self.tr("generations"),self.tr("forms"),self.tr("attempts")]
        for c,text in enumerate(labels):
            tk.Label(filters,text=text,bg=COLORS["panel"],fg="#94a3b8",
                     font=("Segoe UI",8,"bold")).grid(row=0,column=c,sticky="w",padx=(0 if c==0 else 7,0))
        self.type_button=tk.Button(filters,text=self.tr("all_types"),command=self.open_type_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=9,font=("Segoe UI",9,"bold"))
        self.type_button.grid(row=1,column=0,sticky="ew",pady=(3,8))
        self.gen_button=tk.Button(filters,text=self.tr("all_generations"),command=self.open_generation_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=9,font=("Segoe UI",9,"bold"))
        self.gen_button.grid(row=1,column=1,sticky="ew",padx=(7,0),pady=(3,8))
        self.form_button=tk.Button(filters,text=self.tr("both"),command=self.open_form_filter,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=9,font=("Segoe UI",9,"bold"))
        self.form_button.grid(row=1,column=2,sticky="ew",padx=(7,0),pady=(3,8))
        attempts=tk.Frame(filters,bg="white",height=35); attempts.grid(row=1,column=3,sticky="ew",padx=(7,0),pady=(3,8)); attempts.grid_propagate(False); attempts.columnconfigure(1,weight=1)
        tk.Button(attempts,text="−",command=lambda:self.change_attempts(-1),bg="#e2e8f0",fg=COLORS["dark"],relief="flat",bd=0,width=3,font=("Segoe UI",11,"bold")).grid(row=0,column=0,sticky="ns")
        self.attempts_entry=tk.Entry(attempts,textvariable=self.attempts_var,justify="center",bg="white",fg=COLORS["dark"],relief="flat",bd=0,font=("Segoe UI",10,"bold"),validate="key")
        self.attempts_entry.config(validatecommand=(self.register(self.validate_attempts_input),"%P")); self.attempts_entry.grid(row=0,column=1,sticky="nsew")
        tk.Button(attempts,text="+",command=lambda:self.change_attempts(1),bg="#e2e8f0",fg=COLORS["dark"],relief="flat",bd=0,width=3,font=("Segoe UI",11,"bold")).grid(row=0,column=2,sticky="ns")
        tk.Button(filters,text=self.tr("new_game"),command=self.new_game,bg="white",fg=COLORS["dark"],relief="flat",bd=0,pady=9,font=("Segoe UI",10,"bold")).grid(row=2,column=0,columnspan=4,sticky="ew")

        main=tk.Frame(self,bg=COLORS["bg"],padx=18,pady=10)
        main.pack(fill="both",expand=True)
        main.columnconfigure(0,weight=5,uniform="main"); main.columnconfigure(1,weight=5,uniform="main"); main.rowconfigure(0,weight=1)

        card=tk.Frame(main,bg="white",padx=16,pady=10,highlightbackground="#dbe3ee",highlightthickness=1)
        card.grid(row=0,column=0,sticky="nsew",padx=(0,8))
        self.name=tk.Label(card,text="",bg="white",fg=COLORS["dark"],font=("Segoe UI",23,"bold")); self.name.pack()
        self.types_frame=tk.Frame(card,bg="white",height=35); self.types_frame.pack(fill="x",pady=(2,2)); self.types_frame.pack_propagate(False)
        image_box=tk.Frame(card,bg="white",height=270); image_box.pack(fill="both",expand=True); image_box.pack_propagate(False)
        self.image=tk.Label(image_box,bg="white"); self.image.pack(fill="both",expand=True)
        self.bst=tk.Label(card,text="",bg="white",fg=COLORS["green"],font=("Segoe UI",14,"bold")); self.bst.pack()
        self.attempt=tk.Label(card,text="",bg="white",fg=COLORS["muted"],font=("Segoe UI",10,"bold")); self.attempt.pack(pady=(2,0))

        stats=tk.Frame(main,bg=COLORS["panel"],padx=18,pady=12,highlightbackground="#334155",highlightthickness=1)
        stats.grid(row=0,column=1,sticky="nsew",padx=(8,0)); stats.columnconfigure(0,weight=1)
        for c,t in enumerate((self.tr("stat"),self.tr("low"),self.tr("guess"),self.tr("high"))):
            tk.Label(stats,text=t,bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",9,"bold")).grid(row=0,column=c,sticky="w" if c==0 else "")
        for r,(key,_label,icon) in enumerate(STATS,1):
            tk.Label(stats,text=f"{icon}  {self.stat_name(key)}",bg=COLORS["panel"],fg="white",font=("Segoe UI",11,"bold"),anchor="w").grid(row=r,column=0,sticky="ew",pady=5)
            lo=tk.Label(stats,text="—",bg=COLORS["panel"],fg=COLORS["gold"],width=5,font=("Segoe UI",10,"bold")); lo.grid(row=r,column=1)
            cell=tk.Frame(stats,bg="#475569",padx=2,pady=2); cell.grid(row=r,column=2,padx=10,pady=2)
            e=tk.Entry(cell,width=7,justify="center",font=("Segoe UI",12,"bold"),relief="flat",bd=0,bg="white",fg=COLORS["dark"]); e.pack(ipady=3)
            hi=tk.Label(stats,text="—",bg=COLORS["panel"],fg=COLORS["gold"],width=5,font=("Segoe UI",10,"bold")); hi.grid(row=r,column=3)
            self.entries[key]=e; self.bound_labels[key]=(lo,hi)
        self.status=tk.Label(stats,text="",bg=COLORS["panel"],fg="#94a3b8",font=("Segoe UI",9)); self.status.grid(row=7,column=0,columnspan=4,sticky="ew",pady=(6,2))
        self.validate=tk.Button(stats,text=self.tr("submit"),command=self.check,bg=COLORS["gold"],fg=COLORS["dark"],relief="flat",bd=0,pady=10,font=("Segoe UI",12,"bold")); self.validate.grid(row=8,column=0,columnspan=4,sticky="ew",pady=(3,0))
        self.bind("<Return>",lambda _e:self.check())
