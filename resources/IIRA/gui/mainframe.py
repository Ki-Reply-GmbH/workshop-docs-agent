
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font

from gui.containerframe import ContainerFrame
from gui.fileframes import FileFrame, ScaleFrame
from gui.helperframes import MainHelpFrame
from core.fileinteraction import FileValidation

import pandas as pd

class MainFrame(ContainerFrame):
    def __init__(self, container):
        super().__init__(container)


        container.style.configure("MainFrame.TButton", font="Arial 25", foreground="black")

        if container.dbinteraction.active_profile == "":
            self.no_profile()

        center_container = ttk.Frame(self, style="Card", padding=(5, 6, 7, 8))
        left_frame = ttk.Frame(center_container)
        vert_separator = ttk.Separator(center_container, orient="vertical")
        right_frame = ttk.Frame(center_container)

        general_info = ttk.Label(center_container, font="Arial 20",
                                text="Importiere einen Datensatz und ...")

        analyse_info = ttk.Label(left_frame, font="Arial 20",
                                text="... führe eine Intra-, bzw. Inter-Rater-Analyse durch:")

        analyse_buton = ttk.Button(left_frame, text="Analysieren", image=container.analyse_icon, compound="left",
                                   style="MainFrame.TButton", command=lambda: self.start_mode("analyse"))

        rate_info = ttk.Label(right_frame, font="Arial 20",
                                text="... bewerte den Text, um eine\nIntra-Rater-Reliability-Untersuchung zu erstellen:")
        rate_button = ttk.Button(right_frame, text="Bewerten", image=container.rate_icon, compound="left",
                                 style="MainFrame.TButton", command=lambda: self.start_mode("rate"))

        self.menu_bar.grid(row=0, column=0, sticky="nsew")
        center_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        general_info.grid(row=0, column=0, columnspan=3, pady=10)
        left_frame.grid(row=1, column=0)
        vert_separator.grid(row=1, column=1, sticky="nsew", pady=50)
        right_frame.grid(row=1, column=2)

        analyse_info.pack(pady=(0, 100))
        analyse_buton.pack(pady=(0, 200), ipadx=10, ipady=10)

        rate_info.pack(pady=(0, 100))
        rate_button.pack(pady=(0, 200), ipadx=10, ipady=10)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        center_container.rowconfigure(1, weight=1)
        center_container.columnconfigure(0, weight=1)
        center_container.columnconfigure(2, weight=1)

    def start_mode(self, mode):
        self.container.mode = mode
        self.container.frames["ScaleFrame"].update_frame()
        self.container.show_frame("ScaleFrame")
    
    def no_profile(self):
        def start_cmd():
            if len(user_input.get()) == 0:
                messagebox.showerror(title="Profil anlegen", message="Bitte gib einen Namen an, um ein Profil anzulegen.")
            else:
                self.container.dbinteraction.create_profile(user_input.get())
                profile_window.destroy()
                
        user_input = tk.StringVar(value="") # Beinhaltet Namen, falls ein neues Profil angelegt wird.
        profile_window = tk.Toplevel(self.container) # Neues Fenster
        profile_window.title("Profil erstellen")
        profile_window.geometry("500x250")
        profile_window.resizable(False, False)

        container_frame = ttk.Frame(profile_window)

        welcome_label = ttk.Label(container_frame, text="Willkommen!", font="Arial 18 bold")
        profile_label = ttk.Label(container_frame, text="Es wurde noch kein Profil angelegt.\nWie möchtest du heißen?", font="Arial 16")

        input_container = ttk.Frame(container_frame)
        name_label = ttk.Label(input_container, text="Name:", font="Arial 16",
                               image=self.container.face_icon, compound="left")
        input = ttk.Entry(input_container, textvariable=user_input)

        start_button = ttk.Button(container_frame, text="Starten", command=start_cmd)

        container_frame.pack(fill="both", expand=True)

        welcome_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=(10, 5))
        profile_label.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        input_container.grid(row=2, column=0, sticky="nsew", padx=15, pady=20)

        name_label.pack(side="left", padx=(60, 0))
        input.pack(side="right", padx=(0, 60))

        start_button.grid(row=3, column=0, padx=15, pady=8)

        # Responsive Design
        container_frame.columnconfigure(0, weight=1)

    def help_cmd(self,event=None):
        MainHelpFrame(self.container)