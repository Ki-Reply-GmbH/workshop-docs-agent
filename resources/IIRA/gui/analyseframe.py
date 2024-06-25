"""Provides GUI components for reliability analysis using tkinter.

This module sets up the graphical user interface (GUI) for performing
reliability analysis, including intra-rater and inter-rater analysis. It
includes classes for creating and managing frames, handling user inputs,
and displaying results.

Classes:

AnalyseFrame
Sets up the GUI components for reliability analysis, including
methods for populating rater and metrics containers, initiating
the analysis, and updating the frame.

ResultsFrame
Sets up the GUI components for displaying reliability analysis
results. It includes methods for calculating and populating
intra-rater and inter-rater results, exporting results to a file,
and updating the frame with dynamic data.
"""


import tkinter as tk
from tkinter import ttk, messagebox
from math import isnan

from gui.containerframe import ContainerFrame
from gui.helperframes import ScrollFrame, PrepAnalyseHelpFrame, ResultsHelpFrame
from core.create_analyses import CreateAnalyses
from core.fileinteraction import write_excel
from core.metrics import map_metrics

selected_intra_ids = []
selected_inter_ids = []
selected_intra_metrics = []
selected_inter_metrics = []

class AnalyseFrame(ContainerFrame):
    """A class to represent the AnalyseFrame, setting up the GUI components for
    reliability analysis, including methods for populating rater and metrics
    containers, initiating the analysis, and updating the frame.
    """
    def __init__(self, container):
        """Initializes the AnalyseFrame class, setting up the GUI components for the
        analysis frame.
        
        :param container: The parent container to which this frame belongs.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following steps:
        
        1. Initializes various metrics and their corresponding tkinter IntVar variables
        for intra-rater and inter-rater reliability analysis.
        2. Creates dictionaries to map metric names to their IntVar variables for both
        intra-rater and inter-rater metrics.
        3. Initializes dictionaries to hold selected intra-rater and inter-rater IDs.
        4. Calls the parent class constructor.
        5. Configures the style for buttons used in the AnalyseFrame.
        6. Sets up the left and right frames for the GUI layout.
        7. Adds labels, containers, and buttons for selecting raters and metrics.
        8. Configures the layout using grid and pack geometry managers.
        9. Sets the row and column weights for resizing behavior.
        """
        self.metrics = []

        self.intra_kappa = tk.IntVar()
        self.intra_fleiss_kappa = tk.IntVar()
        self.intra_alpha_coefficient = tk.IntVar()
        self.intra_ac = tk.IntVar()
        self.intra_icc = tk.IntVar()
        self.intra_metrics = {
            "Cohen's-|Conger's \u03BA": self.intra_kappa,
            "Fleiss' \u03BA": self.intra_fleiss_kappa,
            "Krippendorff's \u03B1": self.intra_alpha_coefficient,
            "Gwet's AC": self.intra_ac,
            "ICC": self.intra_icc
        }
        self.inter_kappa = tk.IntVar()
        self.inter_fleiss_kappa = tk.IntVar()
        self.inter_alpha_coefficient = tk.IntVar()
        self.inter_ac = tk.IntVar()
        self.inter_icc = tk.IntVar()
        self.inter_metrics = {
            "Cohen's-|Conger's \u03BA": self.inter_kappa,
            "Fleiss' \u03BA": self.inter_fleiss_kappa,
            "Krippendorff's \u03B1": self.inter_alpha_coefficient,
            "Gwet's AC": self.inter_ac,
            "ICC": self.inter_icc
        }

        self.intra_ids = {}
        self.inter_ids = {}


        super().__init__(container)
        container.style.configure("AnalyseFrame.TButton", font="Arial 15", foreground="black", width=15)

        left_frame = ttk.Frame(self, style="Card", padding=(5, 6, 7, 8))
        right_frame = ttk.Frame(self, style="Card", padding=(5, 6, 7, 8))

        rater_label = ttk.Label(left_frame, font="Arial 20", text="1. Auswahl der Bewerter")

        self.rater_container = ScrollFrame(left_frame)

        self.toggle_ids = ttk.Button(left_frame, text="Alle auswählen", style="AnalyseFrame.TButton",
                                    command=lambda: self.toggle("id"))

        metrics_label = ttk.Label(right_frame, font="Arial 20", text="2. Auswahl der Metriken")
        self.metrics_container = ttk.Frame(right_frame)

        self.toggle_metrics = ttk.Button(right_frame, text="Alle auswählen", style="AnalyseFrame.TButton",
                                    command=lambda: self.toggle("metric"))

        start_btn = ttk.Button(self, text="Analyse Starten", style="AnalyseFrame.TButton", 
                                 command=lambda: self.analyse_start(container))

        self.menu_bar.grid(row=0, column=0, sticky="nsew")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=50)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=50, pady=50)

        rater_label.pack(side="top", padx=25, pady=10)
        self.rater_container.pack(side="top", fill="y", expand=True, padx=25, pady=50)
        self.toggle_ids.pack(side="bottom")

        metrics_label.pack(side="top", padx=25, pady=10)
        self.metrics_container.pack(side="top", padx=25, pady=50)
        self.toggle_metrics.pack(side="bottom")

        start_btn.grid(row=2, column=0, columnspan=2, pady=25)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def analyse_start(self, container):
        """Initiates the analysis process by selecting metrics and IDs, validating the
        selections, and updating the results frame.
        
        :param container: The parent container to which this frame belongs.
        :type container: tkinter.Tk or tkinter.Toplevel
        :raises ValueError: If invalid selections are made.
        """
        global selected_intra_metrics
        for metric in self.intra_metrics:
            if self.intra_metrics[metric].get() == 1 and metric not in selected_intra_metrics:
                selected_intra_metrics.append(metric)

        global selected_inter_metrics 
        for metric in self.inter_metrics:
            if self.inter_metrics[metric].get() == 1 and metric not in selected_inter_metrics:
                selected_inter_metrics.append(metric)

        global selected_intra_ids
        for id in self.intra_ids:
            if self.intra_ids[id].get() == 1 and id not in selected_intra_ids:
                selected_intra_ids.append(id)

        global selected_inter_ids
        for id in self.inter_ids:
            if self.inter_ids[id].get() == 1 and id not in selected_inter_ids:
                selected_inter_ids.append(id)
        
        if len(selected_inter_ids) == 1:
            messagebox.showerror("Ungültige Eingabe", "Es kann keine Interrater-Untersuchung von nur einer Bewerter-ID berechnet werden.")
            selected_intra_metrics = []
            selected_inter_metrics = []
            selected_intra_ids = []
            selected_inter_ids = []
            return
        elif len(selected_inter_ids) == 0 and len(selected_inter_ids) == 0:
            messagebox.showerror("Ungültige Eingabe", "Bitte Bewerter-ID's für die Reliabilitätsuntersuchung auswählen.")
            # Auswahl vom User rückgängig machen
            selected_intra_metrics = []
            selected_inter_metrics = []
            return
        elif len(selected_intra_metrics) == 0 and len(selected_inter_metrics) == 0:
            messagebox.showerror("Ungültige Eingabe", "Bitte Metriken für die Reliabilitätsuntersuchung auswählen.")
            selected_intra_ids = []
            selected_inter_ids = []
            return
        
        container.frames["ResultsFrame"].update_frame()
        container.show_frame("ResultsFrame")

    def populate_rater_container(self):
        """Populates the rater container with IDs and corresponding variables.
        
        This method creates a table with rater IDs and their associated intrarater
        and interrater variables. It initializes these variables for each rater ID
        and adds them to the content list for table creation.
        
        :raises AttributeError: If `self.container` or `self.create_table` is not defined.
        """
        headings = ["ID", "Intrarater", "Interrater"]
        content = []
        for id in self.container.rater_ids:
            self.intra_ids[id] = tk.IntVar()
            self.inter_ids[id] = tk.IntVar()
            content.append([str(id), self.intra_ids[id], self.inter_ids[id]])

        self.create_table(self.rater_container.viewPort, headings, content)
        
    def populate_metrics_container(self):
        """Populates the metrics container based on the scale format.
        
        This method sets the available metrics according to the scale format of the
        container. It then creates a table with the metrics and their corresponding
        intrarater and interrater variables.
        
        :raises ValueError: If an invalid scale format is provided.
        """
        if self.container.scale_format == "nominal":
            self.metrics = ["Cohen's-|Conger's \u03BA", "Fleiss' \u03BA", "Krippendorff's \u03B1", "Gwet's AC"]
        elif self.container.scale_format == "ordinal":
            self.metrics = ["Cohen's-|Conger's \u03BA", "Fleiss' \u03BA", "Krippendorff's \u03B1", "Gwet's AC"]
        elif self.container.scale_format == "intervall":
            self.metrics = ["ICC"]
        elif self.container.scale_format == "rational":
            self.metrics = ["ICC"]
        
        headings = ["Metrik", "Intrarater", "Interrater"]
        content = []
        for metric in self.metrics:
            content.append([metric, self.map_metric_to_var("intra", metric), self.map_metric_to_var("inter", metric)])

        self.create_table(self.metrics_container, headings, content)
        
    def map_metric_to_var(self, mode, metric_name):
        """Maps a given metric name to its corresponding variable based on the mode.
        
        :param mode: The mode of the metric, either 'intra' or 'inter'.
        :type mode: str
        :param metric_name: The name of the metric to map.
        :type metric_name: str
        :returns: The variable corresponding to the given metric name and mode.
        :rtype: tk.IntVar
        """
        if mode == "intra":
            if metric_name == "Cohen's-|Conger's \u03BA":
                return self.intra_kappa
            elif metric_name == "Fleiss' \u03BA":
                return self.intra_fleiss_kappa
            elif metric_name == "Krippendorff's \u03B1":
                return self.intra_alpha_coefficient
            elif metric_name == "Gwet's AC":
                return self.intra_ac
            elif metric_name == "ICC":
                return self.intra_icc
        elif mode == "inter":
            if metric_name == "Cohen's-|Conger's \u03BA":
                return self.inter_kappa
            elif metric_name == "Fleiss' \u03BA":
                return self.inter_fleiss_kappa
            elif metric_name == "Krippendorff's \u03B1":
                return self.inter_alpha_coefficient
            elif metric_name == "Gwet's AC":
                return self.inter_ac
            elif metric_name == "ICC":
                return self.inter_icc
            

    def toggle(self, mode):
        """Toggles the selection state of either IDs or metrics.
        
        :param mode: The mode to toggle, either 'id' or 'metric'.
        :type mode: str
        :raises ValueError: If an invalid mode is provided.
        """
        if mode == "id":
            intra_dic = self.intra_ids
            inter_dic = self.inter_ids
            btn = self.toggle_ids
        if mode == "metric":
            intra_dic = self.intra_metrics
            inter_dic = self.inter_metrics
            btn = self.toggle_metrics

        all_set = True
        for i in intra_dic:
            if mode == "metric":
                if i not in self.metrics:
                    continue
            if intra_dic[i].get() == 0:
                all_set = False
                break
        for i in inter_dic:
            if mode == "metric":
                if i not in self.metrics:
                    continue
            if inter_dic[i].get() == 0:
                all_set = False
                break
        
        if all_set: 
            for i in intra_dic:
                intra_dic[i].set(0)
            for i in inter_dic:
                inter_dic[i].set(0)
            btn.config(text="Alle auswählen")
        else:
            for i in intra_dic:
                if mode == "metric":
                    if i not in self.metrics:
                        continue
                intra_dic[i].set(1)
            for i in inter_dic:
                if mode == "metric":
                    if i not in self.metrics:
                        continue
                inter_dic[i].set(1)
            btn.config(text="Alle abwählen")

    def help_cmd(self,event=None):
        """Opens the help frame for the AnalyseFrame.
        
        This method creates an instance of the PrepAnalyseHelpFrame class,
        which displays a help frame with relevant information for the
        AnalyseFrame.
        
        :param event: The event that triggered the help command, defaults to None.
        :type event: tkinter.Event, optional
        """
        PrepAnalyseHelpFrame(self.container)

    def update_frame(self):
        """Updates the frame by populating the rater and metrics containers.
        
        This method is responsible for refreshing the content of the frame by
        invoking methods to populate the rater container and the metrics container.
        """
        self.populate_rater_container()
        self.populate_metrics_container()

class ResultsFrame(ContainerFrame):
    """A class to represent the ResultsFrame, which sets up the GUI components
    for displaying reliability analysis results. It includes methods for
    calculating and populating intra-rater and inter-rater results, exporting
    results to a file, and updating the frame with dynamic data.
    """
    def __init__(self, container):
        """Initializes the ResultsFrame class, setting up the GUI components for displaying
        reliability analysis results.
        
        :param container: The parent container to which this frame belongs.
        :type container: tkinter.Tk or tkinter.Toplevel
        
        The constructor performs the following steps:
        
        1. Initializes the debug mode and reliability analyses attributes.
        2. Calls the parent class constructor.
        3. Configures the styles for buttons and notebook tabs.
        4. Creates a central container frame and a notebook widget.
        5. Adds a label for the results section.
        6. Sets up frames and scrollable frames for intra-rater and inter-rater results.
        7. Adds an export button with a command to export results.
        8. Arranges the layout using grid and pack geometry managers.
        9. Configures the row and column weights for resizing behavior.
        """
        self.debug = True
        self.reliability_analyses = None
        super().__init__(container)
        container.style.configure("ResultsFrame.TButton", font="Arial 15", foreground="black")
        container.style.configure("TNotebook.Tab", font="Arial 15")

        center_container = ttk.Frame(self)
        self.notebook = ttk.Notebook(center_container)

        results_label = ttk.Label(center_container, font="Arial 20", text="Ergebnisse")

        self.intrarater_frame = ttk.Frame(self.notebook)
        self.intrarater_results = ScrollFrame(self.intrarater_frame)
        self.intrarater_infos = ScrollFrame(self.intrarater_frame)



        self.interrater_frame = ttk.Frame(self.notebook)
        self.interrater_results = ttk.Frame(self.interrater_frame)
        self.interrater_infos = ScrollFrame(self.interrater_frame)

        export_btn = ttk.Button(center_container, text="Exportieren", style="ResultsFrame.TButton", 
                                command=self.export_cmd) #TODO command

        self.menu_bar.grid(row=0, column=0, sticky="nsew")
        center_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        results_label.grid(row=0, column=0, columnspan=3 ,padx=5, pady=5)
        self.notebook.grid(row=1, column=0, sticky="nsew",padx=5, pady=5)

        export_btn.grid(row=2, column=0)

        self.intrarater_results.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=25)
        self.intrarater_infos.pack(side="right", fill="both", padx=(0, 15), pady=25)

        self.interrater_results.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=25)
        self.interrater_infos.pack(side="right", fill="both", padx=(0, 15), pady=25)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        center_container.rowconfigure(1, weight=1)
        center_container.columnconfigure(0, weight=1)

        self.intrarater_frame.rowconfigure(0, weight=1)
        self.intrarater_frame.columnconfigure(0, weight=1)

    def calculate_results(self):
        """Calculates and initializes reliability analyses for intra-rater and inter-rater
        metrics using the selected IDs and metrics.
        
        :raises ValueError: If any of the required parameters are missing or invalid.
        """
        self.reliability_analyses = CreateAnalyses(selected_intra_ids, selected_inter_ids, 
                                                   selected_intra_metrics, selected_inter_metrics,
                                                   self.container.scale_format, self.container.categories,
                                                   self.container.weights, self.container.filevalidation.labels)

    def populate_intra_results(self):
        """Populates the intra-rater results tab with the selected metrics and relevant
        information.
        
        Adds a new tab to the notebook for intra-rater results, constructs the table
        headings and content based on the selected metrics, and appends additional
        information if the scale format is nominal or ordinal. Displays the results
        in a table and provides additional information in labeled frames.
        
        :raises ZeroDivisionError: If a division by zero occurs while calculating
        metric values.
        :raises Exception: If an error occurs while retrieving metric values.
        """
        if selected_intra_ids and selected_intra_metrics:
            self.notebook.add(self.intrarater_frame, text="Intra-Rater")

            headings = ["ID"]
            for metric in selected_intra_metrics:
                headings.append(metric)
            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                headings.append("#Subjects")
                headings.append("#Replicates")

            content = []

            not_enough_ratings = []

            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                for rater_id in self.reliability_analyses.results["intra"]:
                    quant_subjects = self.reliability_analyses.results["intra"][rater_id].n
                    quant_replicates = self.reliability_analyses.results["intra"][rater_id].r

                    if quant_replicates < 2 or quant_subjects < 1:
                        not_enough_ratings.append(str(rater_id))
                        continue
                    
                    if self.debug:
                        print("populate_intra_results")
                        print("Rater id: " + str(rater_id))
                        print("quant_subjects " + str(quant_subjects))
                        print("quant_replicates " + str(quant_replicates))
                        print()
                    row = []
                    cont = False
                    for metric in selected_intra_metrics:
                        metric_function_name = map_metrics(metric)

                        metric_value = -99
                        try:
                            metric_value = getattr(self.reliability_analyses.results["intra"][rater_id], metric_function_name)()["est"]["coefficient_value"]
                        except ZeroDivisionError:
                            metric_value = 1.0
                        except Exception as e:
                            print("Exception in populate_intra_results:" + str(e))
                        
                        if isnan(metric_value) and metric == "Cohen's-|Conger's \u03BA":
                            metric_value = 1.0
                            
                        row.append(str(metric_value))
                    
                    if cont:
                        continue
                    row.insert(0, str(rater_id))
                    row.append(str(quant_subjects))
                    row.append(str(quant_replicates))  
                    content.append(row)

            else:
                for rater_id in self.reliability_analyses.results["intra"]:

                    row = [str(rater_id)]
                    metric_function_name = map_metrics(metric)

                    metric_value = -99 
                    try:
                        metric_value = self.reliability_analyses.results["intra"][rater_id].iloc[2]["ICC"]
                    except Exception as e:
                        print("Exception in populate_intra_results:" + str(e))

                    row.append(str(metric_value))
                    content.append(row)

            if self.debug:
                print("populate_intra_results")

                print("Headings")
                print(headings)
                print()

                print("Content")
                print(content)
                print()

            self.create_table(self.intrarater_results.viewPort, headings, content)

            intrarater_infolabel = ttk.Label(self.intrarater_infos.viewPort, font="Arial 20", text="Infos:")

            intrarater_info_list = ttk.Frame(self.intrarater_infos.viewPort)

            txt = "Skalenformat: " + self.container.scale_format
            scale_format_lbl = ttk.Label(intrarater_info_list, font="Arial 18", text=txt)
            scale_format_lbl.pack(padx=5, pady=5, fill="x")

            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal": 
                txt = "Gewichte: " + self.container.weights
                weights_lbl = ttk.Label(intrarater_info_list, font="Arial 18", text=txt)
                weights_lbl.pack(padx=5, pady=(5, 15), fill="x")

                if not_enough_ratings:
                    txt = "Keine Subjects mehrfach\nbewertet:"
                    not_enough_ratings_lbl = ttk.Label(intrarater_info_list, font="Arial 18", text=txt)
                    not_enough_ratings_lbl.pack(padx=5, pady=5, fill="x")

                    for rater_id in not_enough_ratings:
                        txt = "• " + str(rater_id)
                        no_replicates = ttk.Label(intrarater_info_list, font="Arial 18", text=txt)
                        no_replicates.pack(padx=5, pady=5, fill="x")

            intrarater_infolabel.pack(pady=15)
            intrarater_info_list.pack(fill="y")

    def populate_inter_results(self):
        """Populates the inter-rater results tab with the selected metrics and relevant
        information.
        
        Adds a new tab to the notebook for inter-rater results, constructs the table
        headings and content based on the selected metrics, and appends additional
        information if the scale format is nominal or ordinal. Displays the results
        in a table and provides additional information in labeled frames.
        
        :raises Exception: If an error occurs while retrieving metric values.
        """
        if selected_inter_ids and selected_inter_metrics:
            self.notebook.add(self.interrater_frame, text="Inter-Rater")    # Legt einen neuen Tab im Notebook an

            headings = []
            for metric in selected_inter_metrics:
                headings.append(metric)
            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                headings.append("#Subjects")
                headings.append("#Rater")

            content = []

            row = []
            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                for metric in selected_inter_metrics:
                    metric_function_name = map_metrics(metric)

                    metric_value = -99
                    try:
                        metric_value = getattr(self.reliability_analyses.results["inter"], metric_function_name)()["est"]["coefficient_value"]
                    except Exception as e:
                        print("Exception in populate_intra_results:" + str(e))
                    row.append(str(metric_value))
            else:
                metric_value = -99 
                try:
                    metric_value = self.reliability_analyses.results["inter"].iloc[2]["ICC"]
                except Exception as e:
                    print("Exception in populate_intra_results:" + str(e))

                row.append(str(metric_value)) 
                content.append(row)

            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                quant_subjects = self.reliability_analyses.results["inter"].n
                row.append(str(quant_subjects))
                quant_raters = self.reliability_analyses.results["inter"].r
                row.append(str(quant_raters))
                content.append(row)
            
            self.create_table(self.interrater_results, headings, content)

            interrater_infolabel = ttk.Label(self.interrater_infos, font="Arial 18", text="Infos:")

            interrater_info_list = ttk.Frame(self.interrater_infos)
            txt = "Skalenformat: " + self.container.scale_format
            scale_format_lbl = ttk.Label(interrater_info_list, font="Arial 18", text=txt)
            scale_format_lbl.pack(padx=5, pady=5, fill="x")

            if self.container.scale_format == "nominal" or self.container.scale_format == "ordinal":
                txt = "Gewichte: " + self.container.weights
                weights_lbl = ttk.Label(interrater_info_list, font="Arial 18", text=txt)
                weights_lbl.pack(padx=5, pady=(5, 15), fill="x")


            # Platzierungen
            interrater_infolabel.pack(pady=15)
            interrater_info_list.pack(pady=15)

    def export_cmd(self):

        """Saves the reliability analysis results to a file selected by the user.
        
        The user is prompted to choose a file location and format. The supported file
        formats are Excel (.xlsx, .xls), LibreOffice Calc (.ods), and CSV (.csv).
        
        :raises ValueError: If the filename is not provided or invalid.
        """
        filename = tk.filedialog.asksaveasfilename(filetypes=[
            ("Excel files", ".xlsx .xls"), 
            ("Libreoffice Calc files", ".ods"),
            ("Csv files", ".csv")
            ])
        write_excel(self.reliability_analyses, selected_intra_ids, selected_intra_metrics, selected_inter_ids, 
                    selected_inter_metrics, self.container.scale_format, filename) # TODO path abfragen

    def help_cmd(self,event=None):
        """
        Die Funktion öffnet das Helpframe.
        """
        # Jedes Frame erzeugt ein HelpFrame mit eigenen Inhalten.
        # Wird in den vererbten Klassen implementiert.
        ResultsHelpFrame(self.container)

    def update_frame(self):
        """
        Die Funktion füllt den Frame mit dynamisch erzeugten Daten.
        """
        self.calculate_results()
        self.populate_intra_results()
        self.populate_inter_results()














