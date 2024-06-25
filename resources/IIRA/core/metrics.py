import irrCAC as ir
from irrCAC.raw import CAC
import pingouin as pg
import pandas as pd
import numpy as np
import decimal as dec
import math
FIRST_REPLIACTE = 0
SECOND_REPLICATE = 1

class Metrics:
    """    A class to compute various inter-rater reliability metrics based on the given scale format, categories, ratings, and weights.

    Attributes:
        scale_format (str): The format of the scale, either 'ordinal' or 'nominal'.
        categories (list): The list of categories for the ratings.
        ratings (pd.DataFrame): The DataFrame containing the ratings.
        quantity_subjects (int): The number of subjects being rated.
        replications (int): The number of replications per subject.
        weights (list): The list of weights for the ratings.
        analysis (CAC or pd.DataFrame): The analysis object for computing the metrics.
        debug (bool): A flag for enabling debug mode.

    Methods:
        __init__(self, scale_format, categories, ratings, weights): Initializes the Metrics object with the given parameters.
        cohens_kappa(self): Computes Cohen's Kappa metric.
        fleiss_kappa(self): Computes Fleiss' Kappa metric.
        gwets_ac(self): Computes Gwet's AC metric.
        krippendorfs_alpha(self): Computes Krippendorff's Alpha metric.
        g_index(self): Computes the G index metric.
        icc(self): Computes the Intraclass Correlation Coefficient (ICC).
        overall_agreement(self): Computes the overall agreement among the ratings."""

    def __init__(self, scale_format, categories, ratings, weights):
        """    Initializes the Metrics object with the given parameters.

    Args:
        scale_format (str): The format of the scale, either 'ordinal' or 'nominal'.
        categories (list): The list of categories for the ratings.
        ratings (pd.DataFrame): The DataFrame containing the ratings.
        weights (list): The list of weights for the ratings.

    Raises:
        Exception: If there is an error in creating the irrCAC or pingouin analysis."""
        self.debug = False
        self.scale_format = scale_format
        self.categories = categories
        self.ratings = ratings
        self.quantity_subjects = len(self.ratings)
        self.replications = 2
        self.weights = weights
        self.analysis = None
        if scale_format == 'ordinal' or scale_format == 'nominal':
            try:
                self.analysis = CAC(ratings=self.ratings, weights=self.weights, categories=self.categories, digits=4)
            except Exception as e:
                print('Exception creating irrCAC analysis: ' + str(e))
        else:
            try:
                self.analysis = self.icc()
            except Exception as e:
                print('Exception creating pingouin analysis: ' + str(e))
        dec.setcontext(dec.Context(prec=34))
        if self.debug:
            print('Ratings')
            print('len(ratings): ' + str(len(self.ratings)))
            print('len(ratings.columns): ' + str(len(self.ratings.columns)))
            print(self.ratings)
            print()
            print('Analyse')
            print(self.analysis)
            print()
            if self.scale_format == 'ordinal' or self.scale_format == 'nominal':
                print("Cohen's Kappa")
                print(self.analysis.conger())
                print()
                print('Fleiss Kappa')
                print(self.analysis.fleiss())
                print()
                print("Gwet's AC")
                print(self.analysis.gwet())
                print()
                print("Krippendorff's Alpha")
                print(self.analysis.krippendorff())
                print()

    def cohens_kappa(self):
        """    Computes Cohen's Kappa metric.

    Returns:
        float: The computed Cohen's Kappa value."""
        return self.analysis.conger()['est']['coefficient_value']

    def fleiss_kappa(self):
        """
        """
        return self.analysis.fleiss()['est']['coefficient_value']

    def gwets_ac(self):
        """
        """
        return self.analysis.gwet()['est']['coefficient_value']

    def krippendorfs_alpha(self):
        """    Computes Krippendorff's Alpha metric.

    Returns:
        float: The computed Krippendorff's Alpha value."""
        return self.analysis.krippendorff()['est']['coefficient_value']

    def g_index(self):
        """    Computes the G index metric.

    Returns:
        float: The computed G index value."""
        q = len(self.categories)
        p_a = self.overall_agreement()
        g_index = (p_a - dec.Decimal('1') / q) / (dec.Decimal('1') - dec.Decimal('1') / q)
        return float(round(g_index, 4))

    def icc(self):
        """    Computes the Intraclass Correlation Coefficient (ICC).

    Returns:
        pd.DataFrame: The DataFrame containing the ICC values."""
        pg_targets = []
        pg_raters = []
        pg_ratings = []
        for i in range(len(self.ratings.columns)):
            for j in range(len(self.ratings)):
                pg_targets.append(j)
                pg_raters.append(self.ratings.columns[i])
            pg_ratings += list(self.ratings[self.ratings.columns[i]])
        df = pd.DataFrame({'pg_targets': pg_targets, 'pg_raters': pg_raters, 'pg_ratings': pg_ratings})
        if self.debug:
            print('pg_targets')
            print(pg_targets)
            print()
            print('pg_raters')
            print(pg_raters)
            print()
            print('pg_ratings')
            print(pg_ratings)
            print()
        icc = pg.intraclass_corr(data=df, targets='pg_targets', raters='pg_raters', ratings='pg_ratings', nan_policy='omit').round(4)
        return icc

    def overall_agreement(self):
        """    Computes the overall agreement among the ratings.

    Returns:
        decimal.Decimal: The computed overall agreement value.

    Raises:
        ValueError: If there are not enough replications per subject to calculate an overall agreement."""
        q = len(self.categories)
        p_a = dec.Decimal('0')
        if self.replications == 2:
            for k in range(q):
                current_cat = self.categories[k]
                subject_kk = dec.Decimal('0')
                for subject in self.ratings:
                    if self.ratings[subject][FIRST_REPLIACTE] == current_cat and self.ratings[subject][FIRST_REPLIACTE] == self.ratings[subject][SECOND_REPLICATE]:
                        subject_kk += dec.Decimal('1')
                p_kk = subject_kk
                p_a += p_kk / self.quantity_subjects
            return p_a
        elif self.replications > 2:
            m = self.quantity_subjects
            n = self.replications
            for i in self.ratings:
                for k in range(q):
                    n_i_k = dec.Decimal('0')
                    for replicate_label in self.ratings[i]:
                        if replicate_label == self.categories[k]:
                            n_i_k += dec.Decimal('1')
                    p_a += n_i_k * (n_i_k - 1) / (n * (n - 1))
            return p_a / m
        else:
            raise ValueError('Not enough replications per subject to calculate an overall agreement.')

def map_metrics(metric):
    """    Maps the given metric name to its corresponding method name.

    Args:
        metric (str): The name of the metric to map.

    Returns:
        str: The corresponding method name for the given metric."""
    if metric == "Cohen's-|Conger's κ":
        return 'conger'
    elif metric == "Fleiss' κ":
        return 'fleiss'
    elif metric == "Krippendorff's α":
        return 'krippendorff'
    elif metric == "Gwet's AC":
        return 'gwet'