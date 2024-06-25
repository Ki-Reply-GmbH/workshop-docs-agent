"""A module for creating a graphical user interface (GUI) for scale and weight
selection, and file import using tkinter.

Classes:

ScaleFrame
A class to represent the ScaleFrame for scale and weight selection GUI.

FileFrame
A class to represent the FileFrame for file import GUI.
"""


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font

from gui.containerframe import ContainerFrame
from gui.helperframes import ScaleHelpFrame, ImportHelpFrame
from core.fileinteraction import FileValidation

import pandas as pd


class ScaleFrame(ContainerFrame):
    """A class to represent the ScaleFrame for scale and weight selection GUI.
    
    This class extends ContainerFrame and sets up the graphical user interface
    components for selecting scale types and weights. It includes methods to
    initialize the frame, populate scale types and weights, handle navigation,
    display help instructions, and update the frame based on the current mode.
    """
    def __init__(self, container):
        """Initializes the ScaleFrame class, setting up the GUI components for scale and
        weight selection.
        
        This constructor method sets up the ScaleFrame class by configuring styles,
        creating and arranging various widgets, and setting up the layout for the scale
        and weight selection interface. It includes labels, containers, and buttons to
        guide the user through the selection process.
        
        :param container: The main application container that holds the frames and
        shared data.
        :type container: object
        :returns: None
        """
        super().__init__(container)
        self.scale_types = ["nominal", "ordinal", "intervall", "ratio"]
        self.weights = ["identity", "linear", "quadratic", "bipolar", "circular", "ordinal", "radial", "ratio"]

        self.selected_scale = tk.StringVar()

        self.selected_weight = tk.StringVar()

        container.style.configure("FileFrame.TMenubutton", font="Arial 18", foreground="black", width=10)

        self.center_container = ttk.Frame(self, style="Card", padding=(5, 6, 7, 8))
        next_button = ttk.Button(self.center_container, text="Weiter", style="FileFrame.TButton",
                                    command=self.next_cmd)
        self.menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.center_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        tk.Frame(self.center_container).grid(row=3, column=0, columnspan=3) # Separator, der den Button ganz unten erscheinen lässt.
        next_button.grid(row=4, column=0, columnspan=3)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.center_container.columnconfigure(0, weight=1)
        self.center_container.rowconfigure(0, weight=1)
        self.center_container.rowconfigure(1, weight=1)
        self.center_container.rowconfigure(2, weight=1)
        self.center_container.rowconfigure(3, weight=1)



    def populate_frame(self, mode):
        """Populates the frame based on the given mode.
        
        Depending on the mode, this method populates the frame with the appropriate
        UI elements for selecting scale types and weights.
        
        :param mode: The mode to determine which UI elements to populate.
        :type mode: str
        :returns: None
        """
        if mode == "analyse":
            self.populate_scaletype()
            self.populate_weights()
        else:
            self.populate_scaletype()
    
    def populate_weights(self):
            """Populates the weight selection UI elements.
            
            This method creates and arranges the widgets for selecting a weight type and
            provides informational labels describing each weight type. The widgets are
            added to the `center_container` frame.
            
            :returns: None
            """
            weights_label = ttk.Label(self.center_container, font="Arial 22",
                                    text="Gewichte")
            weights_menu = ttk.OptionMenu(self.center_container, self.selected_weight, "identity", *self.weights,
                                        style="FileFrame.TMenubutton")
            
            infolabel_container = ttk.Frame(self.center_container)
            weights_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Legen fest in welchem Verhältnis die Kategorien zueinander stehen.")
            identity_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Identity entspricht den ungewichteten Metriken.\n  Übereinstimmung nur dann, wenn exakt die gleiche\n  Kategorie ausgewählt wurde. ")
            linear_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Üblich sind die Gewichte identity, linear, oder quadratic.")
            
            weights_label.grid(row=0, column=1, pady=10)
            weights_menu.grid(row=1, column=1, pady=20)
            infolabel_container.grid(row=2, column=1, pady=10)

            weights_infolabel.pack(fill="x", pady=5)
            identity_infolabel.pack(fill="x", pady=5)
            linear_infolabel.pack(fill="x", pady=5)

            self.center_container.columnconfigure(0, weight=1)

    def populate_scaletype(self):
            """Populates the scale type selection UI elements.
            
            This method creates and arranges the widgets for selecting a scale type and
            provides informational labels describing each scale type. The widgets are added
            to the `center_container` frame.
            
            :returns: None
            """
            scale_format_label = ttk.Label(self.center_container, font="Arial 22",
                                    text="Skalenformat")
            scale_menu = ttk.OptionMenu(self.center_container, self.selected_scale, "nominal", *self.scale_types,
                                        style="FileFrame.TMenubutton")
            
            infolabel_container = ttk.Frame(self.center_container)
            nominal_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Nominalskala: Objekte werden nur mit Namen versehen.")
            ordinal_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Ordinalskala: Es gibt zusätzlich eine Äquivalenz- und\n  Ordungsrelation.")
            intervall_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Intervallskala: Zusätzlich sind Abstände/Intervall definierbar.")
            rational_infolabel = ttk.Label(infolabel_container, font="Arial 18",
                                    text="• Rationalskala: Es gibt zusätzlich einen Nullpunkt.")
            
            scale_format_label.grid(row=0, column=0, pady=10)
            scale_menu.grid(row=1, column=0, pady=20)
            infolabel_container.grid(row=2, column=0, pady=10)

            nominal_infolabel.pack(fill="x", pady=5)
            ordinal_infolabel.pack(fill="x", pady=5)
            intervall_infolabel.pack(fill="x", pady=5)
            rational_infolabel.pack(fill="x", pady=5)

            self.center_container.columnconfigure(0, weight=1)
    
    def next_cmd(self):
        """Updates the container's scale format and weights, then navigates to the
        FileFrame.
        
        This method sets the container's `scale_format` to the selected scale and,
        if in 'analyse' mode, sets the container's `weights` to the selected weight.
        It then updates and displays the 'FileFrame'.
        
        :returns: None
        """
        self.container.scale_format = self.selected_scale.get()
        if self.container.mode == "analyse":
            self.container.weights = self.selected_weight.get()
        
        self.container.frames["FileFrame"].update_frame()
        self.container.show_frame("FileFrame")
    
    def help_cmd(self,event=None):
        """Displays the help frame for scale selection instructions.
        
        This method creates an instance of the `ScaleHelpFrame` class, which provides
        guidance on how to select scales correctly.
        
        :param event: Optional event parameter for binding with GUI events.
        :type event: tkinter.Event, optional
        :returns: None
        """
        ScaleHelpFrame(self.container)

    def update_frame(self):
        """Updates the frame by clearing non-button and non-frame widgets and repopulating
        it based on the current mode.
        
        This method iterates through the children of `center_container`, destroying any
        widget that is not a button or a frame. It then repopulates the frame according
        to the current mode of the container.
        
        :returns: None
        """
        for widget in self.center_container.winfo_children():
            if not isinstance(widget, tk.ttk.Button) and not isinstance(widget, tk.Frame):
                widget.destroy()
        self.populate_frame(self.container.mode)


class FileFrame(ContainerFrame):
    """A class to represent the FileFrame for file import GUI.
    
    This class extends ContainerFrame and sets up the graphical user interface
    components for importing files. It includes methods to initialize the frame,
    populate format previews, select files, display help instructions, and update
    the frame.
    """
    def __init__(self, container):
        """Initializes the FileFrame class, setting up the GUI components for file import.
        
        This constructor method sets up the FileFrame class by configuring styles, creating
        and arranging various widgets, and setting up the layout for the file import
        interface. It includes labels, containers, and buttons to guide the user through
        the file import process.
        
        :param container: The main application container that holds the frames and shared data.
        :type container: object
        :returns: None
        """
        super().__init__(container)
        container.style.configure("FileFrame.TButton", font="Arial 18", foreground="black")

        center_container = ttk.Frame(self, style="Card", padding=(5, 6, 7, 8))
        file_import_label = ttk.Label(center_container, font="Arial 20",
                                text="Datei importieren")
        accepted_formats_label = ttk.Label(center_container, font="Arial 20",
                                text="Es werden zwei Formate akzeptiert")
        
        format_1_label = ttk.Label(center_container, font="Arial 20",
                                text="Format 1:")
        
        self.format_1_container = ttk.Frame(center_container)
        self.format_1_bulletlist_container = ttk.Frame(center_container)
    
        format_2_label = ttk.Label(center_container, font="Arial 20",
                                text="Format 2:")

        self.format_2_container = ttk.Frame(center_container)
        self.format_2_bulletlist_container = ttk.Frame(center_container)

        self.format_1_2_bulletlist_container = ttk.Frame(center_container)

        select_file_button = ttk.Button(center_container, text="Datei auswählen", style="FileFrame.TButton",
                                        command=lambda: self.select_file(container))

        center_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        file_import_label.grid(row=0, column=0, columnspan=3, pady=10)
        accepted_formats_label.grid(row=1, column=0, columnspan=3, pady=10)

        format_1_label.grid(row=2, column=0, pady=15)
        format_2_label.grid(row=2, column=2, pady=15)

        self.format_1_container.grid(row=3, column=0, padx=15)
        ttk.Frame(center_container).grid(row=2, rowspan=2, column=1, sticky="nsew") # Trennt format_1_container und format_2_container voneinander.
        self.format_2_container.grid(row=3, column=2, padx=15)

        self.format_1_bulletlist_container.grid(row=4, column=0, padx=15, pady=(15, 0))

        self.format_2_bulletlist_container.grid(row=4, column=2, padx=15, pady=(15, 0))

        self.format_1_2_bulletlist_container.grid(row=5, column=0, columnspan=3)

        ttk.Frame(center_container).grid(row=6, column=0, columnspan=3) # Separator, der den Button ganz unten erscheinen lässt.
        select_file_button.grid(row=7, column=0, columnspan=3)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        center_container.columnconfigure(1, weight=1)
        center_container.rowconfigure(6, weight=1)


    def populate_format_preview(self, format_container):
        """Populates the format preview based on the selected scale format and container.
        
        Depending on the scale format (nominal, ordinal, etc.) and the specified format
        container, this method creates a table with appropriate headings and content.
        It also adds relevant informational labels to guide the user about the required
        headers and data format.
        
        :param format_container: The container to populate with the format preview.
        :type format_container: ttk.Frame
        :returns: None
        """
        if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
            if format_container == self.format_1_container:
                headings = ["Categories", "Rater ID", "Sentiment Analysis\nis nice!", "If I run the code in\nthe GUI, it just hangs."]
                content = [["positive", "Alice", "positive", "neutral"],
                            ["neutral", "Bob", "positive", "negative"],
                            ["negative"]]
            
                self.create_table(self.format_1_container, headings, content)

                rater_id_infolabel = ttk.Label(self.format_1_bulletlist_container, font="Arial 18",
                        text="• Header \"Rater ID\" muss in Datei vorkommen.")
                rater_id_infolabel.pack(fill="x", pady=5)
            else:
                headings = ["Categories", "Subject", "Alice", "Bob"]
                content = [["positive", "Sentiment Analysis\nis nice!", "positive", "positive"],
                            ["neutral", "If I run the code in\nthe GUI, it just hangs.", "neutral", "negative"],
                            ["negative"]]
            
                self.create_table(self.format_2_container, headings, content)

                text_infolabel = ttk.Label(self.format_2_bulletlist_container, font="Arial 18",
                                        text="• Header \"Subject\" muss in Datei vorkommen.")
                text_infolabel.pack(fill="x", pady=5)
                
                categories_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text="• Header \"Categories\" in beiden Formaten.")
                
                if self.container.scale_format == "nominal":
                    info_txt = "• Kategorienamen angeben; hier: positive, neutral, negative."
                else:
                    info_txt = "• Kategorienamen in sortierter Reihenfolge angeben.\n  (aufsteigend, oder absteigend)"

                category_entries_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text=info_txt)
                black_headers_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text="• Spalten mit schwarzen Header werden automatisch erkannt.")
                other_columns_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text="• Andere Spalten werden ignoriert.")

                categories_infolabel.pack(fill="x", pady=5)
                category_entries_infolabel.pack(fill="x", pady=5)
                black_headers_infolabel.pack(fill="x", pady=5)
                other_columns_infolabel.pack(fill="x", pady=5)
        else:
            if format_container == self.format_1_container:
                headings = ["Rater ID", "Herzfrequenz\n24.01. 16:30", "Herzfrequenz\n24.01. 17:00"]
                content = [["Alice", "121.5", "89"],
                            ["Bob", "123", "75"]]
            
                self.create_table(self.format_1_container, headings, content)

                rater_id_infolabel = ttk.Label(self.format_1_bulletlist_container, font="Arial 18",
                        text="• Header \"Rater ID\" muss in Datei vorkommen.")
                rater_id_infolabel.pack(fill="x", pady=15)
            else:
                headings = ["Subject", "Alice", "Bob"]
                content = [["Herzfrequenz\n24.01. 16:30", "121.5", "123"],
                            ["Herzfrequenz\n24.01. 17:00", "89", "75"]]
            
                self.create_table(self.format_2_container, headings, content)

                text_infolabel = ttk.Label(self.format_2_bulletlist_container, font="Arial 18",
                                        text="• Header \"Subject\" muss in Datei vorkommen.")
                text_infolabel.pack(fill="x", pady=15)

                other_columns_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text="• Spalten die davor auftauchen werden ignoriert.")
                
                subjects_infolabel = ttk.Label(self.format_1_2_bulletlist_container, font="Arial 18",
                                        text="• Danach ausschließlich Spalten mit den Messergebnissen.")
                
                other_columns_infolabel.pack(fill="x", pady=15)
                subjects_infolabel.pack(fill="x", pady=15)


    def select_file(self, container):
        """Selects a file, validates it, and updates the container with the file's data.
        
        This method opens a file dialog for the user to select a file. It then validates
        the selected file and updates the container with the file's categories, rater
        IDs, text, formatted text, and labels. Depending on the mode of the container,
        it updates and shows the appropriate frame.
        
        :param container: The main application container that holds the frames and
        shared data.
        :type container: object
        :returns: None
        :raises Exception: If there is an error during file import or validation, an
        error message is displayed.
        """
        filename = tk.filedialog.askopenfilename(filetypes=[
            ("Excel files", ".xlsx .xls"), 
            ("Libreoffice Calc files", ".ods"),
            ("Csv files", ".csv")
            ])

        if filename == "":
            return

        try:
            container.filevalidation = FileValidation(filename, self.container.scale_format)
            container.categories = container.filevalidation.categories
            container.rater_ids = container.filevalidation.rater_ids
            container.text = container.filevalidation.text
            container.formatted_text = container.filevalidation.formatted_text
            container.labels = container.filevalidation.labels
        except:
            messagebox.showerror(title="Error", message="Fehler beim importieren der Datei. Auf passendes Format geachtet?")
            return

        if container.mode == "analyse":
            container.frames["AnalyseFrame"].update_frame()
            container.show_frame("AnalyseFrame")
        elif container.mode == "rate":
            result = messagebox.askyesno(title="Reihenfolge", message="Soll die Reihenfolge der Bewertungsobjekte zufällig sein?")
            if result:
                container.frames["RateFrame"].update_frame(mode="do")
            else:
                container.frames["RateFrame"].update_frame()
            container.show_frame("RateFrame")
        else:
            #TODO Fehlermeldung / Fehlerframe ausgeben
            container.show_frame("MainFrame")

    def help_cmd(self,event=None):
        # Jedes Frame erzeugt ein HelpFrame mit eigenen Inhalten.
        # Wird in den vererbten Klassen implementiert.
        """Displays the help frame for file import instructions.
        
        This method creates an instance of the `ImportHelpFrame` class, which provides
        guidance on how to import files correctly.
        
        :param event: Optional event parameter for binding with GUI events.
        :type event: tkinter.Event, optional
        :returns: None
        """
        ImportHelpFrame(self.container)

    def update_frame(self):
        # Widgets aus vorheriger Session löschen, falls User über Home-Button den Frame erneut öffnet.
        """Updates the frame by clearing all existing widgets and repopulating it with
        the format preview.
        
        This method ensures that any widgets from a previous session are removed
        before repopulating the frame with the updated format preview.
        
        :returns: None
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

        # Frames neu befüllen
        self.populate_format_preview(self.format_1_container)
        self.populate_format_preview(self.format_2_container)













