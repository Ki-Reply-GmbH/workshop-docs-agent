"""The `gui` package provides graphical user interface (GUI) components for various
functionalities such as reliability analysis, file import, user profile management,
and rating text elements using the tkinter library.

Modules
=======

analyseframe
------------
Provides GUI components for reliability analysis, including intra-rater and
inter-rater analysis. It includes classes for creating and managing frames,
handling user inputs, and displaying results.

Classes:
- AnalyseFrame: Sets up the GUI components for reliability analysis.
- ResultsFrame: Sets up the GUI components for displaying reliability analysis
results.

containerframe
--------------
A class representing a container frame with a menu bar. This class extends
ttk.Frame and initializes a container frame with an accent color, a menu bar,
and various interactive elements.

fileframes
----------
A module for creating a graphical user interface (GUI) for scale and weight
selection, and file import using tkinter.

Classes:
- ScaleFrame: Represents the ScaleFrame for scale and weight selection GUI.
- FileFrame: Represents the FileFrame for file import GUI.

helperframes
------------
Provides a graphical user interface (GUI) for managing user profiles, creating
scrollable frames, and displaying help dialogs using the tkinter library.

Classes:
- ProfileFrame: Creates a user interface for managing user profiles.
- ScrollFrame: Creates a scrollable frame using a canvas and a vertical
scrollbar.
- MainHelpFrame: Creates a help dialog window for providing information about
the main functionalities of the application.
- ScaleHelpFrame: Creates a help dialog window for providing information on
scales and weights.
- ImportHelpFrame: Creates a help dialog window for providing information on
importing data formats.
- PrepAnalyseHelpFrame: Creates a help dialog window for providing information
on preparing an analysis.
- ResultsHelpFrame: Creates a help dialog window for providing information
about the results of reliability analyses.
- RateHelpFrame: Creates a help dialog window for providing information about
the rating functionality in the application.

Functions:
- callback(url): Opens the provided URL in a web browser.

mainframe
---------
Represents the main frame of the application, setting up the UI components,
handling profile creation, and managing different operational modes such as
'analyse' and 'rate'.

rateframe
---------
Represents the RateFrame, which handles the user interface for rating text
elements. It includes methods for populating navigation, randomizing text
order, handling events, and updating the UI based on user interactions.
"""


