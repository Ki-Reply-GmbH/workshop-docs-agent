import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import os

from gui.helperframes import ProfileFrame

class ContainerFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.accent_color = "#217346"
        container.style.configure("TopFrame.TFrame", background=self.accent_color)
        self.menu_bar = ttk.Frame(self)
        self.init_menu_bar()

    def init_menu_bar(self):
        # GUI-Elemente
        home_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        home_label = ttk.Label(home_frame, text="Home", image=self.container.home_icon, compound="top", font="Arial 12")
        home_frame.bind("<Enter>", lambda x: self.on_enter(home_frame, home_label))
        home_frame.bind("<Leave>", lambda x: self.on_leave(home_frame, home_label))
        home_label.bind("<Button-1>", lambda x: self.home_cmd())
        home_frame.bind("<Button-1>", lambda x: self.home_cmd())

        profile_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        profile_label = ttk.Label(profile_frame, text="Profil", image=self.container.profile_icon, compound="top", font="Arial 12")
        profile_frame.bind("<Enter>", lambda x: self.on_enter(profile_frame, profile_label))
        profile_frame.bind("<Leave>", lambda x: self.on_leave(profile_frame, profile_label))
        #TODO Profil wechseln
        profile_label.bind("<Button-1>", lambda x: self.profile_cmd())
        profile_frame.bind("<Button-1>", lambda x: self.profile_cmd())

        horizon_separator = ttk.Separator(self.menu_bar, orient="horizontal")
        vert_separator = ttk.Separator(self.menu_bar, orient="vertical")
        
        self.help_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        self.help_label = ttk.Label(self.help_frame, text="Hilfe", image=self.container.help_icon, compound="top", font="Arial 12")
        self.help_label.bind("<Enter>", lambda x: self.on_enter(self.help_frame, self.help_label))
        self.help_label.bind("<Leave>", lambda x: self.on_leave(self.help_frame, self.help_label))
        self.help_frame.bind("<Button-1>", self.help_cmd)
        self.help_label.bind("<Button-1>", self.help_cmd)

        home_frame.grid(row=0, column=0, sticky="nsew")
        profile_frame.grid(row=0, column=1, sticky="nsew")
        #color_frame.grid(row=0, column=2, sticky="nsew")
        self.help_frame.grid(row=0, column=3, sticky="nsew")
        horizon_separator.grid(row=1, column=0, columnspan=4, sticky="nsew")
        vert_separator.grid(row=0, column=4, sticky="nsew")

        home_label.place(relx=0.5, rely=0.5, anchor="center")
        profile_label.place(relx=0.5, rely=0.5, anchor="center")
        #color_label.place(relx=0.5, rely=0.5, anchor="center")
        self.help_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_enter(self, frame, label):
        if frame is not None:
            frame.configure(style="TopFrame.TFrame")
        label["background"] = self.accent_color

    def on_leave(self, frame, label):
        if frame is not None:
            frame.configure(style="TFrame")
        label["background"] = ttk.Style().lookup("TFrame", "background")

    def toggle_color_mode(self):
        if self.container.light_mode:
            self.container.light_mode = False
            self.container.style.theme_use("forest-dark")
        else:
            self.container.light_mode = True
            self.container.style.theme_use("forest-light")

    
    def create_table(self, parent, headings, content):
        rowspan = max(len(content) + 2, 2)
        columnspan = max(len(headings) * 2, 2)
        index = 0
        for heading in headings:
            heading_lbl = ttk.Label(parent, text=heading, font="Arial 15 bold")
            heading_lbl.grid(row=0, column=index)

            if heading != headings[-1]: 
                vert_separator = ttk.Separator(parent, orient="vertical")
                vert_separator.grid(row=0, column=index+1, rowspan=rowspan ,sticky="nsew", padx=5)

            index += 2

        horizon_separator = ttk.Separator(parent, orient="horizontal")
        horizon_separator.grid(row=1, column=0, columnspan=columnspan, sticky="nsew", pady=5)

        for i, row in enumerate(content, start=2):
            index = 0
            for cell in row:
                if isinstance(cell, str):
                    cell_lbl = ttk.Label(parent, text=cell, font="Arial 15")
                    cell_lbl.grid(row=i, column=index, pady=5)
                elif isinstance(cell, list):
                    pass
                else:
                    cell_chkbtn = ttk.Checkbutton(parent, variable=cell)
                    cell_chkbtn.grid(row=i, column=index, pady=5)

                index += 2

    def profile_cmd(self):
        ProfileFrame(self.container)

    def home_cmd(self):
        self.container.init_frames()

        self.container.show_frame("MainFrame")

    def help_cmd(self, event=None):
        raise NotImplementedError
        
    def update_frame(self):
        raise NotImplementedError       # Wird in den vererbten Klassen implementiert.
