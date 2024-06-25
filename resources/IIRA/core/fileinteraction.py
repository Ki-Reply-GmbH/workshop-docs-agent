"""Module for validating and processing file content based on specific formats.

This module handles reading file content, determining its format, and extracting
various attributes such as categories, rater IDs, text, and labels. It supports
files in Excel, ODS, and CSV formats, and processes them according to 'nominal'
or 'ordinal' scale formats. The module also provides methods for writing
processed data back to a file and performing specific text processing tasks.

Classes:

FileValidation
A class for validating and processing file content based on specific
formats.

DBInteraction
A class to handle database interactions, including loading, creating,
deleting, and changing profiles, and writing profile data to a CSV file.

Functions:

write_excel(analyse, intra_ids, intra_metrics, inter_ids, inter_metrics,
scale_format, filename)
Writes analysis results to an Excel file.
"""


import re
import pathlib
import datetime
from math import isnan

import pandas as pd
import numpy as np
import xlsxwriter
from pprint import pprint

from core.metrics import map_metrics

PROFILE = 0
RATING = 1

class FileValidation():
    """A class for validating and processing file content based on specific formats.
    
    This class handles reading file content, determining its format, and extracting
    various attributes such as categories, rater IDs, text, and labels. It supports
    files in Excel, ODS, and CSV formats, and processes them according to 'nominal'
    or 'ordinal' scale formats. The class also provides methods for writing processed
    data back to a file and performing specific text processing tasks.
    """
    def __init__(self, file, scale_format):
        """Initializes the FileValidation class with the provided file and scale format.
        
        This constructor sets up various attributes and processes the input file based on
        its extension. It reads the file content into a DataFrame, removes unnamed columns,
        and performs initial checks and data extraction based on the scale format.
        
        :param file: The file path to be validated.
        :type file: str
        :param scale_format: The scale format, either 'nominal' or 'ordinal'.
        :type scale_format: str
        :raises ValueError: If the file format cannot be determined based on headers.
        """
        self.debug = False
        file_extension = pathlib.Path(file).suffix
        self.content = None
        self.format = None

        self.scale_format = scale_format
        self.categories = []
        self.rater_ids = []
        self.text = []
        self.formatted_text = []
        self.labels = {}

        if file_extension == ".xlsx" or file_extension == ".xls":
            self.content = pd.read_excel(file)
        elif file_extension == ".ods":
            self.content = pd.read_excel(file, engine="odf")
        else:
            self.content = pd.read_csv(file, delimiter=";")

        self.content = self.content.loc[:, ~self.content.columns.str.contains("^Unnamed")]
        
        self.check_format()
        if self.scale_format == "nominal" or self.scale_format == "ordinal":
            self.find_categories()
        self.find_rater_ids()
        self.find_text()
        self.find_labels()

        if self.debug:
            print("Format:")
            print(self.format)
            print("Scale Format:")
            print(self.scale_format)
            print("Categories:")
            print(self.categories)
            print("Rater ID's:")
            print(self.rater_ids)
            print()

            print("Text:")
            print(self.text)
            print()

            print("Formatted Text")
            print(self.formatted_text)
            print()

            print("Labels")
            print(self.labels)
            print()
        
    def check_format(self):
        """Checks the format of the file content based on its headers.
        
        This method inspects the headers of the file content to determine its format.
        If a header matches 'Rater ID', it sets the format to 'Format 1'. If a header
        matches 'Subject', it sets the format to 'Format 2'. If neither header is found,
        it raises a ValueError.
        
        :raises ValueError: If the file format cannot be determined based on headers.
        """
        headers = list(self.content.columns)

        for header in headers:
            header = header.lower()
            if header == "Rater ID".lower():
                self.format = "Format 1"
                return
            
            if header == "Subject".lower():
                self.format = "Format 2"
                return
        
        raise ValueError
        

    def find_categories(self):
        """Identifies and extracts categories from the file content.
        
        This method processes the file content to find and store unique categories
        in the `categories` attribute. It skips any null values encountered.
        
        :returns: None
        """
        for item in self.content["Categories"]:
            if not pd.isnull(item):
                self.categories.append(item)

    def find_rater_ids(self):
        """Identifies and extracts rater IDs from the file content based on the file format.
        
        This method processes the file content to find and store unique rater IDs in the
        `rater_ids` attribute. The extraction logic varies depending on whether the file
        format is 'Format 1' or 'Format 2', and further depends on the scale format for
        'Format 2'.
        
        :raises ValueError: If the file format is not recognized.
        """
        if self.format == "Format 1":
            for item in self.content["Rater ID"]:
                if not pd.isnull(item):
                    if item not in self.rater_ids:
                        self.rater_ids.append(item)
        elif self.format == "Format 2":
            if self.scale_format == "nominal" or self.scale_format == "ordinal":
                for header in self.content:
                    if all(self.content[header].isin(self.categories) | self.content[header].isnull()):
                        if header not in self.rater_ids:
                            self.rater_ids.append(header)
            else: 
                for header in self.content:
                    if header == "Subject":
                        continue
                    if header not in self.rater_ids:
                        self.rater_ids.append(header)

        
    def find_text(self):
        """Processes and extracts text from the file content based on the file format.
        
        This method identifies and processes text from the file content, storing it
        in the `text` and `formatted_text` attributes. The processing differs
        depending on whether the file format is 'Format 1' or 'Format 2'.
        
        :raises ValueError: If the file format is not recognized.
        """
        if self.format == "Format 1":
            if self.scale_format == "nominal" or self.scale_format == "ordinal":
                for header in self.content:

                    if self.debug:
                        print("header: " + str(header))

                    if all(self.content[header].isin(self.categories) | self.content[header].isnull()):
                        if header not in self.rater_ids:
                            if "Categories" == header:
                                continue
                            self.formatted_text.append(self.nlp(header))
                            self.text.append(header)
            else:
                for header in self.content:
                    if header == "Rater ID":
                        continue
                    self.formatted_text.append(self.nlp(header))
                    self.text.append(header)

        elif self.format == "Format 2":
            for item in self.content["Subject"]:
                if not pd.isnull(item):
                    self.formatted_text.append(self.nlp(item))
                    self.text.append(item)

    def find_labels(self):
        """Processes and extracts labels from the file content based on the file format.
        
        This method identifies and processes labels from the file content, storing them
        in the `labels` attribute. The processing differs depending on whether the file
        format is 'Format 1' or 'Format 2'.
        
        :raises ValueError: If the file format is not recognized.
        """
        if self.format == "Format 1":
            for row in range(len(self.content)):
                if pd.isnull(self.content.loc[row, "Rater ID"]):
                    continue

                text_label_list = []

                for i, text in enumerate(self.text):
                    text_label_list.append((self.formatted_text[i], self.content.loc[row, text]))

                if self.content.loc[row, "Rater ID"] in self.labels:
                    self.labels[self.content.loc[row, "Rater ID"]] += text_label_list
                else:
                    self.labels[self.content.loc[row, "Rater ID"]] = text_label_list
        elif self.format == "Format 2":
            for rater_id in self.rater_ids:
                text_label_list = []
                for row in range(len(self.content)):
                    if pd.isnull(self.content.loc[row, "Subject"]):
                        continue

                    text_label_list.append((self.content.loc[row, "Subject"], self.content.loc[row, rater_id]))

                if rater_id in self.labels:
                    self.labels[rater_id] += text_label_list
                else:
                    self.labels[rater_id] = text_label_list

    def write_file(self, path, ratings):
        """Writes the ratings data to a specified file.
        
        This method processes the ratings data, merges it with existing content, and
        writes the combined data to a file in the specified format (Excel, ODS, or CSV).
        
        :param path: The file path where the data will be written.
        :type path: str
        :param ratings: A list of ratings to be written to the file.
        :type ratings: list of tuples
        :returns: None
        """
        if self.scale_format == "nominal" or self.scale_format == "ordinal":
            columns = ["Categories", "Rater ID"]
        else:
            columns = ["Rater ID"]
        users = []
        col_rename = {}

        if self.format == "Format 1":
            for txt in self.text:
                columns.append(txt)
                col_rename[txt] = self.nlp(txt)
        else:
            pass

        for rating in ratings:
            if rating == ():
                continue
            if rating[PROFILE] not in users:
                users.append(rating[PROFILE])

        old_df = pd.DataFrame(self.content, columns=columns)
        old_df = old_df.rename(columns=col_rename)

        if self.debug:
            print("old df")
            print(old_df)
            print()

        if self.scale_format == "nominal" or self.scale_format == "ordinal":
            columns = ["Categories", "Rater ID"]
        else:
            columns = ["Rater ID"]
        for txt in self.formatted_text:
            columns.append(txt)
        new_df = pd.DataFrame([], columns=columns)

        for user in users:
            if self.scale_format == "nominal" or self.scale_format == "ordinal": 
                row = [np.nan, self.usr_to_id(user)]
            else:
                row = [self.usr_to_id(user)]
            for rating in ratings:
                if rating == ():
                    row.append(np.nan)
                elif rating[PROFILE] == user:
                    row.append(rating[RATING])
                else:
                    row.append(np.nan)
            new_df.loc[len(new_df)] = row

        df = pd.concat([old_df, new_df], axis="index")
        df = df.reset_index(drop=True)

        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # Without milliseconds

        date_col = []
        for i in range(len(old_df)):
            date_col.append(np.nan)
        for i in range(len(new_df)):
            date_col.append(current_datetime)
        date_df = pd.DataFrame({"datum_ir_app": date_col})

        df = pd.concat([df, date_df], axis="columns")

        file_extension = pathlib.Path(path).suffix
        if file_extension == ".xlsx" or file_extension == ".xls":
            df.to_excel(path, index = False, header=True)
        elif file_extension == ".ods":
            df.to_excel(path, engine="odf", index = False, header=True)
        else:
            df.to_csv(path, sep=";", index = False, header=True)

    def usr_to_id(self, user):
        """Generates a unique identifier for a user.
        
        :param user: The username to be converted.
        :type user: str
        :returns: A unique identifier string prefixed with 'ir_app_'.
        :rtype: str
        """
        return "ir_app_" + user

    def nlp(self, text):
        """Processes the input text for NLP tasks.
        
        This method performs specific text processing steps, including extracting
        the longest substring within square brackets if a specific metadata string
        is present, and removing trailing decimal points.
        
        :param text: The input text to be processed.
        :type text: str
        :returns: The processed text.
        :rtype: str
        """
        sentisurvey_metadata = "How would you label the following sentences regarding its polarity? Rate the sentences as positive, negative or neutral (neither positive nor negative) based on your perception."
        if sentisurvey_metadata in text:
            text = max(re.findall(re.escape("[")+"(.*?)"+re.escape("]"),text), key=len)

        text = re.sub("\.[0-9]*$", "", text)

        return text


class DBInteraction():
    """A class to handle database interactions, including loading, creating, deleting,
    and changing profiles, and writing profile data to a CSV file.
    """
    def __init__(self, db_path):
        """Initializes the DBInteraction class.
        
        This constructor initializes the DBInteraction class by setting up the database
        path, reading the database file, and loading profiles. It supports Excel files
        with extensions '.xlsx' and '.xls', OpenDocument Spreadsheet files with the
        extension '.ods', and CSV files. The profiles are then loaded from the database.
        
        :param db_path: The file path to the database.
        :type db_path: str
        :raises ValueError: If the file extension is not supported.
        """
        file_extension = pathlib.Path(db_path).suffix
        self.db_path = db_path
        self.db = None 

        self.active_profile = ""
        self.profiles = []

        if file_extension == ".xlsx" or file_extension == ".xls":
            self.db = pd.read_excel(db_path)
        elif file_extension == ".ods":
            self.db = pd.read_excel(db_path, engine="odf")
        else:
            self.db = pd.read_csv(db_path, delimiter=";") 
        
        self.load_profiles()

    def load_profiles(self):
        """Loads profiles from the database.
        
        This method checks if there are any profiles in the database. If a profile
        exists, it sets the first profile as the active profile and stores the
        remaining profiles in a list.
        
        :returns: None
        """
        if len(self.db["Profile"]) > 0:
            if not pd.isnull(self.db["Profile"][0]):
                self.active_profile = self.db["Profile"][0]
                self.profiles = list(self.db["Profile"][1:])
        else:
            return
    
    def create_profile(self, new_profile):
        """Creates a new profile and updates the database.
        
        If there is an active profile, it is added to the profiles list before
        setting the new profile as active. The changes are then written to the
        database.
        
        :param new_profile: The new profile to be set as active.
        """
        if self.active_profile != "":
            self.profiles.append(self.active_profile)
        self.active_profile = new_profile

        self.write_to_db()

    
    def delete_profile(self):
        """Deletes the active profile from the database.
        
        This method sets the active profile to the first profile in the list of
        profiles, removes it from the list, and writes the changes to the database.
        
        :raises IndexError: If the profiles list is empty.
        """
        self.active_profile = self.profiles[0]
        self.profiles.remove(self.active_profile)

        self.write_to_db()

    def change_profile(self, change_to):
        """Changes the active profile to a specified profile.
        
        This method swaps the current active profile with the profile specified by
        the `change_to` parameter. The current active profile is then added to the
        list of profiles, and the specified profile is removed from it. Finally,
        the changes are written to the database.
        
        :param change_to: The profile to switch to.
        :raises ValueError: If the specified profile is not in the list of profiles.
        """
        tmp = self.active_profile
        self.active_profile = change_to
        self.profiles.remove(change_to)
        self.profiles.append(tmp)

        self.write_to_db()

    def write_to_db(self):
        """Writes the current active profile and other profiles to a CSV file.
        
        This method creates a DataFrame from the active profile and the list of
        other profiles, then writes it to the specified CSV file path.
        
        :raises IOError: If there is an issue writing to the CSV file.
        """
        self.db = pd.DataFrame([self.active_profile] + self.profiles, columns=["Profile"])
        self.db.to_csv(self.db_path, sep=";", index = False, header=True)


def write_excel(analyse, intra_ids, intra_metrics, inter_ids, inter_metrics, scale_format, filename):
    """Writes analysis results to an Excel file.
    
    :param analyse: Analysis object containing the results.
    :param intra_ids: List of intra-rater IDs.
    :param intra_metrics: List of intra-rater metrics.
    :param inter_ids: List of inter-rater IDs.
    :param inter_metrics: List of inter-rater metrics.
    :param scale_format: Scale format, either 'nominal' or 'ordinal'.
    :param filename: Name of the output Excel file.
    :raises ZeroDivisionError: If a division by zero occurs during metric calculation.
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    b_cell_format = workbook.add_format()
    b_cell_format.set_bold()

    not_enough_ratings = []
    
    if scale_format == "nominal" or scale_format == "ordinal":
        if intra_ids and intra_metrics:
            worksheet.write(0, 0, "Intra-Rater-Analyse", b_cell_format)
            worksheet.write(1, 0, "")
            worksheet.write(2, 0, "Gewichte", b_cell_format)
            worksheet.write(3, 0, analyse.results["intra"][intra_ids[0]].weights_name)
            worksheet.write(4, 0, "")
            worksheet.write(5, 0, "")
            worksheet.write(6, 0, "Rater ID", b_cell_format)
            worksheet.write(6, 1, "#Subjects", b_cell_format)
            worksheet.write(6, 2, "#Replicates", b_cell_format)
            j = 3
            for metric in intra_metrics:
                worksheet.write(6, j, metric, b_cell_format)
                j += 1
            i = 7
            for rater_id in intra_ids:
                quant_subjects = analyse.results["intra"][rater_id].n
                quant_replicates = analyse.results["intra"][rater_id].r
                if quant_replicates < 2 or quant_subjects < 1:
                    not_enough_ratings.append(str(rater_id))
                    continue

                worksheet.write(i, 0, rater_id)
                worksheet.write(i, 1, quant_subjects)
                worksheet.write(i, 2, quant_replicates)

                j = 3
                cont = False
                for metric in intra_metrics:
                    metric_function_name = map_metrics(metric)

                    try:
                        metric_dict = getattr(analyse.results["intra"][rater_id], metric_function_name)()["est"]
                        metric_value = metric_dict["coefficient_value"]

                        if isnan(metric_value) and metric == "Cohen's-|Conger's \u03BA":
                            metric_value = 1.0
                                
                        worksheet.write(i, j, str(metric_value))
                    except ZeroDivisionError:
                        worksheet.write(i, j, "1.0")
                    j += 1
                if cont:
                    continue
                i += 1
            worksheet.write(i, 0, "")
            worksheet.write(i + 1, 0, "")
            i += 2
            # Original
            #i = 6
            for rater_id in intra_ids:
                quant_subjects = analyse.results["intra"][rater_id].n
                quant_replicates = analyse.results["intra"][rater_id].r

                if quant_replicates < 2 or quant_subjects < 1:
                    continue

                worksheet.write(i, 0, "Rater ID", b_cell_format)
                worksheet.write(i+1, 0, rater_id)

                worksheet.write(i, 1, "#Subjects", b_cell_format)
                worksheet.write(i+1, 1, quant_subjects)

                worksheet.write(i, 2, "#Replikate", b_cell_format)
                worksheet.write(i+1, 2, quant_replicates)

                worksheet.write(i+2, 0, "")

                i = i +3
                for metric in intra_metrics:
                    metric_function_name = map_metrics(metric)

                    try:
                        metric_dict = getattr(analyse.results["intra"][rater_id], metric_function_name)()["est"]

                        worksheet.write(i, 0, metric, b_cell_format)
                        worksheet.write(i+1, 0, str(metric_dict["coefficient_value"]))

                        worksheet.write(i, 1, "p-Wert", b_cell_format)
                        worksheet.write(i+1, 1, str(metric_dict["p_value"]))

                        worksheet.write(i, 2, "95% Konfidenzintervall", b_cell_format)
                        worksheet.write(i+1, 2, str(metric_dict["confidence_interval"]))

                        worksheet.write(i+2, 0, "")
                    except ZeroDivisionError:
                        worksheet.write(i, 0, metric, b_cell_format)
                        worksheet.write(i+1, 0, "1.0")

                        worksheet.write(i, 1, "p-Wert", b_cell_format)
                        worksheet.write(i+1, 1, "n.a.")

                        worksheet.write(i, 2, "95% Konfidenzintervall", b_cell_format)
                        worksheet.write(i+1, 2, "(n.a., n.a.)")

                        worksheet.write(i+2, 0, "")
                    i = i +3
            worksheet.write(i, 0, "")
            worksheet.write(i+1, 0, "")
            worksheet.write(i+2, 0, "")
            worksheet.write(i+3, 0, "ID's, die kein Subject mehrfach bewertet haben:")
            i = i + 4
            for id in not_enough_ratings:
                worksheet.write(i, 0, id)
                i += 1

        else:
            i = 0

        if inter_ids and inter_metrics:
            quant_subjects = analyse.results["inter"].n
            quant_raters = analyse.results["inter"].r
            worksheet.write(i, 0, "Inter-Rater-Analyse", b_cell_format)
            worksheet.write(i+1, 0, "")
            worksheet.write(i+2, 0, "Gewichte", b_cell_format)
            worksheet.write(i+3, 0, analyse.results["inter"].weights_name)
            worksheet.write(i+4, 0, "")
            worksheet.write(i+5, 0, "Rater ID's", b_cell_format)
            worksheet.write(i+5, 1, "#Subjects", b_cell_format)
            worksheet.write(i+5, 2, "#Raters", b_cell_format)
            worksheet.write(i+6, 1, str(quant_subjects))
            worksheet.write(i+6, 2, str(quant_raters))
            i = i + 6
            for rater_id in inter_ids:
                worksheet.write(i, 0, rater_id)
                i = i + 1
            worksheet.write(i, 0, "")
            i = i + 1
            for metric in inter_metrics:
                metric_function_name = map_metrics(metric)
                metric_dict = getattr(analyse.results["inter"], metric_function_name)()["est"]

                worksheet.write(i, 0, metric, b_cell_format)
                worksheet.write(i+1, 0, str(metric_dict["coefficient_value"]))

                worksheet.write(i, 1, "p-Wert", b_cell_format)
                worksheet.write(i+1, 1, str(metric_dict["p_value"]))

                worksheet.write(i, 2, "95% Konfidenzintervall", b_cell_format)
                worksheet.write(i+1, 2, str(metric_dict["confidence_interval"]))

                worksheet.write(i+2, 0, "")
                i = i + 3
                

    workbook.close()


























