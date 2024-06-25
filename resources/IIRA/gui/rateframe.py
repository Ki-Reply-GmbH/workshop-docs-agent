import math
import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import numpy as np

from gui.containerframe import ContainerFrame
from gui.helperframes import RateHelpFrame

PROFILE = 0
RATING = 1

class RateFrame(ContainerFrame):

    """A class to represent the RateFrame, which handles the user interface for
    rating text elements. It includes methods for populating navigation,
    randomizing text order, handling events, and updating the UI based on
    user interactions. The class also manages saving and deleting rating
    sessions, and updating the percentage of completed ratings.
    """
    def __init__(self, container):
        """Initializes the RateFrame class, setting up the user interface and configuring
        various widgets and styles.
        
        :param container: The container widget that holds this frame.
        :type container: tkinter.Widget
        :returns: None
        :raises None: This method does not raise any exceptions.
        
        The constructor performs the following steps:
        
        1. Initializes instance variables such as `text`, `text_index`, `profile`,
        `ratings`, `total_ratings`, `shuffler`, and `undo_shuffler`.
        2. Calls the superclass constructor with the container parameter.
        3. Configures various styles for Treeview, Radiobutton, and Label widgets.
        4. Binds the right and left arrow keys to `next_cmd` and `prev_cmd` methods.
        5. Creates and configures frames for layout: `left_frame`, `mid_frame`,
        `right_frame`, and `top_frame`.
        6. Sets row and column configurations for the grid layout.
        7. Adds separators and frames to the menu bar for layout and functionality.
        8. Creates and configures save and delete frames with associated labels and
        binds events for mouse enter, leave, and click actions.
        9. Sets up the text preview Treeview widget with columns, headings, and binds
        events for double-click and arrow keys.
        10. Creates and configures the percentage label.
        11. Sets up the text label and navigation buttons in the middle frame.
        12. Configures the right frame with separators and a container for radio
        buttons.
        13. Calls `populate_categories` to initialize category selection widgets.
        """
        self.text = []
        self.text_index = 0
        self.profile = container.dbinteraction.active_profile

        self.ratings = []
        self.total_ratings = 0  

        self.shuffler = None
        self.undo_shuffler = None

        super().__init__(container)
        container.style.configure("RateFrame.Treeview", font="Arial 16 bold", rowheight=30)
        container.style.configure("RateFrame.Treeview.Heading", font="Arial 18")
        container.style.configure("RateFrame.TRadiobutton", font="Arial 16")
        container.style.configure("Red.TLabel", foreground="#CC0000")
        container.style.configure("Orange.TLabel", foreground="#FF8000")
        container.style.configure("Yellow.TLabel", foreground="#CCCC00")
        container.style.configure("Lightgreen.TLabel", foreground="#00FF00")
        container.style.configure("Green.TLabel", foreground=self.accent_color)
        
        self.bind("<Right>", self.next_cmd)
        self.bind("<Left>", self.prev_cmd)
        left_frame = ttk.Frame(self)
        mid_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)
        top_frame = ttk.Frame(self)

        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

        separator_frame = ttk.Frame(self.menu_bar)
        separator_frame.grid(row=0, column=5, sticky="nsew")

        vert_separator = ttk.Separator(self.menu_bar, orient="vertical")
        vert_separator.grid(row=0, column=6, sticky="nsew")

        save_frame = ttk.Frame(self.menu_bar, width=75, height=50)
        save_label = ttk.Label(save_frame, text="Speichern", image=self.container.save_icon, compound="top", font="Arial 12")
        save_frame.bind("<Enter>", lambda x: self.on_enter(save_frame, save_label))
        save_frame.bind("<Leave>", lambda x: self.on_leave(save_frame, save_label))
        save_frame.bind("<Button-1>", lambda x: self.save_cmd())
        save_label.bind("<Button-1>", lambda x: self.save_cmd())

        save_frame.grid(row=0, column=7, sticky="nsew")
        save_label.place(relx=0.5, rely=0.5, anchor="center")

        delete_frame = ttk.Frame(self.menu_bar, width=85, height=50)
        delete_label = ttk.Label(delete_frame, text="Verwerfen", image=self.container.delete_icon, compound="top", font="Arial 12")
        delete_frame.bind("<Enter>", lambda x: self.on_enter(delete_frame, delete_label))
        delete_frame.bind("<Leave>", lambda x: self.on_leave(delete_frame, delete_label))
        delete_frame.bind("<Button-1>", lambda x: self.delete_cmd())
        delete_label.bind("<Button-1>", lambda x: self.delete_cmd())

        delete_frame.grid(row=0, column=8, sticky="nsew")
        delete_label.place(relx=0.5, rely=0.5, anchor="center")

        horizon_separator = ttk.Separator(self.menu_bar, orient="horizontal")
        horizon_separator.grid(row=1, column=6, columnspan=3, sticky="nsew")

        self.menu_bar.grid(row=0, column=0, columnspan=3,sticky="nsew")
        self.menu_bar.columnconfigure(5, weight=1)


        left_frame.grid(row = 3, column=0, sticky="nsew")
        left_frame.rowconfigure(0, weight=1)
        
        columns = ("text")

        self.text_preview = ttk.Treeview(left_frame, columns=columns, show="headings", style="RateFrame.Treeview",
                                        selectmode="browse")
        self.text_preview.heading("text", text="Navigation")
        self.text_preview.pack(fill="both", expand=True, pady=25, padx=5)
        self.text_preview.tag_configure("unselected", font="Arial 14")
        self.text_preview.bind("<Double-Button-1>", self.doubleclick_treeview)
        self.text_preview.bind("<Right>", self.next_cmd)
        self.text_preview.bind("<Left>", self.prev_cmd)

        self.percent_label = ttk.Label(top_frame, text="0 %", font="Arial 20", style="Red.TLabel")
        self.percent_label.pack()

        top_frame.grid(row=2, column=1, sticky="nsew")

        self.text_label = ttk.Label(mid_frame, text="", font="Arial 20")

        mid_btn_container = ttk.Frame(mid_frame)
        prev_btn = ttk.Button(mid_btn_container, text="\u276E", command=self.prev_cmd)
        next_btn = ttk.Button(mid_btn_container, text="\u276F", command=self.next_cmd)
        prev_btn.pack(side="left", padx=5)
        next_btn.pack(side="right", padx=5)

        mid_frame.grid(row=3, column=1 ,sticky="nsew")
        self.text_label.grid(row=0, column=0)
        mid_btn_container.grid(row=1, column=0, pady=20)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.columnconfigure(0, weight=1)

        right_seperator0 = ttk.Frame(right_frame)
        right_seperator1 = ttk.Frame(right_frame)

        self.categories_var = tk.StringVar()
        right_frame.grid(row=3, column=2, sticky="nsew", padx=(5, 15), pady=10)
        self.rbtn_container = ttk.Frame(right_frame)

        right_seperator0.grid(row=1, column=0)
        self.rbtn_container.grid(row=2, column=0)
        right_seperator1.grid(row=3, column=0)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(3, weight=1)

        self.populate_categories()

        

    def populate_navigation(self):

        """Populates the navigation tree view with text elements.
        
        This method divides the text elements into groups of ten and creates parent
        nodes for each group in the tree view. Each parent node contains child nodes
        representing individual text elements. The method also sets the initial focus
        and selection to the first child node.
        
        :returns: None
        """
        upper_limit = math.ceil(len(self.text) / 10)
        for i in range(upper_limit): #aufrunden, damit es genügend parent nodes gibt
            # values arguments als tuple, um treeview internes nlp zu vermeiden
            if i == upper_limit - 1:
                # Beim letzten Schleifendurchlauf im Parent-Node die maximale Anzahl an Text
                # exakt ausgeben als obere Grenze
                self.text_preview.insert("", "end", iid=("parent_" + str(i)), open=False, 
                                        values=(("Elemente " + str(i * 10 + 1) + " - " + str(len(self.text))),))
            else:
                self.text_preview.insert("", "end", iid=("parent_" + str(i)), open=False, 
                                        values=(("Elemente " + str(i * 10 + 1) + " - " + str(i * 10 + 10)),))

            # Populate the children:
            for j in range(10):
                k = j + 10 * i # Offset k; 0 <= k < len(self.text)
                if k >= len(self.text):
                    break
                n = self.count_upper_case(self.text[k], 18)
                nav_text = self.text[k]

                if len(self.text[k]) > n:
                    nav_text = self.text[k][:n] + "..."
                self.text_preview.insert(("parent_" + str(i)), "end", iid=("child_" + str(k)), open=False,
                                        values=(nav_text,), tags=("unselected"))
        
        self.text_preview.item("parent_0", open=True)
        self.text_preview.focus("child_0")
        self.text_preview.selection_set("child_0")

    def randomize(self, mode):
        """Randomizes or restores the order of text and ratings based on the mode.
        
        :param mode: The mode of operation. 'do' shuffles the text and ratings,
        'undo' restores the original order.
        :type mode: str
        :raises ValueError: If the mode is not 'do' or 'undo'.
        """
        if mode == "do":
            self.shuffler = np.random.permutation(len(self.text))
            self.undo_shuffler = np.argsort(self.shuffler)

            self.text = [self.text[j] for j in self.shuffler]
            self.ratings = [self.ratings[j] for j in self.shuffler]
        if mode == "undo":
            self.text = [self.text[j] for j in self.undo_shuffler]
            self.ratings = [self.ratings[j] for j in self.undo_shuffler]


    def doubleclick_treeview(self, event):
        """Handles the double-click event on the tree view.
        
        This method identifies the row that was double-clicked, updates the text index,
        and populates the text based on the selected item. If a rating exists for the
        selected text, it sets the category variable accordingly. Otherwise, it clears
        the category variable.
        
        :param event: The event object containing information about the double-click.
        :type event: tkinter.Event
        """
        item_iid = self.text_preview.identify_row(event.y)

        if "child_" in item_iid:
            self.text_index = int(item_iid.replace("child_", ""))       # Zum ausgewählten Element springen
            self.populate_text()


            if self.ratings[self.text_index] != (): 
                self.categories_var.set(self.ratings[self.text_index][RATING])
            else:
                self.categories_var.set("")
        
        self.focus_set()


    def delete_questions(self):
        """Clears all questions from the text preview tree view.
        
        This method iterates through all items in the `text_preview` tree view
        widget and deletes each one, effectively clearing the tree view.
        
        :returns: None
        """
        for item in self.text_preview.get_children():
            self.text_preview.delete(item)

    def populate_categories(self):
        """Populates the category selection widgets based on the scale format.
        
        If the scale format is 'intervall' or 'ratio', it creates an entry widget
        for numerical input. Otherwise, it creates radio buttons for each category.
        
        :returns: None
        """
        if self.container.scale_format == "intervall" or self.container.scale_format == "ratio":
            info_label = ttk.Label(self.rbtn_container, text="Eingegeben:", font="Arial 16")
            self.var_entered = ttk.Label(self.rbtn_container, text="n.a.", font="Arial 16")
            self.var_input = ttk.Entry(self.rbtn_container, textvariable=self.categories_var, text="Zahlenwert eingeben",
                                  font="Arial 16")
            self.var_input.bind("<Return>", self.entry_input_cmd)

            info_label.pack(pady=5)
            self.var_entered.pack(pady=5)
            self.var_input.pack(pady=15)
        else:
            categories_rbtns = []
            for i in range(len(self.container.categories)):
                categories_rbtns.append(
                    ttk.Radiobutton(self.rbtn_container, text=self.container.categories[i],
                    variable=self.categories_var, value=self.container.categories[i],
                    style="RateFrame.TRadiobutton", command=self.label_text)
                    )
                categories_rbtns[i].pack(side="top", anchor="nw", pady=5)
                if i < 9:
                    if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                        self.bind_all(str(i + 1), self.cat_hotkey_cmd)

    def delete_categories(self):
        """Deletes all category-related widgets from the `rbtn_container` frame.
        
        This method retrieves all child widgets of the `rbtn_container` frame and
        destroys them, effectively clearing any displayed categories.
        
        :returns: None
        """
        children_widgets = self.rbtn_container.winfo_children()
        for widget in children_widgets:
            widget.destroy()

    def populate_text(self):
        """Updates the text label with the current text element.
        
        This method configures the `text_label` widget to display the current text
        element, formatted with newlines for readability.
        
        :returns: None
        """
        self.text_label.config(text=self.add_newlines(self.text[self.text_index], 75))

    def add_newlines(self, text, n):
        """Adds newlines to the given text at appropriate positions based on the specified
        length `n`. If a word exceeds the length `n`, it is split with a newline. The
        method ensures that no line exceeds the length `n`.
        
        :param text: The text to be formatted with newlines.
        :type text: str
        :param n: The maximum length of each line.
        :type n: int
        :returns: The formatted text with newlines.
        :rtype: str
        """
        n = self.count_upper_case(text, n)

        if len(text) < n:
            return text

        form_text = ""
        for word in text.split(" "):
            if len(word) > n:
                word = word[:n] + "\n" + word[n:]
            form_text += word + " "

        offset = 0
        try:
            while True:
                p = form_text.rindex(" ", offset, offset + n)
                form_text = form_text[:p] + "\n" + form_text[p + 1:]
                offset = p
                if len(form_text[p + 1:]) < n:
                    return form_text
        except ValueError:
            pass
        return form_text
    
    def count_upper_case(self, text, n):
        """Counts the number of uppercase characters in the given text and adjusts the
        value of `n` if the count is at least half the length of the text.
        
        :param text: The text to be analyzed.
        :type text: str
        :param n: The initial value to be potentially adjusted.
        :type n: int
        :returns: The adjusted value of `n`.
        :rtype: int
        """
        count_upper_case = 0 
        for char in text:
            if char.isupper():
                count_upper_case += 1
        if count_upper_case >= len(text) // 2:
            n = int(n * 0.75)
        
        return n

    def entry_input_cmd(self, event=None):
        """Handles the input command for the entry widget.
        
        This method processes the input from the entry widget. If the input is not
        empty, it sets the `categories_var` to the input value, updates the label
        text, moves to the next item, and clears the entry widget.
        
        :param event: Optional event that triggered the method, defaults to None.
        :type event: tkinter.Event, optional
        :returns: None
        """
        if len(self.var_input.get()) == 0:
            # Falls User nichts eingegeben hat, tue nichts.
            return
        
        # Setzt die Variable categories_var auf den Wert, der im Entry-Feld eingegeben wurde.
        self.categories_var.set(self.var_input.get())

        # Bewertung in die Datenstruktur hinzufügen, in der alle bewertungen pro User gespeichert werden
        # und in Navigation-Treeview die Aktualisierung anzeigen
        self.label_text()
        
        # Zum nächsten Bewertungsobjekt wechseln
        self.next_cmd()

        # Die Eingabe im Entry-Feld zurücksetzen, nachdem die Bewertung gespeichert wurde
        self.var_input.delete(0, "end")

    def cat_hotkey_cmd(self, event):
        """Handles the hotkey command for category selection.
        
        This method adjusts the category based on the hotkey pressed by the user.
        It updates the `categories_var` with the selected category and calls the
        `label_text` method to reflect the changes in the UI and data structure.
        
        :param event: The event that triggered the method, containing the hotkey.
        :type event: tkinter.Event
        :returns: None
        """
        category_no = int(event.char) - 1

        # Wert der Variablen anpassen
        self.categories_var.set(self.container.categories[category_no])

        # Das Rating in der Datenstruktur setzen und den Navigationsframe auf der linken Seite anpassen.
        self.label_text()

    def next_cmd(self, event=None):

        """Advances to the next text element and updates the UI accordingly.
        
        This method handles the action for navigating to the next text element.
        It updates the current text index, populates the text and rating fields,
        and adjusts the navigation tree view to reflect the current state. If the
        text index is already at the end, the method returns without making any
        changes.
        
        :param event: Optional; the event that triggered the method, defaults to None.
        :type event: tkinter.Event, optional
        :returns: None
        """
        self.focus_set() # Für Zugriff auf Key-Bindings von left- und right-arrow
        if self.text_index == len(self.text) - 1:
            # User ist am Ende der Fragen angekommen.
            return 
        else:
            self.text_index = self.text_index + 1
            self.populate_text()
            if self.ratings[self.text_index] != (): 
                self.categories_var.set(self.ratings[self.text_index][RATING])

                if self.container.scale_format == "intervall" or self.container.scale_format == "ratio":

                    self.var_entered.config(text=self.categories_var.get())
            else:
                # Vorherige Auswahl vom anderen Textelement im Radiobutton in GUI resetten
                self.categories_var.set("")

                if self.container.scale_format == "intervall" or self.container.scale_format == "ratio":
                    # Bei Intervall- oder Rationaldaten zusätzlich n.a. im Label anzeigen
                    self.var_entered.config(text="n.a.")

            # Navigation-Treeview anpassen
            # Passendes-Parent-Item öffnen / schließen
            parent_iid = "parent_" + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            # Alle anderen Parent-Items schließen
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = "parent_" + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)

            # Child-Item hervorheben
            child_iid = "child_" + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)

            #TODO write to tmp-file for autosave

    def prev_cmd(self, event=None):

        """Handles the action for navigating to the previous text element.
        
        This method updates the current text index, populates the text and rating
        fields, and adjusts the navigation tree view to reflect the current state.
        If the text index is already at the beginning, the method returns without
        making any changes.
        
        :param event: Optional; the event that triggered the method, defaults to None.
        :type event: tkinter.Event, optional
        :returns: None
        """
        self.focus_set() # Für Zugriff auf Key-Bindings von left- und right-arrow
        if self.text_index == 0:
            return 
        else:
            self.text_index = self.text_index - 1
            self.populate_text()
            if self.ratings[self.text_index] != (): 
                # Es wurde bereits ein Rating für die vorherige Frage gesetzt.
                # Das soll in den Radiobuttons angezeigt werden.
                self.categories_var.set(self.ratings[self.text_index][RATING])

                if self.container.scale_format == "intervall" or self.container.scale_format == "ratio":
                    # Bei Intervall- oder Rationaldaten zusätzlich im Label anzeigen welcher Wert bereits
                    # gesetzt wurde
                    self.var_entered.config(text=self.categories_var.get())
            else:
                self.categories_var.set("") # Radiobutton resetten

                if self.container.scale_format == "intervall" or self.container.scale_format == "ratio":
                    self.var_entered.config(text="n.a.")
            
            parent_iid = "parent_" + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = "parent_" + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)

            child_iid = "child_" + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)


    def save_cmd(self):
        """Saves the current ratings to a file.
        
        This method first checks if the text has been shuffled and, if so,
        restores the original order. It then sets the focus to the current
        widget and opens a file dialog to prompt the user to specify a
        filename and file type for saving. The ratings are then written
        to the specified file.
        
        :returns: None
        """
        if self.shuffler is not None:
            self.randomize("undo")

        self.focus_set()
        filename = tk.filedialog.asksaveasfilename(filetypes=[
            ("Excel files", ".xlsx .xls"), 
            ("Libreoffice Calc files", ".ods"),
            ("Csv files", ".csv")
            ])
        
        self.container.filevalidation.write_file(filename, self.ratings)

    def delete_cmd(self):
        """Handles the deletion of the current rating session.
        
        This method sets the focus, prompts the user with a message box to confirm
        the deletion of the entire rating session. If the user confirms, it resets
        the categories, clears the ratings list, and updates the frame.
        
        :returns: None
        """
        self.focus_set()
        result = messagebox.askyesno(title="Verwerfen", message="Die gesamte Bewertungssession verwerfen?")
        if result:
            self.categories_var.set("")
            self.ratings = []
            for text_entry in self.text:
                self.ratings.append(())

                self.text_index = 0
                self.update_frame()
        else:
            return

    def label_text(self, event=None):
        """Updates the rating for the current text element based on the selected category.
        
        If the selected category matches the existing rating, it removes the rating.
        Otherwise, it updates or sets the rating. It also updates the navigation tree
        to reflect the changes and checks if all text elements have been rated.
        
        :param event: Optional event that triggered the method, defaults to None.
        :type event: tkinter.Event, optional
        :returns: None
        """
        self.focus_set()

        if self.ratings[self.text_index]:
            if self.ratings[self.text_index][RATING] == self.categories_var.get():
                self.ratings[self.text_index] = ()
                self.categories_var.set("")
                self.total_ratings -= 1
                self.populate_percentage()

                child_iid = "child_" + str(self.text_index)
                self.text_preview.item(child_iid, tags=(self.text_preview.item(child_iid, "tags")[0]))
                self.text_preview.item(child_iid, values=(self.text_preview.item(child_iid, "values")[0].replace(" ✓", ""),))
                parent_iid = self.text_preview.parent(child_iid)
                values = self.text_preview.item(parent_iid, "values")
                values = (values[0].replace("     ✓", ""),)
                self.text_preview.item(parent_iid, values=values)
            else:
                # Wurde bereits gelabeld; nur der Wert wird geändert
                self.ratings[self.text_index] = (self.container.dbinteraction.active_profile, self.categories_var.get())
        else:
            # Kategorieauswahl, sowie Profil in der Ratings-Liste speichern.
            self.ratings[self.text_index] = (self.container.dbinteraction.active_profile, self.categories_var.get())
            #TODO checken, ob neue Auswahl gemacht wurde
            self.total_ratings += 1
            #TODO Falls was abgewählt wird total_ratings dekrementieren

            self.populate_percentage()

            # Häckchen im Navigation-Treeview hinzufügen
            child_iid = "child_" + str(self.text_index)

            # Gibt die Tags, bzw values vom Child-Element
            tags = self.text_preview.item(child_iid, "tags")
            values = self.text_preview.item(child_iid, "values")

            if "labeled" not in tags:
                tags += ("labeled",)
                values = (values[0] + " ✓",)

            self.text_preview.item(child_iid, tags=tags)
            self.text_preview.item(child_iid, values=values)

            self.text_preview.selection_set(child_iid)

            # Falls alle Child-Elemente gelabeled wurden, setze Häckchen beim Parent
            parent_iid = self.text_preview.parent(child_iid)
            for child_iid in self.text_preview.get_children(parent_iid):
                tags = self.text_preview.item(child_iid, "tags")
                if "labeled" not in tags:
                    return
            
            values = self.text_preview.item(parent_iid, "values")
            values = (values[0] + "     ✓",)
            self.text_preview.item(parent_iid, values=values)

            self.update()
            self.labeling_finished()

    def labeling_finished(self):
        """Checks if all text elements have been rated and prompts the user to save.
        
        This method compares the total number of ratings with the length of the text.
        If all text elements have been rated, it displays a message box asking the user
        if they want to save the ratings. If the user confirms, it calls the save
        command.
        
        :returns: None
        """
        if self.total_ratings == len(self.text):
            # Falls alle Fragen beantwortet worde sind, fragen ob er speichern will.
            result = messagebox.askyesno(title="Glückwunsch", message="Du hast alle Textelemente bewertet.\nBewertungen speichern?")
            if result:
                self.save_cmd()

    def populate_percentage(self):
        """Updates the percentage label based on the total ratings.
        
        This method calculates the percentage of total ratings relative to the length
        of the text. It updates the percentage label with the calculated percentage
        and changes its style based on predefined thresholds.
        
        :returns: None
        """
        percentage = int(100 * self.total_ratings / len(self.text))
        percentage_str = str(int(100 * self.total_ratings / len(self.text))) + " %"
        self.percent_label.config(text=percentage_str)

        if percentage < 20:
            self.percent_label.config(style="Red.TLabel")
        elif percentage < 40:
            self.percent_label.config(style="Orange.TLabel")
        elif percentage < 60:
            self.percent_label.config(style="Yellow.TLabel")
        elif percentage < 80:
            self.percent_label.config(style="Lightgreen.TLabel")
        else:
            self.percent_label.config(style="Green.TLabel")

    def home_cmd(self):
        """Handles the home command action.
        
        This method prompts the user with a message box asking if they want to save
        the current rating session. If the user chooses to save, it calls the save
        command. Regardless of the user's choice, it initializes the frames and
        displays the main frame.
        
        :returns: None
        """
        result = messagebox.askyesno(title="Speichern?", message="Soll die Bewertungssession gespeichert werden?")
        if result:
            self.save_cmd()

        self.container.init_frames()

        self.container.show_frame("MainFrame")

    def help_cmd(self,event=None):
        """Opens the help frame for the RateFrame.
        
        This method creates an instance of the RateHelpFrame class, which displays
        help information related to the RateFrame.
        
        :param event: Optional; the event that triggered the help command.
        :type event: tkinter.Event, optional
        """
        RateHelpFrame(self.container)

    def update_frame(self, mode=None):
        """Updates the frame with the latest text and ratings.
        
        This method sets the focus, updates the text from the container, and initializes
        the ratings list. If the mode is 'do', it randomizes the text and ratings. It
        also deletes and repopulates categories, questions, navigation, text, and
        percentage.
        
        :param mode: Optional; if set to 'do', randomizes text and ratings.
        :type mode: str, optional
        """
        self.focus_set() # Für Zugriff auf Key-Bindings von left- und right-arrow
        self.text = self.container.formatted_text
        for text_entry in self.text:
            # Liste mit leeren Tupeln füllen, da noch kein Rating gesetzt.
            self.ratings.append(())
        
        if mode == "do":
            self.randomize(mode)

        self.delete_categories()
        self.populate_categories()
        self.delete_questions()
        self.populate_navigation()
        self.populate_text()
        self.populate_percentage()
        






















