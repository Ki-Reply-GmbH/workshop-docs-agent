# IIRA Package

Welcome to the IIRA package repository! This package provides a comprehensive framework for managing the main application window, including GUI elements, themes, frames, and database interactions. It also includes functionalities for data analysis, file processing, and inter-rater reliability metrics calculation.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Main Application](#main-application)
  - [Core Functionalities](#core-functionalities)
  - [Data Handling](#data-handling)
  - [Graphical User Interface](#graphical-user-interface)
- [Modules Overview](#modules-overview)
  - [IIRA](#iira)
  - [IIRA/core](#iiracore)
  - [IIRA/data](#iiradata)
  - [IIRA/gui](#iiragui)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The IIRA package aims to provide a robust framework for managing various aspects of a main application window, including graphical user interface (GUI) elements, themes, frames, and database interactions. Additionally, it offers tools for performing data analysis, validating and processing file content, and calculating inter-rater reliability metrics.

## Installation

To install the IIRA package, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/IIRA.git
cd IIRA
pip install -r requirements.txt
```

## Usage

### Main Application

The main application window is managed by the `app` module, which includes GUI elements, themes, frames, and database interactions.

### Core Functionalities

The `core` package provides essential functionalities for data analysis, file processing, and inter-rater reliability metrics calculation.

### Data Handling

The `data` package includes modules and classes for handling and manipulating data, including data processing, storage, and retrieval.

### Graphical User Interface

The `gui` package provides various GUI components for functionalities such as reliability analysis, file import, user profile management, and rating text elements using the tkinter library.

## Modules Overview

### IIRA

The `IIRA` package includes the main application window management:

- **app**: Manages GUI elements, themes, frames, and database interactions.

### IIRA/core

The `core` package provides functionalities for data analysis and inter-rater reliability metrics:

- **create_analyses**: Performs intra-rater and inter-rater analyses.
- **fileinteraction**: Validates, processes, and analyzes file content.
  - **FileValidation**: Validates and processes file content.
  - **DBInteraction**: Handles database interactions.
  - **write_excel**: Writes analysis results to an Excel file.
- **metrics**: Calculates various inter-rater reliability metrics.
  - **Metrics**: Calculates metrics like Cohen's Kappa, Fleiss' Kappa, etc.
  - **map_metrics**: Maps metric names to their internal representations.

### IIRA/data

The `data` package handles data processing, storage, and retrieval:

- **processing**:
  - **DataProcessor**: Processes data.
  - **process**: Method to process data.
  - **validate**: Method to validate data.
- **storage**:
  - **DataStorage**: Stores data.
  - **save**: Method to save data.
  - **load**: Method to load data.
- **retrieval**:
  - **DataRetriever**: Retrieves data.
  - **fetch**: Method to fetch data.
  - **parse**: Method to parse fetched data.

### IIRA/gui

The `gui` package provides GUI components for various functionalities:

- **analyseframe**:
  - **AnalyseFrame**: Sets up GUI for reliability analysis.
  - **ResultsFrame**: Displays reliability analysis results.
- **containerframe**: Represents a container frame with a menu bar.
- **fileframes**:
  - **ScaleFrame**: Scale and weight selection GUI.
  - **FileFrame**: File import GUI.
- **helperframes**:
  - **ProfileFrame**: Manages user profiles.
  - **ScrollFrame**: Creates a scrollable frame.
  - **MainHelpFrame**: Help dialog for main functionalities.
  - **ScaleHelpFrame**: Help dialog for scales and weights.
  - **ImportHelpFrame**: Help dialog for importing data.
  - **PrepAnalyseHelpFrame**: Help dialog for preparing an analysis.
  - **ResultsHelpFrame**: Help dialog for analysis results.
  - **RateHelpFrame**: Help dialog for rating functionality.
  - **callback**: Opens a URL in a web browser.
- **mainframe**: Sets up the main frame of the application.
- **rateframe**: Handles the UI for rating text elements.

## Contributing

We welcome contributions to the IIRA package! If you have any bug reports, feature requests, or pull requests, please submit them through the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.