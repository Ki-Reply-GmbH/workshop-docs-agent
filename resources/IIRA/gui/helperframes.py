"""This module provides a graphical user interface (GUI) for managing user profiles,
creating scrollable frames, and displaying help dialogs using the tkinter library.

Classes:

ProfileFrame
A class to create a user interface for managing user profiles.

ScrollFrame
A class to create a scrollable frame using a canvas and a vertical scrollbar.

MainHelpFrame
A class to create a help dialog window for providing information about the
main functionalities of the application, organized into tabs with detailed
help text.

ScaleHelpFrame
A class to create a help dialog window for providing information on scales
and weights, organized into tabs with detailed help text and interactive
elements.

ImportHelpFrame
A class to create a help dialog window for providing information on importing
data formats, organized into tabs with detailed help text for each format.

PrepAnalyseHelpFrame
A class to create a help dialog window for providing information on preparing
an analysis, including selecting raters and metrics. The window is organized
into tabs with detailed help text and hyperlinks for further information.

ResultsHelpFrame
A class to create a help dialog window for providing information about the
results of reliability analyses.

RateHelpFrame
A class to create a help dialog window for providing information about the
rating functionality in the application.

Functions:

callback(url)
Opens the provided URL in a web browser.
"""


import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import platform
import os
import webbrowser


file_path = os.path.dirname(os.path.realpath(__file__))
urls = ["https://irrcac.readthedocs.io/en/latest/irrCAC.html#module-irrCAC.weights",
        "https://journals.sagepub.com/doi/pdf/10.1177/001316446002000104",
        "https://psycnet.apa.org/record/1980-29309-001",
        "https://psycnet.apa.org/record/1972-05083-001",
        "https://www.narcis.nl/publication/RecordID/oai:repository.ubn.ru.nl:2066%2F54804",
        "https://bpspsychub.onlinelibrary.wiley.com/doi/abs/10.1348/000711006X126600",
        "https://agreestat.com/papers/wiley_encyclopedia2008_eoct631.pdf"
        ]

class ProfileFrame(tk.Toplevel):
    """A class to create a user interface for managing user profiles.
    """
    def __init__(self, container):
        """Initializes the ProfileFrame class, which creates a user interface for managing
        user profiles.
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Initializes a StringVar for user input.
        - Sets the window title to 'Profil' and configures its geometry and
        non-resizable properties.
        - Creates and configures various widgets including labels, buttons, and frames.
        - Populates the profile change menu with available profiles.
        - Arranges the widgets using grid and pack layout managers.
        - Configures the row weights for responsive design.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        """
        super().__init__(container)
        self.container = container

        self.user_input = tk.StringVar(value="")

        self.title("Profil")
        self.geometry("500x300")
        self.resizable(False, False)

        container_frame = ttk.Frame(self)

        signed_in_as_label = ttk.Label(container_frame, text="Angemeldet als", font="Arial 18")
        self.profile_name_label = ttk.Label(container_frame, text=self.container.dbinteraction.active_profile,
                                        font="Arial 18", image=self.container.face_icon, compound="left")

        self.separator_frame = ttk.Frame(container_frame)
        create_delete_container = ttk.Frame(container_frame)

        button_container = ttk.Frame(container_frame)
        create_profile_button = ttk.Button(create_delete_container, text="Profil anlegen", command=self.create_new_profile)
        delete_profile_button  = ttk.Button(create_delete_container, text="Profil löschen", command=self.delete_profile)
        ok_button = ttk.Button(button_container, text="Ok", style="Accent.TButton", command=self.ok_cmd)

        self.change_profile_mbutton = ttk.Menubutton(button_container, text="Profil wechseln")
        change_profile_menu = tk.Menu(self.change_profile_mbutton, tearoff=False)
        self.change_profile_mbutton.configure(menu=change_profile_menu)
        profile_selection = tk.StringVar()
        for user in self.container.dbinteraction.profiles:
            change_profile_menu.add_radiobutton(variable=profile_selection, value=user,
                                                label=user, command=lambda: self.change_profile(profile_selection.get()))

        container_frame.pack(fill="both", expand=True)
        signed_in_as_label.grid(row=0, column=0, padx=15, pady=15)
        self.profile_name_label.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.separator_frame.grid(row=2, column=0, columnspan=2)
        create_delete_container.grid(row=3, column=0, rowspan=2, padx=15, pady=15)

        button_container.grid(row=4, column=1, columnspan=2)
        self.change_profile_mbutton.grid(row=0, column=1, padx=15, pady=15)
        ok_button.grid(row=0, column=2, padx=15, pady=15)

        create_profile_button.pack(side="top", pady=5)
        delete_profile_button.pack(side="bottom", pady=5)

        # Responsive Design
        container_frame.rowconfigure(2, weight=1)


    def ok_cmd(self, event=None):
        # event=None erforderlich für die Return-Taste
        """Handles the 'Ok' button click event.
        
        If the user input is empty, the window is closed. Otherwise, a new profile
        is created using the user input, and the profile label and change profile
        menu are updated. The user input field is then cleared, and any child
        widgets in the separator frame are destroyed.
        
        :param event: The event object (default is None).
        :returns: None
        """
        if len(self.user_input.get()) == 0:
            # Kein neues Profil angelegt; Fenster direkt schließen.
            self.destroy()
        else:
            # User-Input wurde gesetzt. Neues Profil wird angelegt.
            self.container.dbinteraction.create_profile(self.user_input.get()) # Das neu angelegt Profil wechseln.
            self.populate_profile_label()
            self.populate_change_profile_menu()
            self.user_input.set("")

            for widget in self.separator_frame.winfo_children():
                # Label und Input-Feld wieder aus der GUI entfernen.
                widget.destroy()

    def populate_profile_label(self):
        """Updates the profile name label with the active profile.
        
        This method retrieves the active profile name from the database interaction
        object and updates the text of the profile name label accordingly.
        
        :returns: None
        """
        self.profile_name_label.configure(text=self.container.dbinteraction.active_profile)

    def populate_change_profile_menu(self):
        """Populate the profile change menu with available profiles.
        
        This method creates a new menu for changing profiles and populates it with
        radio buttons for each profile stored in the database. When a profile is
        selected, the `change_profile` method is called to update the active profile.
        
        :returns: None
        """
        change_profile_menu = tk.Menu(self.change_profile_mbutton, tearoff=False)
        self.change_profile_mbutton.configure(menu=change_profile_menu)
        profile_selection = tk.StringVar()
        for user in self.container.dbinteraction.profiles:
            # Menü mit den gespeicherten Profilen füllen.
            change_profile_menu.add_radiobutton(variable=profile_selection, value=user,
                                                label=user, command=lambda:self.change_profile(profile_selection.get()))

    def create_new_profile(self):
        """Creates a new profile input field if none exists.
        
        This method checks if the separator frame has any child widgets. If not,
        it adds a label and an entry field for the user to input a new profile name.
        The entry field is bound to the Return key to trigger the `ok_cmd` method.
        
        :returns: None
        """
        if not self.separator_frame.winfo_children():
            # Falls der Button noch nicht gedrückt wurde, füge Input-Feld hinzu.
            name_label = ttk.Label(self.separator_frame, text="Name:", font="Arial 16")
            name_label.pack(side="left", padx=15)

            input = ttk.Entry(self.separator_frame, textvariable=self.user_input)
            input.bind("<Return>", self.ok_cmd)
            input.pack(side="right")

    def change_profile(self, profile_selection):
        """Changes the active profile to the selected profile and updates the UI.
        
        :param profile_selection: The name of the profile to switch to.
        :type profile_selection: str
        """
        self.container.dbinteraction.change_profile(profile_selection)
        self.populate_profile_label()
        self.populate_change_profile_menu()

    def delete_profile(self):
        """Deletes the current profile if there are multiple profiles available. If it is
        the only profile, shows an error message.
        
        :raises messagebox.showerror: If attempting to delete the only profile.
        """
        if len(self.container.dbinteraction.profiles) == 0:
            # Kein anderes Profil vorhanden. Dann darf das Aktuelle nicht gelöscht werden.
            messagebox.showerror(title="Einziges Profil", message="Das ist dein einziges Profil. Erstelle erst ein Neues, um es zu löschen.")
        else:
            self.container.dbinteraction.delete_profile()
            self.populate_profile_label()
            self.populate_change_profile_menu()


class ScrollFrame(ttk.Frame):
    """A class to create a scrollable frame using a canvas and a vertical scrollbar.
    """
    def __init__(self, parent):
        """Initializes the ScrollFrame class, which creates a scrollable frame using a
        canvas and a vertical scrollbar.
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (ttk.Frame).
        - Creates a vertical scrollbar and associates it with the canvas.
        - Creates a canvas with no border and no highlight, sets its background to
        white, and configures it to use the scrollbar for vertical scrolling.
        - Creates a viewport frame within the canvas to hold child widgets.
        - Packs the scrollbar to the right side of the frame, filling vertically.
        - Packs the canvas to the left side of the frame, expanding to fill the space.
        - Adds the viewport frame to the canvas as a window, anchored to the northwest.
        - Binds the '<Configure>' event of the viewport frame to the onFrameConfigure
        method to adjust the scroll region when the viewport size changes.
        - Binds the '<Configure>' event of the canvas to the onCanvasConfigure method
        to adjust the canvas window width when the canvas is resized.
        - Binds the '<Enter>' event of the viewport frame to the onEnter method to bind
        mouse wheel events when the cursor enters the control.
        - Binds the '<Leave>' event of the viewport frame to the onLeave method to
        unbind mouse wheel events when the cursor leaves the control.
        - Calls the onFrameConfigure method to perform an initial adjustment of the
        scroll region.
        
        :param parent: The parent container for this frame.
        :type parent: tkinter.Tk or tkinter.Toplevel
        """
        super().__init__(parent) # create a frame (self)

        self.vsb = ttk.Scrollbar(self, orient="vertical") #place a scrollbar on self 
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.vsb.set, background="#ffffff")          #place canvas on self
        self.viewPort = ttk.Frame(self.canvas)                                       #place a frame on the canvas, this frame will hold the child widgets 

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind("<Enter>", self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind("<Leave>", self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        """Adjusts the scroll region of the canvas based on the bounding box of all
        items within it.
        
        :param event: The event object containing information about the frame
        configure event.
        :type event: tkinter.Event
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        """Adjusts the width of the canvas window when the canvas is resized.
        
        :param event: The event object containing information about the canvas
        configure event.
        :type event: tkinter.Event
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        """Handles mouse wheel events for scrolling the canvas.
        
        This method adjusts the vertical view of the canvas based on the mouse wheel
        event. It supports different platforms (Windows, macOS, Linux) by using the
        appropriate event attributes.
        
        :param event: The event object containing information about the mouse wheel
        event.
        :type event: tkinter.Event
        """
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == "Darwin":
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        """Binds mouse wheel events when the cursor enters the control.
        
        This method handles the binding of mouse wheel events for different platforms
        when the cursor enters the control. On Linux, it binds the '<Button-4>' and
        '<Button-5>' events, while on other platforms, it binds the '<MouseWheel>' event.
        
        :param event: The event object containing information about the enter event.
        :type event: tkinter.Event
        """
        if platform.system() == "Linux":
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        """Unbinds mouse wheel events when the cursor leaves the control.
        
        This method handles the unbinding of mouse wheel events for different platforms
        when the cursor leaves the control. On Linux, it unbinds the '<Button-4>' and
        '<Button-5>' events, while on other platforms, it unbinds the '<MouseWheel>' event.
        
        :param event: The event object containing information about the leave event.
        :type event: tkinter.Event
        """
        if platform.system() == "Linux":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")


class MainHelpFrame(tk.Toplevel):
    """A class to create a help dialog window for providing information about the
    main functionalities of the application, organized into tabs with detailed
    help text.
    """
    def __init__(self, container):
        """Initializes the MainHelpFrame class, which creates a help dialog window for
        providing information about the main functionalities of the application.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Hauptmenü'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds three tabs labeled 'Generell', 'Analysieren', and 'Bewerten' to the
        notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Generell' tab to display general help
        information.
        - Inserts various sections of help text into the 'Generell' text widget.
        - Packs the 'Generell' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Analysieren' tab to display help information
        about the analysis functionality.
        - Inserts various sections of help text into the 'Analysieren' text widget.
        - Packs the 'Analysieren' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Bewerten' tab to display help information
        about the rating functionality.
        - Inserts various sections of help text into the 'Bewerten' text widget.
        - Packs the 'Bewerten' text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        self.title("Hilfe - Hauptmenü")
        self.geometry("500x650")

        self.notebook = ttk.Notebook(self)

        tab_general = ttk.Frame(self.notebook)
        tab_analyse = ttk.Frame(self.notebook)
        tab_rate = ttk.Frame(self.notebook)

        self.notebook.add(tab_general, text ="Generell")
        self.notebook.add(tab_analyse, text ="Analysieren")
        self.notebook.add(tab_rate, text ="Bewerten")

        self.notebook.pack(expand = True, fill ="both")

        general_txt = tk.Text(tab_general, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        general_txt.insert("end", "Das Hilfe-Symbol gibt dir auf jeder Seite Hinweise zu den Funktionalitäten der App.\n\n")
        general_txt.insert("end", ("Auf jeder Seite werden unterschiedliche Hilfsvorschläge angezeigt, je nachdem welche "
                           "Elemente gerade in der App angezeigt werden.\n\n"))
        general_txt.insert("end", ("Die Navigation erfolgt über die Tabs. Jeder Tab beinhaltet nähere Informationen zu den "
                           "wichtigsten Elementen, die dir in der App begegnen werden."))
        general_txt.pack(padx = 15, pady = 30)


        analyse_txt = tk.Text(tab_analyse, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        analyse_txt.insert("end", ("Die Analysieren-Funktion ermöglicht es dir Intra-, und\nInter-Rater-Reliability-"
                                   "Untersuchungen durchzuführen.\n\n"))
        analyse_txt.insert("end", "Folgende Metriken können verwendet werden, um die\nReliability-Untersuchungen vorzunehmen:\n\n")
        analyse_txt.insert("end", ("• Cohen's \u03BA\n"
                                   "• Conger's \u03BA"
                                   "• Fleiss' \u03BA\n"
                                   "• Krippendorff's \u03B1\n"
                                   "• Gwet's AC\n"
                                   "• ICC\n\n"))
        analyse_txt.insert("end", "Die für die Reliability-Untersuchungen benötigten Daten\nwerden im nächsten Schritt abgefragt.")
        analyse_txt.pack(padx = 15, pady = 30)

        rate_txt = tk.Text(tab_rate, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        rate_txt.insert("end", ("Die Bewerten-Funktion ermöglicht es dir einen Datensatz zu importieren der "
                                "von dir, oder einem\nanderen SW-Nutzer, bewertet werden soll.\n\n"))
        rate_txt.insert("end", "Dabei können die Daten mit beliebigen Labeln versehen werden (Kategorisierung).\n\n")
        rate_txt.insert("end", ("Alternativ ist es möglich den Daten kontinuierliche Werte zuzuordnen, wie es "
                                "beispielsweise beim Messen von\nSehstärken der Fall wäre."))
        rate_txt.pack(padx = 15, pady = 30)


class ScaleHelpFrame(tk.Toplevel):
    """A class to create a help dialog window for providing information on scales
    and weights, organized into tabs with detailed help text and interactive
    elements.
    """
    def __init__(self, container):
        """Initializes the ScaleHelpFrame class, which creates a help dialog window for
        providing information on scales and weights.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Skalen & Gewichte'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds two tabs labeled 'Skalenformate' and 'Gewichte' to the notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Skalenformate' tab to display help
        information about different scale formats.
        - Configures text tags for bold formatting within the 'Skalenformate' text
        widget.
        - Inserts various sections of help text into the 'Skalenformate' text widget.
        - Packs the 'Skalenformate' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Gewichte' tab to display help information
        about weights.
        - Configures text tags for bold formatting and hyperlink styling within the
        'Gewichte' text widget.
        - Binds a callback function to hyperlinks in the 'Gewichte' text widget.
        - Inserts various sections of help text into the 'Gewichte' text widget.
        - Packs the 'Gewichte' text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        # Maße vom neuen Fenster
        self.title("Hilfe - Skalen & Gewichte")
        self.geometry("500x650")

        self.notebook = ttk.Notebook(self)

        tab_scale = ttk.Frame(self.notebook)
        tab_weights = ttk.Frame(self.notebook)

        self.notebook.add(tab_scale, text="Skalenformate")
        self.notebook.add(tab_weights, text="Gewichte")

        self.notebook.pack(expand = True, fill ="both")

        scale_txt = tk.Text(tab_scale, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        scale_txt.tag_configure("bold", font="Arial 18 bold")
        
        scale_txt.insert("end", ("Das Skalenformat beschreibt Eigenschaften der zu betrachtenden Daten. "
                                 "Man kann zwischen den folgenden Skalenformaten\nuntescheiden:\n\n"))
        scale_txt.insert("end", "Nominalskala:\n ", "bold")
        scale_txt.insert("end", ("• Klassifikationen und Kategorisierungen\nsind möglich\n"
                          "• Objekte stehen nicht notwendigerweise\n"
                           "  in Relation zueinander\n"
                           "• z.B. {\"Rot\", \"Haus\", \"Stadt\"}\n\n"))
        scale_txt.insert("end", "Ordinalskala:\n", "bold")
        scale_txt.insert("end", ("• Es gibt zusätzlich eine Äquivalenzrelation\nx = y\n"
                          "• Und eine Ordnungsrelation x < y\n"
                           "• z.B. Schulnoten\n\n"))
        scale_txt.insert("end", "Intervallskala:\n", "bold")
        scale_txt.insert("end", ("• Abstände (Intervalle) sind definiert\n"
                                 "• z.B. (01.01.22 -> 03.01.22)\n" 
                                 "        = (01.01.23 -> 03.01.23)\n"
                                 "• Rechnen mit Intervallen ist erlaubt,\nmit Werten nicht\n\n"))
        scale_txt.insert("end", "Rationalskala:\n", "bold")
        scale_txt.insert("end", ("• Die Skala hat zusätzlich einen Nullpunkt\n"
                                 "• Es darf mit den Werten multipliziert\n"
                                 "  und dividiert werden.\n"
                                 "• Dadurch könnn Verhältnisse gebildet werden.\n"
                                 "• z.B. Programm A ist doppelt so schnell\n"
                                 "  wie Programm B."))

        scale_txt.pack(padx = 15, pady = 30)


        weights_txt = ("Warum sind Gewichte erorderlich?\n\n"
                       "Wenn man beispielsweise das ungewichtete "
                       "Cohen's \u03BA betrachtet und den Grad an "
                       "Übereinstimmung messen möchte, so würden "
                       "nur die Fälle als Übereinstimmung gewertet "
                       "werden, bei denen beide Räter die gleiche "
                       "Kategorie auswählen.\n\n\n"
                       "Gewichte ermöglich es darüber hinaus "
                       "Beziehungen zwischen den Kategorien "
                       "herzustellen.\n"
                       "So liegt es nahe, dass ein Rater der "
                       "einen Text als positiv bewertet mit "
                       "seiner Einschätzung mehr mit einem "
                       "Rater übereinstimmt, der den selben "
                       "Text als neutral bewertet, statt "
                       "mit einem Rater, der ihn als negativ "
                       "bewertet.\n\n"
                       )

        weights_txt = tk.Text(tab_weights, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        weights_txt.tag_configure("bold", font="Arial 18 bold")
        weights_txt.tag_configure("link", foreground="#217346", underline=True)     # Aussehen der Links festlegen
        weights_txt.tag_configure("0")                                              # Für jeden Link separaten Tag, damit eine individuelle URL geöffnet werden kann.
        weights_txt.tag_bind("0", "<Button-1>", lambda x: callback(urls[0]))

        weights_txt.insert("end", "Warum sind Gewichte erorderlich?\n\n", "bold")
        weights_txt.insert("end", ("Wenn man beispielsweise das ungewichtete "
                                   "Cohen's \u03BA betrachtet und den Grad an "
                                   "Übereinstimmung messen möchte, so würden "
                                   "nur die Fälle als Übereinstimmung gewertet "
                                   "werden, bei denen beide Räter die gleiche "
                                   "Kategorie auswählen.\n\n"))
        weights_txt.insert("end", ("Gewichte ermöglich es darüber hinaus "
                                   "Beziehungen zwischen den Kategorien "
                                   "herzustellen. "
                                   "So liegt es nahe, dass ein Rater der "
                                   "einen Text als positiv bewertet mit "
                                   "seiner Einschätzung mehr mit einem "
                                   "Rater übereinstimmt, der den selben "
                                   "Text als neutral bewertet, statt "
                                   "mit einem Rater, der ihn als negativ "
                                   "bewertet. "
                                   "Wie stark diese Beziehungen ausgeprägt sind, "
                                   "bzw. wie stark sie gewichtet werden sollen "
                                   "hängt von der Wahl des Gewichts ab.\n\n"))
        weights_txt.insert("end", "Wie werden die Gewichte berechnet?\n\n", "bold")

        img = tk.PhotoImage(file=os.path.join(file_path, "../data/img/weights_identity.png"))
        weights_txt.insert("end", "Ausführliche Informationen zur Berechnung der Gewichte gibt es auf ")
        weights_txt.insert("end", "dieser Website", ("link", "0"))
        weights_txt.insert("end", ".")


        weights_txt.pack(padx=15, pady=30)


class ImportHelpFrame(tk.Toplevel):
    """A class to create a help dialog window for providing information on importing
    data formats, organized into tabs with detailed help text for each format.
    """
    def __init__(self, container):
        """Initializes the ImportHelpFrame class, which creates a help dialog window for
        providing information on importing data formats.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Importieren'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds two tabs labeled 'Format 1' and 'Format 2' to the notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Format 1' tab to display help information
        about the first data format.
        - Configures text tags for bold formatting within the 'Format 1' text widget.
        - Inserts various sections of help text into the 'Format 1' text widget.
        - Packs the 'Format 1' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Format 2' tab to display help information
        about the second data format.
        - Configures text tags for bold formatting within the 'Format 2' text widget.
        - Inserts various sections of help text into the 'Format 2' text widget.
        - Packs the 'Format 2' text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        # Maße vom neuen Fenster
        self.title("Hilfe - Importieren")
        self.geometry("500x650")

        self.notebook = ttk.Notebook(self)

        tab_format1 = ttk.Frame(self.notebook)
        tab_format2 = ttk.Frame(self.notebook)

        self.notebook.add(tab_format1, text ="Format 1")
        self.notebook.add(tab_format2, text ="Format 2")

        self.notebook.pack(expand = True, fill ="both")

        format1_txt = tk.Text(tab_format1, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        format1_txt.tag_configure("bold", font="Arial 18 bold")
        format1_txt.insert("end", "Format 1\n\n", "bold")
        format1_txt.insert("end", ("Beim ersten Format sind die Rater ID's in einer eigenen Spalte organisiert.  "
                                   "Es ist verpflichtend einem Header den Namen 'Rater ID' zu geben, damit die ID's "
                                   "gefunden werden können. Auf Groß- und Kleinschreibung wird beim Header nicht geachtet. "
                                   "Es ist aber darauf zu achten, dass der Headername nicht mehrfach vorkommt. "
                                   "Es darf die gleiche Rater ID mehrfach in der Spalte vorkommen. Mehrfache Vorkommnisse "
                                   "werden intern in dieser App zusammengefasst.\n\n\n"))
        format1_txt.insert("end", "Diskretes Skalenformat\n\n", "bold")
        format1_txt.insert("end", ("Falls du ein diskretes Skalenformaten (nominal, ordinal) ausgewählt hast, "
                                   "muss die Datei zusätzlich eine Spalte mit dem Headernamen 'Categories' enthalten "
                                   "Die Spalte enthält alle Kategorienamen, die bei der Analyse, oder beim Bewerten, vorkommen"
                                   "können. Die Kategorienamen sind case sensitive.\n"
                                   "Es spielt keine Rolle wo die 'Rater ID'-, bzw. die 'Categories'-Spalten in der Datei auftauchen. "
                                   "Die Suche nach den Spalten erfolgt alleine durch den Namen.\n\n\n" 
                                   ))
        format1_txt.insert("end", "Kontinuierliche Skalenformat\n\n", "bold")
        format1_txt.insert("end", ("Bei kontinuierlichen Skalenformaten (intervall, rational) gibt es keine 'Categories'-Spalte. "
                                   "Vor der 'Rater ID'-Spalte können beliebige Spalten auftauchen, die von IIRA ignoriert werden. "
                                   "Es ist wichtig, dass nach der 'Rater ID'-Spalte ausschließlich Spalten auftauchen, die die Bewertungen "
                                   "enthalten. Bei kontinuierlichen Skalenformaten können diese Spalten nämlich nicht durch die Kategorienamen "
                                   "automatisch gesucht werden."
                                   ))
        format1_txt.pack(padx = 15, pady = 30)

        format2_txt = tk.Text(tab_format2, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        format2_txt.tag_configure("bold", font="Arial 18 bold")
        format2_txt.insert("end", "Format 2\n\n", "bold")
        format2_txt.insert("end", ("Beim zweiten Format sind die Subjects in einer eigenen Spalte organisiert.  "
                                   "Es ist verpflichtend einem Header den Namen 'Subject' zu geben, damit die Subjects "
                                   "gefunden werden können. Auf Groß- und Kleinschreibung wird beim Header nicht geachtet. "
                                   "Es ist aber darauf zu achten, dass der Headername nicht mehrfach vorkommt. "
                                   "Es darf das gleiche Subject mehrfach in der Spalte vorkommen. Mehrfache Vorkommnisse "
                                   "werden intern in dieser App zusammengefasst.\n\n\n"))
        format2_txt.insert("end", "Diskretes Skalenformat\n\n", "bold")
        format2_txt.insert("end", ("Falls du ein diskretes Skalenformaten (nominal, ordinal) ausgewählt hast, "
                                   "muss die Datei zusätzlich eine Spalte mit dem Headernamen 'Categories' enthalten "
                                   "Die Spalte enthält alle Kategorienamen, die bei der Analyse, oder beim Bewerten, vorkommen"
                                   "können. Die Kategorienamen sind case sensitive.\n"
                                   "Es spielt keine Rolle wo die 'Subject'-, bzw. die 'Categories'-Spalten in der Datei auftauchen. "
                                   "Die Suche nach den Spalten erfolgt alleine durch den Namen.\n\n\n" 
                                   ))
        format2_txt.insert("end", "Kontinuierliche Skalenformat\n\n", "bold")
        format2_txt.insert("end", ("Bei kontinuierlichen Skalenformaten (intervall, rational) gibt es keine 'Categories'-Spalte. "
                                   "Vor der 'Subject'-Spalte können beliebige Spalten auftauchen, die von IIRA ignoriert werden. "
                                   "Es ist wichtig, dass nach der 'Subject'-Spalte ausschließlich Spalten auftauchen, die die Bewertungen "
                                   "enthalten. Bei kontinuierlichen Skalenformaten können diese Spalten nämlich nicht durch die Kategorienamen "
                                   "automatisch gesucht werden."))
        format2_txt.pack(padx = 15, pady = 30)

class PrepAnalyseHelpFrame(tk.Toplevel):

    """A class to create a help dialog window for providing information on preparing
    an analysis, including selecting raters and metrics. The window is organized
    into tabs with detailed help text and hyperlinks for further information.
    """
    def __init__(self, container):
        """Initializes the PrepAnalyseHelpFrame class, which creates a help dialog window
        for providing information on preparing an analysis.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Analyse vorbereiten'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds two tabs labeled 'Bewerter' and 'Metriken' to the notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Bewerter' tab to display help information
        about selecting raters.
        - Configures text tags for bold formatting within the 'Bewerter' text widget.
        - Inserts various sections of help text into the 'Bewerter' text widget.
        - Packs the 'Bewerter' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Metriken' tab to display help information
        about selecting metrics.
        - Configures text tags for bold formatting and hyperlink styling within the
        'Metriken' text widget.
        - Binds callback functions to hyperlinks in the 'Metriken' text widget.
        - Inserts various sections of help text into the 'Metriken' text widget.
        - Packs the 'Metriken' text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        # Maße vom neuen Fenster
        self.title("Hilfe - Analyse vorbereiten")
        self.geometry("500x650")

        # Notebooks kann mit Textinhalt gefüllt werden und Inhalt
        # wird über verschiedene Tabs organisiert.
        self.notebook = ttk.Notebook(self)

        #TODO Namen anpassen
        tab_rater = ttk.Frame(self.notebook)
        tab_metrics = ttk.Frame(self.notebook)

        self.notebook.add(tab_rater, text ="Bewerter")
        self.notebook.add(tab_metrics, text ="Metriken")

        self.notebook.pack(expand = True, fill ="both")

        rater_txt = tk.Text(tab_rater, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        rater_txt.tag_configure("bold", font="Arial 18 bold")
        rater_txt.insert("end", "Auswahl der Bewerter\n\n\n", "bold")
        rater_txt.insert("end", ("Durch die Auswahl der Bewerter wird festgelegt, von welchen Bewertern die "
                                 "Reliabilitätsuntersuchungen vorgenommen werden sollen.\n\n"
                                 "Für jeden ausgewählten Intrarater wird eine eigene Intrarater-Reliabilitätsuntersuchung "
                                 "für den Bewerter vorgenommen.\n\n"
                                 "Bei der Auswahl mehrerer Interrater, wird eine Interrater-Reliabilitätsuntersuchung "
                                 "für alle ausgewählten Bewerter erstellt."))
        rater_txt.pack(padx = 15, pady = 30)

        metrics_txt = tk.Text(tab_metrics, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        metrics_txt.tag_configure("bold", font="Arial 18 bold")
        metrics_txt.tag_configure("link", foreground="#217346", underline=True)     # Aussehen der Links festlegen
        metrics_txt.tag_configure("1")                                              # Für jeden Link separaten Tag, damit eine individuelle URL geöffnet werden kann.
        metrics_txt.tag_bind("1", "<Button-1>", lambda x: callback(urls[1]))
        metrics_txt.tag_bind("2", "<Button-1>", lambda x: callback(urls[2]))
        metrics_txt.tag_bind("3", "<Button-1>", lambda x: callback(urls[3]))
        metrics_txt.tag_bind("4", "<Button-1>", lambda x: callback(urls[4]))
        metrics_txt.tag_bind("5", "<Button-1>", lambda x: callback(urls[5]))
        metrics_txt.tag_bind("6", "<Button-1>", lambda x: callback(urls[6]))

        metrics_txt.insert("end", "Auswahl der Metriken\n\n", "bold")
        metrics_txt.insert("end", ("Durch die Auswahl der Metriken kann festgelegt werden, welche Metrikwerte für die  "
                                 "Reliabilitätsuntersuchungen berechnet werden sollen.\n\n"
                                 "Weiterführende Informationen zu den Metriken, findest du unter den folgenden Links:\n\n"))
        
        metrics_txt.insert("end", "Cohen's \u03BA\n", "bold")
        metrics_txt.insert("end", "COHEN, Jacob. A coefficient of agreement for nominal scales. Educational and psychological measurement, 1960, 20. Jg., Nr. 1, S. 37-46.\n\n", ("link", "1"))

        metrics_txt.insert("end", "Conger's \u03BA\n", "bold")
        metrics_txt.insert("end", "Anthony J Conger. Integration and generalization of kappas for multiple raters. Psychological Bulletin, 88(2):322, 1980.\n\n", ("link", "2"))

        metrics_txt.insert("end", "Fleiss' \u03BA\n", "bold")
        metrics_txt.insert("end", "Joseph L Fleiss. Measuring nominal scale agreement among many raters. Psychological bulletin, 76(5):378, 1971.\n\n", ("link", "3"))

        metrics_txt.insert("end", "Krippendorff's \u03B1\n", "bold")
        metrics_txt.insert("end", "K. Krippendorff. Content Analysis: An Introduction To Its Methodology. Sage, Beverly Hills, CA, 1980.\n\n", ("link", "4"))

        metrics_txt.insert("end", "Gwet's AC\n", "bold")
        metrics_txt.insert("end", "GWET, Kilem Li. Computing inter‐rater reliability and its variance in the presence of high agreement. British Journal of Mathematical and Statistical Psychology, 2008, 61. Jg., Nr. 1, S. 29-48.\n\n", ("link", "5"))

        metrics_txt.insert("end", "ICC\n", "bold")
        metrics_txt.insert("end", "GWET, Kilem L. Intrarater reliability. Wiley encyclopedia of clinical trials, 2008, 4. Jg.\n\n", ("link", "6"))

        metrics_txt.pack(padx = 15, pady = 30)

class ResultsHelpFrame(tk.Toplevel):
    """
    Die Klasse stellt dem SW-User ein Hilsdialog zur Verfügung, in Abhängigkeit
    von dem Frame in dem sich der SW-User aktuell befindet.
    TODO
    """
    def __init__(self, container):
        """Initializes the ResultsHelpFrame class, which creates a help dialog window for
        providing information about the results of reliability analyses.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Ergebnisse'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds two tabs labeled 'Generell' and 'Interpretation' to the notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Generell' tab to display general help
        information about the results.
        - Configures text tags for bold formatting within the 'Generell' text widget.
        - Inserts various sections of help text into the 'Generell' text widget.
        - Packs the 'Generell' text widget with padding for better layout.
        - Creates a tk.Text widget in the 'Interpretation' tab to display information
        on how to interpret the results.
        - Configures text tags for bold formatting within the 'Interpretation' text
        widget.
        - Inserts various sections of help text into the 'Interpretation' text widget.
        - Packs the 'Interpretation' text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        # Maße vom neuen Fenster
        self.title("Hilfe - Ergebnisse")
        self.geometry("500x650")

        # Notebooks kann mit Textinhalt gefüllt werden und Inhalt
        # wird über verschiedene Tabs organisiert.
        self.notebook = ttk.Notebook(self)

        #TODO Namen anpassen
        tab_general = ttk.Frame(self.notebook)
        tab_interpratation = ttk.Frame(self.notebook)

        self.notebook.add(tab_general, text ="Generell")
        self.notebook.add(tab_interpratation, text ="Interpretation")

        self.notebook.pack(expand = True, fill ="both")

        general_txt = tk.Text(tab_general, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        general_txt.tag_configure("bold", font="Arial 18 bold")
        general_txt.insert("end", "Informationen zu den Ergebnissen\n\n", "bold")
        general_txt.insert("end", ("Die Ergebnisse der Reliabilitätsuntersuchungen werden in zwei Tabs "
                                   "dargestellt. In einem Tab werden die Ergebnisse der Intrarater-Analyse "
                                   "dargestellt und im anderen Tab die Ergebnisse der Interrater-Analyse.\n"
                                   "Vorausgesetzt, du hast im vorherigen Fenster die Auswahl getroffen, die entsprechenden "
                                   "Analysen vorzunehmen.\n\n"))
        
        general_txt.insert("end", "ID\n", "bold")
        general_txt.insert("end", "Die Spalte gibt an auf welche Bewerter-ID sich die Analyse bezieht.\n\n")

        general_txt.insert("end", "Metrikwerte\n", "bold")
        general_txt.insert("end", "In den mittleren Spalten werden die Ergebnisse der Reliabilitätsuntersuchungen für jede ausgewählte Metrik angezeigt.\n\n")

        general_txt.insert("end", "#Subjects\n", "bold")
        general_txt.insert("end", ("Die Spalte gibt an, wie viele Subjects, oder Bewertungsobjekte, "
                                   "es in der Reliabilitätsuntersuchung gibt."
                                   "Falls ein Bewerter 10 unterschiedliche Subjects an zwei unterschiedlichen Beobachtungszeitpunkten " 
                                   "bewertet hat, würde in der Spalte also eine 10 stehen.\n\n"))

        general_txt.insert("end", "#Replicates\n", "bold")
        general_txt.insert("end", ("Die Spalte gibt an, wie viele Replikate es gibt. "
                                   "Beim oberen Beispiel, in dem ein Bewerter 10 Subjects an zwei unterschiedlichen Beobachtungszeitpunkten "
                                   "bewertet hat, würde in der Spalte also eine 2 stehen.\n\n"))
        
        general_txt.insert("end", "#Rater\n", "bold")
        general_txt.insert("end", ("Bei der Interrater-Analyse wird zusätzlich in einer Spalte angegeben, wie viele Bewerter "
                                   "in der Analyse betrachtet worden sind."))
        
        general_txt.pack(padx = 15, pady = 30)


        interpretation_txt = tk.Text(tab_interpratation, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        interpretation_txt.tag_configure("bold", font="Arial 18 bold")
        interpretation_txt.insert("end", "Wie werden die Werte interpretiert?\n\n", "bold")
        interpretation_txt.insert("end", ("In der folgenden Tabelle wurde die gängige Interpretation der Ergebnisse der "
                                          "Intra- und Interrater-Analysen dargestellt. Die Interpretationsmöglichkeit gilt "
                                          "für alle auswählbaren Metriken.\n\n"))

        interpretation_txt.insert("end", "Interpretation nach Landis & Koch:\n\n", "bold")
        interpretation_txt.insert("end", "Metrikwert | Grad der Übereinstimmung\n", "bold")
        interpretation_txt.insert("end", "<0.00         | Poor\n")
        interpretation_txt.insert("end", "0.00 - 0.20 | Slight\n")
        interpretation_txt.insert("end", "0.21 - 0.40 | Fair\n")
        interpretation_txt.insert("end", "0.41 - 0.60 | Moderate\n")
        interpretation_txt.insert("end", "0.61 - 0.80 | Substantial\n")
        interpretation_txt.insert("end", "0.81 - 1.00 | Almost Perfect\n")

        
        interpretation_txt.pack(padx = 15, pady = 30)

class RateHelpFrame(tk.Toplevel):
    """
    Die Klasse stellt dem SW-User ein Hilsdialog zur Verfügung, in Abhängigkeit
    von dem Frame in dem sich der SW-User aktuell befindet.
    TODO
    """
    def __init__(self, container):
        """Initializes the RateHelpFrame class, which creates a help dialog window for
        providing information about the rating functionality in the application.
        
        :param container: The parent container for this Toplevel window.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following actions:
        - Calls the constructor of the parent class (tk.Toplevel).
        - Sets the container attribute to the provided container.
        - Sets the title of the window to 'Hilfe - Bewerten'.
        - Sets the geometry of the window to 500x650 pixels.
        - Creates a ttk.Notebook widget for organizing content in tabs.
        - Adds a single tab labeled 'Generell' to the notebook.
        - Packs the notebook to expand and fill the window.
        - Creates a tk.Text widget in the 'Generell' tab to display help information.
        - Configures text tags for bold formatting within the text widget.
        - Inserts various sections of help text into the text widget.
        - Packs the text widget with padding for better layout.
        """
        super().__init__(container)
        self.container = container

        # Maße vom neuen Fenster
        self.title("Hilfe - Bewerten")
        self.geometry("500x650")

        # Notebooks kann mit Textinhalt gefüllt werden und Inhalt
        # wird über verschiedene Tabs organisiert.
        self.notebook = ttk.Notebook(self)

        #TODO Namen anpassen
        tab_general = ttk.Frame(self.notebook)

        self.notebook.add(tab_general, text ="Generell")

        self.notebook.pack(expand = True, fill ="both")

        general_txt = tk.Text(tab_general, foreground="black", background="white", relief="flat",
                      font="Arial 18", highlightthickness = 0, borderwidth=0)
        general_txt.tag_configure("bold", font="Arial 18 bold")
        general_txt.insert("end", "Informationen zum Bewerten\n\n", "bold")
        general_txt.insert("end", ("In dieser Ansicht können die zuvor importierten Daten bewertet werden.\n\n"
                                   "Es ist möglich über den Profil-Button das aktuelle Nutzerprofil zu wechseln. "
                                   "Die Bewertungen werden immer dem Profil zugeordnet, das gerade angemeldet ist. "
                                   "So ist es möglich während einer Bewertungssession mit unterschiedlichen Profilen Bewertungen vorzunehmen.\n\n"))
        
        general_txt.insert("end", "Navigation\n", "bold")
        general_txt.insert("end", "Das Navigations-Widget links ermöglicht es schnell zwischen den Fragen hin und her zu springen. "
                                  "Außerdem bietet es, neben der Statusbar oben, eine Übersicht darüber, wie viele Elemente bereits bewertet worden sind.\n"
                                  "Zusätzlich sind die linke, bzw. die rechte, Pfeiltaste mit Hotkeys belegt, um zum vorherigen, bzw. zum nächsten, Element zu wechseln.\n\n")

        general_txt.insert("end", "Bewerten\n", "bold")
        general_txt.insert("end", ("Um eine Bewertung vorzunehmen, kannst du die Radiobuttons ganz links drücken."
                                   "Die ersten 9 Kategorien sind zusätzlich mit den Hotkeys 1-9 belegt.\n"
                                   "Bei kontinuierlichen Daten kann das Eingabefeld ganz links zum Bewerten genutzt werden.\n\n"))

        general_txt.insert("end", "Speichern & Verwerfen\n", "bold")
        general_txt.insert("end", "Zum Speichern, oder zum Verwerfen der aktuellen Bewertungssession sind die jeweiligen Buttons oben rechts zu drücken.\n\n")

        
        general_txt.pack(padx = 15, pady = 30)

def callback(url):
    """ Die Funktion erhält ein String-Argument, welches im Webbrowser geöffnet wird. """
    webbrowser.open_new(url)
























