import irrCAC as ir
from irrCAC.raw import CAC 
import pingouin as pg
import pandas as pd
import numpy as np

import decimal as dec
import math

FIRST_REPLIACTE = 0
SECOND_REPLICATE = 1


class Metrics():
    def __init__(self, scale_format, categories, ratings, weights):
        self.debug = False
        self.scale_format = scale_format
        self.categories = categories
        self.ratings = ratings
        self.quantity_subjects = len(self.ratings)
        self.replications = 2

        self.weights = weights
        self.analysis = None

        if scale_format == "ordinal" or scale_format == "nominal":
            try:
                self.analysis = CAC(ratings=self.ratings, weights=self.weights, categories=self.categories, digits=4)
            except Exception as e:
                print("Exception creating irrCAC analysis: " + str(e))
        else:
            try:
                self.analysis = self.icc()
            except Exception as e:
                print("Exception creating pingouin analysis: " + str(e))

        dec.setcontext(dec.Context(prec=34))

        if self.debug:
            print("Ratings")
            print("len(ratings): " + str(len(self.ratings)))
            print("len(ratings.columns): " + str(len(self.ratings.columns)))
            print(self.ratings)
            print()

            print("Analyse")
            print(self.analysis)
            print()

            if self.scale_format == "ordinal" or self.scale_format == "nominal":
                print("Cohen's Kappa")
                print(self.analysis.conger())
                print()

                print("Fleiss Kappa")
                print(self.analysis.fleiss())
                print()

                print("Gwet's AC")
                print(self.analysis.gwet())
                print()

                print("Krippendorff's Alpha")
                print(self.analysis.krippendorff())
                print()



    def cohens_kappa(self):
        return self.analysis.conger()["est"]["coefficient_value"]

    def fleiss_kappa(self):
        """
        """
        return self.analysis.fleiss()["est"]["coefficient_value"]

    def gwets_ac(self):
        """
        """
        return self.analysis.gwet()["est"]["coefficient_value"]


    def krippendorfs_alpha(self):
        return self.analysis.krippendorff()["est"]["coefficient_value"]

    def g_index(self):
        #TODO Vorraussetzungen checken
        q = len(self.categories)
        p_a = self.overall_agreement()

        g_index = (p_a - (dec.Decimal("1") / q)) / (dec.Decimal("1") - (dec.Decimal("1") / q))

        return float(round(g_index, 4))

    def icc(self):
        pg_targets = []
        pg_raters = []
        pg_ratings = []
        for i in range(len(self.ratings.columns)):
            for j in range(len(self.ratings)):
                pg_targets.append(j)
                pg_raters.append(self.ratings.columns[i])
            pg_ratings += list(self.ratings[self.ratings.columns[i]])

        df = pd.DataFrame({'pg_targets': pg_targets,
                        'pg_raters': pg_raters,
                        'pg_ratings': pg_ratings})

        if self.debug:
            print("pg_targets")
            print(pg_targets)
            print()
            print("pg_raters")
            print(pg_raters)
            print()
            print("pg_ratings")
            print(pg_ratings)
            print()
        icc = pg.intraclass_corr(data=df, targets="pg_targets", raters="pg_raters", ratings="pg_ratings", nan_policy="omit").round(4)
        # get coef. value: icc.iloc[2]["ICC"]
        return icc

    # Helper functions
    def overall_agreement(self):
        q = len(self.categories)
        p_a = dec.Decimal("0")
        if self.replications == 2:
            # Quelle: INTRARATER RELIABILITY, KILEM L. GWET, STATAXIS Consulting, Gaithersburg, Maryland
            # Paper S. 8 - Gleichung (12)
            for k in range(q):
                # p_a berechnet den Anteil wo die beiden Replikate bei den Subjects gleich bewertet worden sind.
                current_cat = self.categories[k]
                subject_kk = dec.Decimal("0")

                for subject in self.ratings:
                    if self.ratings[subject][FIRST_REPLIACTE] == current_cat and self.ratings[subject][FIRST_REPLIACTE] == self.ratings[subject][SECOND_REPLICATE]:
                        subject_kk += dec.Decimal("1")
                p_kk = subject_kk
                p_a += p_kk / self.quantity_subjects

            return p_a
        elif self.replications > 2:
            # m subjects, n replications per subject, q categories.
            # Quelle: INTRARATER RELIABILITY, KILEM L. GWET, STATAXIS Consulting, Gaithersburg, Maryland
            # Paper S. 9 - Gleichung (16)
            m = self.quantity_subjects
            n = self.replications

            for i in self.ratings:
                for k in range(q):
                    n_i_k = dec.Decimal("0")

                    for replicate_label in self.ratings[i]:
                        # Anzahl der Replikate in subject i berechnen, die der Kategorie k zugewiesen worden sind.
                        if replicate_label == self.categories[k]:
                            n_i_k += dec.Decimal("1")
                    
                    p_a += n_i_k * (n_i_k - 1) / (n * (n - 1))
            
            return p_a / m
        else:
            raise ValueError("Not enough replications per subject to calculate an overall agreement.")
    

def map_metrics(metric):
    if metric == "Cohen's-|Conger's \u03BA":
        return "conger"
    elif metric == "Fleiss' \u03BA":
        return "fleiss"
    elif metric == "Krippendorff's \u03B1":
        return "krippendorff"
    elif metric == "Gwet's AC":
        return "gwet"