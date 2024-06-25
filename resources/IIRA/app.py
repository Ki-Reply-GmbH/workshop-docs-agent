__author__ = 'Timo Kubera'
__email__ = 'timo.kubera@stud.uni-hannover.de'
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
    """    Main application class that inherits from tkinter.Tk. Initializes the main application window and its components, including loading icons, setting up the database interaction, and configuring the main frames."""

    def __init__(self):
        """    Initializes the App class.

    Sets up the main application window, loads icons, initializes database interaction, and configures the main frames.

    Attributes:
        filevalidation (None): Placeholder for file validation logic.
        dbinteraction (DBInteraction): Handles database interactions using the specified CSV file.
        scale_format (str): Format for the scale, initialized as an empty string.
        weights (str): Weights for the scale, initialized as an empty string.
        categories (list): List of categories, initialized as an empty list.
        rater_ids (list): List of rater IDs, initialized as an empty list.
        text (list): List of text data, initialized as an empty list.
        formatted_text (list): List of formatted text data, initialized as an empty list.
        labels (dict): Dictionary of labels, initialized as an empty dictionary.
        light_mode (bool): Flag to indicate if the application is in light mode, initialized as True.
        mode (None): Placeholder for the mode of the application.
        style (ttk.Style): Style object for configuring the application's theme.
        frames (dict): Dictionary to hold the application's frames."""
        super().__init__()
        self.load_icons()
        self.filevalidation = None
        self.dbinteraction = DBInteraction(os.path.join(file_path, 'data/internal_db.csv'))
        self.scale_format = ''
        self.weights = ''
        self.categories = []
        self.rater_ids = []
        self.text = []
        self.formatted_text = []
        self.labels = {}
        self.title('IIRA')
        self.geometry('1500x750')
        self.minsize(1450, 750)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.light_mode = True
        self.mode = None
        self.tk.call('source', os.path.join(file_path, 'data/themes/forest-light.tcl'))
        self.style = ttk.Style()
        self.style.theme_use('forest-light')
        self.frames = {}
        self.init_frames()
        self.show_frame('MainFrame')

    def show_frame(self, frame_name):
        """    Displays the specified frame by bringing it to the front.

    Args:
        frame_name (str): The name of the frame to be displayed."""
        frame = self.frames[frame_name]
        frame.tkraise()

    def load_icons(self):
        """    Loads the icons used in the application from the specified file paths.

    Attributes:
        app_icon (ImageTk.PhotoImage): Icon for the application.
        file_select_icon (ImageTk.PhotoImage): Icon for file selection.
        home_icon (ImageTk.PhotoImage): Icon for the home button.
        profile_icon (ImageTk.PhotoImage): Icon for the profile button.
        help_icon (ImageTk.PhotoImage): Icon for the help button.
        face_icon (ImageTk.PhotoImage): Icon for the face button.
        rate_icon (ImageTk.PhotoImage): Icon for the rate button.
        analyse_icon (ImageTk.PhotoImage): Icon for the analyse button.
        tooltip_icon (ImageTk.PhotoImage): Icon for tooltips.
        save_icon (ImageTk.PhotoImage): Icon for the save button.
        delete_icon (ImageTk.PhotoImage): Icon for the delete button.
        light_icon (ImageTk.PhotoImage): Icon for light mode.
        dark_icon (ImageTk.PhotoImage): Icon for dark mode.
        unchecked_icon (ImageTk.PhotoImage): Icon for unchecked state.
        checked_icon (ImageTk.PhotoImage): Icon for checked state."""
        self.app_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/intrarater_512px.png'))
        self.file_select_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/file_select.png'))
        self.home_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/home_32px.png'))
        self.profile_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/profile_32px.png'))
        self.help_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/help_32px.png'))
        self.face_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/face_32px.png'))
        self.rate_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/rate.png'))
        self.analyse_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/analyse.png'))
        self.tooltip_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/tooltip-16px.png'))
        self.save_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/save_32px.png'))
        self.delete_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/delete_32px.png'))
        self.light_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/light_mode_32px.png'))
        self.dark_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/icons/dark_mode.png'))
        self.unchecked_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/themes/forest-light/check-unsel-accent.png'))
        self.checked_icon = ImageTk.PhotoImage(file=os.path.join(file_path, 'data/themes/forest-light/check-accent.png'))

    def init_root_frame(self, frame):
        """    Initializes the root frame by setting its grid configuration.

    Args:
        frame (tk.Frame): The frame to be initialized."""
        frame.grid(row=0, column=0, sticky='nsew')

    def init_frames(self):
        """    Initializes all the main frames of the application, including MainFrame, ScaleFrame, FileFrame, RateFrame, ResultsFrame, and AnalyseFrame.

    Attributes:
        frames (dict): Dictionary to hold the application's frames."""
        for frame in self.frames:
            for widget in self.frames[frame].winfo_children():
                widget.destroy()
        main_frame = MainFrame(self)
        self.init_root_frame(main_frame)
        self.frames['MainFrame'] = main_frame
        scale_frame = ScaleFrame(self)
        self.init_root_frame(scale_frame)
        self.frames['ScaleFrame'] = scale_frame
        file_frame = FileFrame(self)
        self.init_root_frame(file_frame)
        self.frames['FileFrame'] = file_frame
        rate_frame = RateFrame(self)
        self.init_root_frame(rate_frame)
        self.frames['RateFrame'] = rate_frame
        restults_frame = ResultsFrame(self)
        self.init_root_frame(restults_frame)
        self.frames['ResultsFrame'] = restults_frame
        analyse_frame = AnalyseFrame(self)
        self.init_root_frame(analyse_frame)
        self.frames['AnalyseFrame'] = analyse_frame
if __name__ == '__main__':
    app = App()
    app.mainloop()