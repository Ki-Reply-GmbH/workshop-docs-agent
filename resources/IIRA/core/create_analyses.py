from math import nan, isnan
from core.metrics import Metrics
from pprint import pprint
import pandas as pd
import numpy as np
TEXT = 0
LABEL = 1
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class CreateAnalyses:
    """    This class is responsible for creating intra-rater and inter-rater analyses based on the provided data and metrics.

    Attributes:
        intra_id_list (list): List of IDs for intra-rater analysis.
        inter_id_list (list): List of IDs for inter-rater analysis.
        intra_metrics (list): List of metrics for intra-rater analysis.
        inter_metrics (list): List of metrics for inter-rater analysis.
        scale_format (str): The scale format used in the analysis.
        categories (list): List of categories used in the analysis.
        weights (list): List of weights used in the analysis.
        data (dict): The data used for analysis, structured similarly to the labels format in the FileValidation class.
        results (dict): Dictionary to store the results of intra and inter analyses.
        debug (bool): Flag to enable or disable debug mode."""

    def __init__(self, intra_id_list, inter_id_list, intra_metrics, inter_metrics, scale_format, categories, weights, data):
        """    Initializes the CreateAnalyses class with the provided parameters and triggers the intra and inter analyses if the corresponding IDs and metrics are provided.

    Args:
        intra_id_list (list): List of IDs for intra-rater analysis.
        inter_id_list (list): List of IDs for inter-rater analysis.
        intra_metrics (list): List of metrics for intra-rater analysis.
        inter_metrics (list): List of metrics for inter-rater analysis.
        scale_format (str): The scale format used in the analysis.
        categories (list): List of categories used in the analysis.
        weights (list): List of weights used in the analysis.
        data (dict): The data used for analysis, structured similarly to the labels format in the FileValidation class."""
        self.debug = True
        self.intra_id_list = intra_id_list
        self.inter_id_list = inter_id_list
        self.intra_metrics = intra_metrics
        self.inter_metrics = inter_metrics
        self.scale_format = scale_format
        self.categories = categories
        self.weights = weights
        self.data = data
        self.results = {'intra': {}, 'inter': {}}
        if self.intra_id_list and self.intra_metrics:
            if self.debug:
                print('Enter intra analysis')
            self.create_intra_analyses()
        if self.inter_id_list and self.inter_metrics:
            if self.debug:
                print('Enter inter analysis')
            self.create_inter_analyses()
        if self.debug:
            print("Intra ID's:")
            print(self.intra_id_list)
            print('Intra Metrics:')
            print(self.intra_metrics)
            print()
            print("Inter ID's:")
            print(self.inter_id_list)
            print('Inter Metrics:')
            print(self.inter_metrics)
            print()
            print('Skalenformat')
            print(self.scale_format)
            print()
            print('Kategorien')
            print(self.categories)
            print()
            print('Gewichte')
            print(self.weights)
            print()
            print('Daten')
            print(self.data)
            print()
            print('Results')
            print(self.results)
            print()

    def create_intra_analyses(self):
        """    Creates intra-rater analyses for each ID in the intra_id_list by finding the corresponding ratings and performing calculations using the Metrics class.

    This method updates the 'results' attribute with the intra-rater analysis results."""
        for id in self.intra_id_list:
            self.results['intra'][id] = {}
            ratings = self.find_intra_ratings(id)
            if self.debug:
                print('Intra Ratings for ID ' + str(id) + ':')
                print(ratings)
                print()
            calculations = Metrics(self.scale_format, self.categories, ratings, self.weights)
            self.results['intra'][id] = calculations.analysis
            if self.debug:
                print('Intra Analyse for ID ' + str(id) + ':')
                print(self.results['intra'][id])
                print()

    def create_inter_analyses(self):
        """    Creates inter-rater analyses by finding the corresponding ratings and performing calculations using the Metrics class.

    This method updates the 'results' attribute with the inter-rater analysis results."""
        ratings = self.find_inter_ratings()
        if self.debug:
            print('Inter Ratings:')
            print(ratings)
            print()
        calculations = Metrics(self.scale_format, self.categories, ratings, self.weights)
        self.results['inter'] = calculations.analysis

    def find_intra_ratings(self, id):
        """    Finds and returns the intra-rater ratings for a given ID.

    Args:
        id (int): The ID for which to find the intra-rater ratings.

    Returns:
        pd.DataFrame: A DataFrame containing the intra-rater ratings, with subjects as the index and their corresponding ratings as the values."""
        ret = {}
        for rating in self.data[id]:
            if not isinstance(rating[LABEL], str) or rating[LABEL] == '':
                continue
            if rating[TEXT] in ret:
                ret[rating[TEXT]].append(rating[LABEL])
            else:
                ret[rating[TEXT]] = [rating[LABEL]]
        if self.debug:
            ret_rmv = {k: v for k, v in ret.items() if len(v) >= 2}
        return pd.DataFrame.from_dict(ret_rmv, orient='index')

    def find_inter_ratings(self):
        """    Finds and returns the inter-rater ratings for the IDs in the inter_id_list.

    Returns:
        pd.DataFrame: A DataFrame containing the inter-rater ratings, with subjects as the index and their corresponding ratings as the values."""
        ret = {}
        for i, id in enumerate(self.inter_id_list):
            for rating in self.data[id]:
                if rating[TEXT] in ret:
                    if len(ret[rating[TEXT]]) > i:
                        continue
                    ret[rating[TEXT]].append(rating[LABEL])
                else:
                    ret[rating[TEXT]] = [rating[LABEL]]
        return pd.DataFrame.from_dict(ret, orient='index')