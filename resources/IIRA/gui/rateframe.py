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

    def __init__(self, container):
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
        if mode == "do":
            self.shuffler = np.random.permutation(len(self.text))
            self.undo_shuffler = np.argsort(self.shuffler)

            self.text = [self.text[j] for j in self.shuffler]
            self.ratings = [self.ratings[j] for j in self.shuffler]
        if mode == "undo":
            self.text = [self.text[j] for j in self.undo_shuffler]
            self.ratings = [self.ratings[j] for j in self.undo_shuffler]


    def doubleclick_treeview(self, event):
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
        for item in self.text_preview.get_children():
            self.text_preview.delete(item)

    def populate_categories(self):
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
        children_widgets = self.rbtn_container.winfo_children()
        for widget in children_widgets:
            widget.destroy()

    def populate_text(self):
        self.text_label.config(text=self.add_newlines(self.text[self.text_index], 75))

    def add_newlines(self, text, n):
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
        count_upper_case = 0 
        for char in text:
            if char.isupper():
                count_upper_case += 1
        if count_upper_case >= len(text) // 2:
            n = int(n * 0.75)
        
        return n

    def entry_input_cmd(self, event=None):
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
        category_no = int(event.char) - 1

        # Wert der Variablen anpassen
        self.categories_var.set(self.container.categories[category_no])

        # Das Rating in der Datenstruktur setzen und den Navigationsframe auf der linken Seite anpassen.
        self.label_text()

    def next_cmd(self, event=None):

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
        if self.total_ratings == len(self.text):
            # Falls alle Fragen beantwortet worde sind, fragen ob er speichern will.
            result = messagebox.askyesno(title="Glückwunsch", message="Du hast alle Textelemente bewertet.\nBewertungen speichern?")
            if result:
                self.save_cmd()

    def populate_percentage(self):
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
        result = messagebox.askyesno(title="Speichern?", message="Soll die Bewertungssession gespeichert werden?")
        if result:
            self.save_cmd()

        self.container.init_frames()

        self.container.show_frame("MainFrame")

    def help_cmd(self,event=None):
        RateHelpFrame(self.container)

    def update_frame(self, mode=None):
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
        