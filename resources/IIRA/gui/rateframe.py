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
    """    Represents the frame for rating texts in the application. Inherits from ContainerFrame and provides functionalities for navigating, rating, and saving text ratings."""

    def __init__(self, container):
        """    Initializes the RateFrame with the given container. Sets up the UI components, styles, and event bindings.

    Args:
        container (Container): The container that holds this frame."""
        self.text = []
        self.text_index = 0
        self.profile = container.dbinteraction.active_profile
        self.ratings = []
        self.total_ratings = 0
        self.shuffler = None
        self.undo_shuffler = None
        super().__init__(container)
        container.style.configure('RateFrame.Treeview', font='Arial 16 bold', rowheight=30)
        container.style.configure('RateFrame.Treeview.Heading', font='Arial 18')
        container.style.configure('RateFrame.TRadiobutton', font='Arial 16')
        container.style.configure('Red.TLabel', foreground='#CC0000')
        container.style.configure('Orange.TLabel', foreground='#FF8000')
        container.style.configure('Yellow.TLabel', foreground='#CCCC00')
        container.style.configure('Lightgreen.TLabel', foreground='#00FF00')
        container.style.configure('Green.TLabel', foreground=self.accent_color)
        self.bind('<Right>', self.next_cmd)
        self.bind('<Left>', self.prev_cmd)
        left_frame = ttk.Frame(self)
        mid_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)
        top_frame = ttk.Frame(self)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)
        separator_frame = ttk.Frame(self.menu_bar)
        separator_frame.grid(row=0, column=5, sticky='nsew')
        vert_separator = ttk.Separator(self.menu_bar, orient='vertical')
        vert_separator.grid(row=0, column=6, sticky='nsew')
        save_frame = ttk.Frame(self.menu_bar, width=75, height=50)
        save_label = ttk.Label(save_frame, text='Speichern', image=self.container.save_icon, compound='top', font='Arial 12')
        save_frame.bind('<Enter>', lambda x: self.on_enter(save_frame, save_label))
        save_frame.bind('<Leave>', lambda x: self.on_leave(save_frame, save_label))
        save_frame.bind('<Button-1>', lambda x: self.save_cmd())
        save_label.bind('<Button-1>', lambda x: self.save_cmd())
        save_frame.grid(row=0, column=7, sticky='nsew')
        save_label.place(relx=0.5, rely=0.5, anchor='center')
        delete_frame = ttk.Frame(self.menu_bar, width=85, height=50)
        delete_label = ttk.Label(delete_frame, text='Verwerfen', image=self.container.delete_icon, compound='top', font='Arial 12')
        delete_frame.bind('<Enter>', lambda x: self.on_enter(delete_frame, delete_label))
        delete_frame.bind('<Leave>', lambda x: self.on_leave(delete_frame, delete_label))
        delete_frame.bind('<Button-1>', lambda x: self.delete_cmd())
        delete_label.bind('<Button-1>', lambda x: self.delete_cmd())
        delete_frame.grid(row=0, column=8, sticky='nsew')
        delete_label.place(relx=0.5, rely=0.5, anchor='center')
        horizon_separator = ttk.Separator(self.menu_bar, orient='horizontal')
        horizon_separator.grid(row=1, column=6, columnspan=3, sticky='nsew')
        self.menu_bar.grid(row=0, column=0, columnspan=3, sticky='nsew')
        self.menu_bar.columnconfigure(5, weight=1)
        left_frame.grid(row=3, column=0, sticky='nsew')
        left_frame.rowconfigure(0, weight=1)
        columns = 'text'
        self.text_preview = ttk.Treeview(left_frame, columns=columns, show='headings', style='RateFrame.Treeview', selectmode='browse')
        self.text_preview.heading('text', text='Navigation')
        self.text_preview.pack(fill='both', expand=True, pady=25, padx=5)
        self.text_preview.tag_configure('unselected', font='Arial 14')
        self.text_preview.bind('<Double-Button-1>', self.doubleclick_treeview)
        self.text_preview.bind('<Right>', self.next_cmd)
        self.text_preview.bind('<Left>', self.prev_cmd)
        self.percent_label = ttk.Label(top_frame, text='0 %', font='Arial 20', style='Red.TLabel')
        self.percent_label.pack()
        top_frame.grid(row=2, column=1, sticky='nsew')
        self.text_label = ttk.Label(mid_frame, text='', font='Arial 20')
        mid_btn_container = ttk.Frame(mid_frame)
        prev_btn = ttk.Button(mid_btn_container, text='❮', command=self.prev_cmd)
        next_btn = ttk.Button(mid_btn_container, text='❯', command=self.next_cmd)
        prev_btn.pack(side='left', padx=5)
        next_btn.pack(side='right', padx=5)
        mid_frame.grid(row=3, column=1, sticky='nsew')
        self.text_label.grid(row=0, column=0)
        mid_btn_container.grid(row=1, column=0, pady=20)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.columnconfigure(0, weight=1)
        right_seperator0 = ttk.Frame(right_frame)
        right_seperator1 = ttk.Frame(right_frame)
        self.categories_var = tk.StringVar()
        right_frame.grid(row=3, column=2, sticky='nsew', padx=(5, 15), pady=10)
        self.rbtn_container = ttk.Frame(right_frame)
        right_seperator0.grid(row=1, column=0)
        self.rbtn_container.grid(row=2, column=0)
        right_seperator1.grid(row=3, column=0)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(3, weight=1)
        self.populate_categories()

    def populate_navigation(self):
        """    Populates the navigation tree view with parent and child nodes based on the text content. Each parent node represents a group of text elements, and each child node represents an individual text element."""
        upper_limit = math.ceil(len(self.text) / 10)
        for i in range(upper_limit):
            if i == upper_limit - 1:
                self.text_preview.insert('', 'end', iid='parent_' + str(i), open=False, values=('Elemente ' + str(i * 10 + 1) + ' - ' + str(len(self.text)),))
            else:
                self.text_preview.insert('', 'end', iid='parent_' + str(i), open=False, values=('Elemente ' + str(i * 10 + 1) + ' - ' + str(i * 10 + 10),))
            for j in range(10):
                k = j + 10 * i
                if k >= len(self.text):
                    break
                n = self.count_upper_case(self.text[k], 18)
                nav_text = self.text[k]
                if len(self.text[k]) > n:
                    nav_text = self.text[k][:n] + '...'
                self.text_preview.insert('parent_' + str(i), 'end', iid='child_' + str(k), open=False, values=(nav_text,), tags='unselected')
        self.text_preview.item('parent_0', open=True)
        self.text_preview.focus('child_0')
        self.text_preview.selection_set('child_0')

    def randomize(self, mode):
        """    Randomizes the order of the text elements and their corresponding ratings. Can also undo the randomization.

    Args:
        mode (str): The mode of operation. 'do' to randomize, 'undo' to revert to the original order."""
        if mode == 'do':
            self.shuffler = np.random.permutation(len(self.text))
            self.undo_shuffler = np.argsort(self.shuffler)
            self.text = [self.text[j] for j in self.shuffler]
            self.ratings = [self.ratings[j] for j in self.shuffler]
        if mode == 'undo':
            self.text = [self.text[j] for j in self.undo_shuffler]
            self.ratings = [self.ratings[j] for j in self.undo_shuffler]

    def doubleclick_treeview(self, event):
        """    Handles the double-click event on the tree view. Sets the current text index to the clicked item and updates the text and rating display.

    Args:
        event (Event): The event object containing information about the double-click event."""
        item_iid = self.text_preview.identify_row(event.y)
        if 'child_' in item_iid:
            self.text_index = int(item_iid.replace('child_', ''))
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
            else:
                self.categories_var.set('')
        self.focus_set()

    def delete_questions(self):
        """    Deletes all items from the navigation tree view."""
        for item in self.text_preview.get_children():
            self.text_preview.delete(item)

    def populate_categories(self):
        """    Populates the rating categories based on the scale format (nominal, ordinal, interval, or ratio). Sets up radio buttons or entry fields for rating input."""
        if self.container.scale_format == 'intervall' or self.container.scale_format == 'ratio':
            info_label = ttk.Label(self.rbtn_container, text='Eingegeben:', font='Arial 16')
            self.var_entered = ttk.Label(self.rbtn_container, text='n.a.', font='Arial 16')
            self.var_input = ttk.Entry(self.rbtn_container, textvariable=self.categories_var, text='Zahlenwert eingeben', font='Arial 16')
            self.var_input.bind('<Return>', self.entry_input_cmd)
            info_label.pack(pady=5)
            self.var_entered.pack(pady=5)
            self.var_input.pack(pady=15)
        else:
            categories_rbtns = []
            for i in range(len(self.container.categories)):
                categories_rbtns.append(ttk.Radiobutton(self.rbtn_container, text=self.container.categories[i], variable=self.categories_var, value=self.container.categories[i], style='RateFrame.TRadiobutton', command=self.label_text))
                categories_rbtns[i].pack(side='top', anchor='nw', pady=5)
                if i < 9:
                    if self.container.scale_format == 'nominal' or self.container.scale_format == 'ordinal':
                        self.bind_all(str(i + 1), self.cat_hotkey_cmd)

    def delete_categories(self):
        """    Deletes all widgets from the rating button container."""
        children_widgets = self.rbtn_container.winfo_children()
        for widget in children_widgets:
            widget.destroy()

    def populate_text(self):
        """    Updates the text label with the current text element, adding newlines for better readability."""
        self.text_label.config(text=self.add_newlines(self.text[self.text_index], 75))

    def add_newlines(self, text, n):
        """    Adds newlines to the text at appropriate positions to ensure it fits within a specified width.

    Args:
        text (str): The text to be formatted.
        n (int): The maximum number of characters per line.

    Returns:
        str: The formatted text with newlines."""
        n = self.count_upper_case(text, n)
        if len(text) < n:
            return text
        form_text = ''
        for word in text.split(' '):
            if len(word) > n:
                word = word[:n] + '\n' + word[n:]
            form_text += word + ' '
        offset = 0
        try:
            while True:
                p = form_text.rindex(' ', offset, offset + n)
                form_text = form_text[:p] + '\n' + form_text[p + 1:]
                offset = p
                if len(form_text[p + 1:]) < n:
                    return form_text
        except ValueError:
            pass
        return form_text

    def count_upper_case(self, text, n):
        """    Counts the number of uppercase characters in the text and adjusts the maximum line length if the text contains many uppercase characters.

    Args:
        text (str): The text to be analyzed.
        n (int): The initial maximum number of characters per line.

    Returns:
        int: The adjusted maximum number of characters per line."""
        count_upper_case = 0
        for char in text:
            if char.isupper():
                count_upper_case += 1
        if count_upper_case >= len(text) // 2:
            n = int(n * 0.75)
        return n

    def entry_input_cmd(self, event=None):
        """    Handles the event when the user presses the Enter key in the entry field. Sets the rating based on the input value and moves to the next text element.

    Args:
        event (Event, optional): The event object containing information about the key press event."""
        if len(self.var_input.get()) == 0:
            return
        self.categories_var.set(self.var_input.get())
        self.label_text()
        self.next_cmd()
        self.var_input.delete(0, 'end')

    def cat_hotkey_cmd(self, event):
        """    Handles the event when the user presses a hotkey to select a rating category. Sets the rating based on the hotkey and updates the display.

    Args:
        event (Event): The event object containing information about the key press event."""
        category_no = int(event.char) - 1
        self.categories_var.set(self.container.categories[category_no])
        self.label_text()

    def next_cmd(self, event=None):
        """    Moves to the next text element in the list and updates the display. If the current text element is the last one, does nothing.

    Args:
        event (Event, optional): The event object containing information about the key press event."""
        self.focus_set()
        if self.text_index == len(self.text) - 1:
            return
        else:
            self.text_index = self.text_index + 1
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
                if self.container.scale_format == 'intervall' or self.container.scale_format == 'ratio':
                    self.var_entered.config(text=self.categories_var.get())
            else:
                self.categories_var.set('')
                if self.container.scale_format == 'intervall' or self.container.scale_format == 'ratio':
                    self.var_entered.config(text='n.a.')
            parent_iid = 'parent_' + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = 'parent_' + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)
            child_iid = 'child_' + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)

    def prev_cmd(self, event=None):
        """    Moves to the previous text element in the list and updates the display. If the current text element is the first one, does nothing.

    Args:
        event (Event, optional): The event object containing information about the key press event."""
        self.focus_set()
        if self.text_index == 0:
            return
        else:
            self.text_index = self.text_index - 1
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
                if self.container.scale_format == 'intervall' or self.container.scale_format == 'ratio':
                    self.var_entered.config(text=self.categories_var.get())
            else:
                self.categories_var.set('')
                if self.container.scale_format == 'intervall' or self.container.scale_format == 'ratio':
                    self.var_entered.config(text='n.a.')
            parent_iid = 'parent_' + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = 'parent_' + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)
            child_iid = 'child_' + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)

    def save_cmd(self):
        """    Prompts the user to save the ratings to a file. If the text elements were randomized, undoes the randomization before saving."""
        if self.shuffler is not None:
            self.randomize('undo')
        self.focus_set()
        filename = tk.filedialog.asksaveasfilename(filetypes=[('Excel files', '.xlsx .xls'), ('Libreoffice Calc files', '.ods'), ('Csv files', '.csv')])
        self.container.filevalidation.write_file(filename, self.ratings)

    def delete_cmd(self):
        """    Prompts the user to confirm the deletion of the entire rating session. If confirmed, resets all ratings and updates the display."""
        self.focus_set()
        result = messagebox.askyesno(title='Verwerfen', message='Die gesamte Bewertungssession verwerfen?')
        if result:
            self.categories_var.set('')
            self.ratings = []
            for text_entry in self.text:
                self.ratings.append(())
                self.text_index = 0
                self.update_frame()
        else:
            return

    def label_text(self, event=None):
        """    Sets the rating for the current text element based on the selected category. Updates the navigation tree view and checks if all text elements have been rated.

    Args:
        event (Event, optional): The event object containing information about the event."""
        self.focus_set()
        if self.ratings[self.text_index]:
            if self.ratings[self.text_index][RATING] == self.categories_var.get():
                self.ratings[self.text_index] = ()
                self.categories_var.set('')
                self.total_ratings -= 1
                self.populate_percentage()
                child_iid = 'child_' + str(self.text_index)
                self.text_preview.item(child_iid, tags=self.text_preview.item(child_iid, 'tags')[0])
                self.text_preview.item(child_iid, values=(self.text_preview.item(child_iid, 'values')[0].replace(' ✓', ''),))
                parent_iid = self.text_preview.parent(child_iid)
                values = self.text_preview.item(parent_iid, 'values')
                values = (values[0].replace('     ✓', ''),)
                self.text_preview.item(parent_iid, values=values)
            else:
                self.ratings[self.text_index] = (self.container.dbinteraction.active_profile, self.categories_var.get())
        else:
            self.ratings[self.text_index] = (self.container.dbinteraction.active_profile, self.categories_var.get())
            self.total_ratings += 1
            self.populate_percentage()
            child_iid = 'child_' + str(self.text_index)
            tags = self.text_preview.item(child_iid, 'tags')
            values = self.text_preview.item(child_iid, 'values')
            if 'labeled' not in tags:
                tags += ('labeled',)
                values = (values[0] + ' ✓',)
            self.text_preview.item(child_iid, tags=tags)
            self.text_preview.item(child_iid, values=values)
            self.text_preview.selection_set(child_iid)
            parent_iid = self.text_preview.parent(child_iid)
            for child_iid in self.text_preview.get_children(parent_iid):
                tags = self.text_preview.item(child_iid, 'tags')
                if 'labeled' not in tags:
                    return
            values = self.text_preview.item(parent_iid, 'values')
            values = (values[0] + '     ✓',)
            self.text_preview.item(parent_iid, values=values)
            self.update()
            self.labeling_finished()

    def labeling_finished(self):
        """    Checks if all text elements have been rated. If so, prompts the user to save the ratings."""
        if self.total_ratings == len(self.text):
            result = messagebox.askyesno(title='Glückwunsch', message='Du hast alle Textelemente bewertet.\nBewertungen speichern?')
            if result:
                self.save_cmd()

    def populate_percentage(self):
        """    Updates the percentage label to reflect the current progress of the rating session. Changes the label color based on the percentage of completion."""
        percentage = int(100 * self.total_ratings / len(self.text))
        percentage_str = str(int(100 * self.total_ratings / len(self.text))) + ' %'
        self.percent_label.config(text=percentage_str)
        if percentage < 20:
            self.percent_label.config(style='Red.TLabel')
        elif percentage < 40:
            self.percent_label.config(style='Orange.TLabel')
        elif percentage < 60:
            self.percent_label.config(style='Yellow.TLabel')
        elif percentage < 80:
            self.percent_label.config(style='Lightgreen.TLabel')
        else:
            self.percent_label.config(style='Green.TLabel')

    def home_cmd(self):
        """    Prompts the user to save the rating session before returning to the main frame. If confirmed, saves the ratings and switches to the main frame."""
        result = messagebox.askyesno(title='Speichern?', message='Soll die Bewertungssession gespeichert werden?')
        if result:
            self.save_cmd()
        self.container.init_frames()
        self.container.show_frame('MainFrame')

    def help_cmd(self, event=None):
        """    Displays the help frame for the rating session.

    Args:
        event (Event, optional): The event object containing information about the event."""
        RateHelpFrame(self.container)

    def update_frame(self, mode=None):
        """    Updates the frame with the current text elements and ratings. Optionally randomizes the text elements.

    Args:
        mode (str, optional): The mode of operation. 'do' to randomize the text elements."""
        self.focus_set()
        self.text = self.container.formatted_text
        for text_entry in self.text:
            self.ratings.append(())
        if mode == 'do':
            self.randomize(mode)
        self.delete_categories()
        self.populate_categories()
        self.delete_questions()
        self.populate_navigation()
        self.populate_text()
        self.populate_percentage()