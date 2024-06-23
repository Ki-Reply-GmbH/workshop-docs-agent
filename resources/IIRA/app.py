__author__ = "Timo Kubera"
__email__ = "timo.kubera@stud.uni-hannover.de"

import os
import tkinter as tk
from tkinter import ttk

from gui.mainframe import MainFrame
from gui.fileframes import FileFrame, ScaleFrame
from gui.analyseframe import AnalyseFrame, ResultsFrame
from gui.rateframe import RateFrame
from core.fileinteraction import DBInteraction

from PIL import ImageTk

file_path = os.path.dirname(os.path.realpath(__file__))

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.load_icons()

        self.filevalidation = None
        self.dbinteraction = DBInteraction(os.path.join(file_path, "data/internal_db.csv"))
        self.scale_format = ""      # Skalenformate sind nominal, ordinal, intervall und ratio.
        self.weights = ""
        
        self.categories = []
        self.rater_ids = []
        self.text = []
        self.formatted_text = []
        self.labels = {} # Label pro Text und Rater

        self.title("IIRA")
        self.geometry("1500x750")
        self.minsize(1450, 750)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.light_mode = True
        self.mode = None

        self.tk.call("source", os.path.join(file_path, "data/themes/forest-light.tcl"))
        self.style = ttk.Style()

        self.style.theme_use("forest-light")

        self.frames = {} 
        self.init_frames()
        self.show_frame("MainFrame")
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def load_icons(self):
        self.app_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/intrarater_512px.png"))
        self.file_select_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/file_select.png"))
        self.home_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/home_32px.png"))
        self.profile_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/profile_32px.png"))
        self.help_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/help_32px.png"))
        self.face_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/face_32px.png"))
        self.rate_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/rate.png"))
        self.analyse_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/analyse.png"))
        self.tooltip_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/tooltip-16px.png"))
        self.save_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/save_32px.png"))
        self.delete_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/delete_32px.png"))
        
        self.light_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/light_mode_32px.png"))
        self.dark_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/icons/dark_mode.png"))
        self.unchecked_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/themes/forest-light/check-unsel-accent.png"))
        self.checked_icon = ImageTk.PhotoImage(file=os.path.join(file_path, "data/themes/forest-light/check-accent.png"))

    def init_root_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
    
    def init_frames(self):
        for frame in self.frames:
            for widget in self.frames[frame].winfo_children():
                widget.destroy()

        main_frame = MainFrame(self)
        self.init_root_frame(main_frame)
        self.frames["MainFrame"] = main_frame

        scale_frame = ScaleFrame(self)
        self.init_root_frame(scale_frame)
        self.frames["ScaleFrame"] = scale_frame

        file_frame = FileFrame(self)
        self.init_root_frame(file_frame)
        self.frames["FileFrame"] = file_frame

        rate_frame = RateFrame(self)
        self.init_root_frame(rate_frame)
        self.frames["RateFrame"] = rate_frame

        restults_frame = ResultsFrame(self)
        self.init_root_frame(restults_frame)
        self.frames["ResultsFrame"] = restults_frame

        analyse_frame = AnalyseFrame(self)
        self.init_root_frame(analyse_frame)
        self.frames["AnalyseFrame"] = analyse_frame



if __name__ == "__main__":
  app = App()
  app.mainloop()