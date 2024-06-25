import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
from gui.containerframe import ContainerFrame
from gui.helperframes import ScaleHelpFrame, ImportHelpFrame
from core.fileinteraction import FileValidation
import pandas as pd

class FileFrame(ContainerFrame):
    """    This function does something.  
      
    Parameters:  
        arg1 (type): Description of arg1  
        arg2 (type): Description of arg2  
      
    Returns:  
        type: Description of return value  """

    def help_cmd(self, event=None):
        ImportHelpFrame(self.container)

    def update_frame(self):
        """     This function does something.

            Parameters:
            arg1 (type): Description of arg1
            arg2 (type): Description of arg2

            Returns:
            type: Description of return value

        """
        for widget in self.format_1_container.winfo_children():
            widget.destroy()
        for widget in self.format_2_container.winfo_children():
            widget.destroy()
        for widget in self.format_1_bulletlist_container.winfo_children():
            widget.destroy()
        for widget in self.format_2_bulletlist_container.winfo_children():
            widget.destroy()
        for widget in self.format_1_2_bulletlist_container.winfo_children():
            widget.destroy()
        self.populate_format_preview(self.format_1_container)
        self.populate_format_preview(self.format_2_container)