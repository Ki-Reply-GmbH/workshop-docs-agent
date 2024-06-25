"""The `core` package provides functionalities for performing data analysis,
validating and processing file content, and calculating inter-rater reliability
metrics.

Modules:

- `create_analyses`: A module containing a class to perform intra-rater and
inter-rater analyses on provided data.

- `fileinteraction`: A module for validating, processing, and analyzing file
content for data analysis. It includes classes for file validation and
database interactions, and functions for writing analysis results to Excel
files.

Classes:

- `FileValidation`: Validates and processes file content for data analysis.

- `DBInteraction`: Handles database interactions, including loading,
creating, deleting, and changing profiles, and writing profile data to a
CSV file.

Functions:

- `write_excel(analyse, intra_ids, intra_metrics, inter_ids, inter_metrics,
scale_format, filename)`: Writes analysis results to an Excel file.

- `metrics`: A module for calculating various inter-rater reliability metrics.
It includes functionalities to compute Cohen's Kappa, Fleiss' Kappa, Gwet's
AC, Krippendorff's Alpha, and the Intraclass Correlation Coefficient (ICC).
It also computes the overall agreement and G-index for the given ratings.

Classes:

- `Metrics`: Calculates various inter-rater reliability metrics.

Functions:

- `map_metrics(metric)`: Maps a given metric name to its corresponding
internal representation.
"""


