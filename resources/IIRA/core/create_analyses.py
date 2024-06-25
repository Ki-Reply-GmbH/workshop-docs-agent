from math import nan, isnan
from core.metrics import Metrics
from pprint import pprint
import pandas as pd
import numpy as np

TEXT = 0
LABEL = 1

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

class CreateAnalyses():
    """A class to perform intra-rater and inter-rater analyses on provided data.
    """
    def __init__(self, intra_id_list, inter_id_list, intra_metrics, inter_metrics, scale_format, categories, weights, data):
        # Daten, die von der Klasse f�r die Analyse gebraucht werden
        """Initializes the CreateAnalyses class with provided parameters and performs
        initial analyses.
        
        This constructor sets up the initial state of the CreateAnalyses object by
        storing the provided parameters into instance variables. It then initializes
        an empty results dictionary for intra-rater and inter-rater analyses. If
        intra-rater IDs and metrics are provided, it triggers the intra-rater analysis.
        Similarly, if inter-rater IDs and metrics are provided, it triggers the
        inter-rater analysis. If debugging is enabled, it prints the initial state
        and parameters.
        
        :param intra_id_list: List of IDs for intra-rater analysis.
        :type intra_id_list: list
        :param inter_id_list: List of IDs for inter-rater analysis.
        :type inter_id_list: list
        :param intra_metrics: Metrics to be used for intra-rater analysis.
        :type intra_metrics: list
        :param inter_metrics: Metrics to be used for inter-rater analysis.
        :type inter_metrics: list
        :param scale_format: Format of the scale used in the analysis.
        :type scale_format: str
        :param categories: Categories used in the analysis.
        :type categories: list
        :param weights: Weights applied in the analysis.
        :type weights: list
        :param data: Data to be analyzed, formatted as in the FileValidation class.
        :type data: dict
        :returns: None
        """
        self.debug = True
        self.intra_id_list = intra_id_list
        self.inter_id_list = inter_id_list
        self.intra_metrics = intra_metrics
        self.inter_metrics = inter_metrics
        self.scale_format = scale_format
        self.categories = categories
        self.weights = weights
        self.data = data                            # Format entspricht dem labels-Format in der FileValidation-Klasse

        self.results = {
            "intra": {},
            "inter": {}
        }
        if self.intra_id_list and self.intra_metrics:
            if self.debug:
                print("Enter intra analysis")
            self.create_intra_analyses()

        if self.inter_id_list and self.inter_metrics:
            if self.debug:
                print("Enter inter analysis")
            self.create_inter_analyses()

        if self.debug:
            print("Intra ID's:")
            print(self.intra_id_list)
            print("Intra Metrics:")
            print(self.intra_metrics)
            print()

            print("Inter ID's:")
            print(self.inter_id_list)
            print("Inter Metrics:")
            print(self.inter_metrics)
            print()

            print("Skalenformat")
            print(self.scale_format)
            print()

            print("Kategorien")
            print(self.categories)
            print()

            print("Gewichte")
            print(self.weights)
            print()

            print("Daten")
            print(self.data)
            print()

            print("Results")
            print(self.results)
            print()


    def create_intra_analyses(self):
        """Generates intra-rater analysis results and stores them in the results dictionary.
        
        This method iterates over the list of intra-rater IDs, finds intra-rater ratings,
        performs calculations using the Metrics class, and stores the analysis results
        in the 'intra' key of the results dictionary. If debugging is enabled, it prints
        the intermediate ratings and results.
        
        :returns: None
        """
        for id in self.intra_id_list:
            self.results["intra"][id] = {}

            ratings = self.find_intra_ratings(id)

            if self.debug:
                print("Intra Ratings for ID " + str(id)+ ":")
                print(ratings)
                print()

            calculations = Metrics(self.scale_format, self.categories, ratings, self.weights)
            self.results["intra"][id] = calculations.analysis

            if self.debug:
                print("Intra Analyse for ID " + str(id)+ ":")
                print(self.results["intra"][id])
                print()

    def create_inter_analyses(self):
        """Generates inter-rater analysis results and stores them in the results dictionary.
        
        This method finds inter-rater ratings, performs calculations using the Metrics
        class, and stores the analysis results in the 'inter' key of the results
        dictionary. If debugging is enabled, it prints the intermediate ratings and
        results.
        
        :returns: None
        """
        ratings = self.find_inter_ratings()
        if self.debug:
            print("Inter Ratings:")
            print(ratings)
            print()
        
        calculations = Metrics(self.scale_format, self.categories, ratings, self.weights)
        self.results["inter"] = calculations.analysis

    def find_intra_ratings(self, id):
        """Finds and aggregates intra-rater ratings for a given ID.
        
        Iterates over the ratings for the specified ID and collects ratings for each
        text subject. If a text subject already exists in the result dictionary, it
        appends the new rating label to the list. Otherwise, it creates a new entry
        for the text subject with the rating label. Optionally filters out text
        subjects that have been rated less than twice.
        
        :param id: The identifier for which intra-rater ratings are to be found.
        :type id: int
        :returns: DataFrame where each row represents a text subject and columns
        represent ratings from the same rater.
        :rtype: pandas.DataFrame
        """
        ret = {}
        for rating in self.data[id]:
            if not isinstance(rating[LABEL], str) or rating[LABEL] == "":
                # Nullwerte �berspringen
                continue
            if rating[TEXT] in ret:
                # Falls das Subject rating[TEXT] schon im dictionary vorhanden ist, f�ge
                # das Label vom Repilkat hinzu.
                ret[rating[TEXT]].append(rating[LABEL])
            else:
                # Andernfalls f�ge das erste Label hinzu
                ret[rating[TEXT]] = [rating[LABEL]]
        if self.debug:
            # Keys entfernen, die nur einmal bewertet worden sind. Die sind nicht relevant f�r intrarater.
            ret_rmv = {k: v for k, v in ret.items() if len(v) >= 2}
        return pd.DataFrame.from_dict(ret_rmv, orient="index")


    def find_inter_ratings(self):
        """
```
Finds and aggregates inter-rater ratings from the provided data.

Iterates over the list of inter-rater IDs and collects ratings for each text 
subject. If a text subject already exists in the result dictionary, it appends 
the new rating label to the list. Otherwise, it creates a new entry for the 
text subject with the rating label.

:returns: DataFrame where each row represents a text subject and columns 
          represent ratings from different raters.
:rtype: pandas.DataFrame
```
"""
        ret = {}
        for i, id in enumerate(self.inter_id_list):
            for rating in self.data[id]:
                if rating[TEXT] in ret:
                    # Duplikate �berspringen; sind nur f�r Intra-Rater-Analyse relevant
                    if len(ret[rating[TEXT]]) > i:
                        continue

                    # Falls das Subject rating[TEXT] schon im dictionary vorhanden ist, f�ge
                    # das Label vom Repilkat hinzu.
                    ret[rating[TEXT]].append(rating[LABEL])
                else:
                    # Andernfalls f�ge das erste Label hinzu
                    ret[rating[TEXT]] = [rating[LABEL]]

        return pd.DataFrame.from_dict(ret, orient="index")                







