# DayZ Type.xml Editor

## Overview

The **DayZ Type.xml Editor** is a graphical user interface (GUI) application designed to edit the `types.xml` file used in the game **DayZ**. This application allows users to load, modify, and save item attributes within the `types.xml` file, facilitating easier management of game items without directly editing the XML file.

## Features

- **Load XML File**: Load the `types.xml` file from an `input` directory.
- **Search Functionality**: Search for items by name using a search box.
- **Edit Item Attributes**: Display and edit various attributes of the selected item, including:
  - Name
  - Nominal
  - Lifetime
  - Restock
  - Minimum
  - QuantMin
  - QuantMax
  - Cost
- **Overwrite All Items**: Overwrite attributes of all items with the values entered in the corresponding fields.
- **Save Changes**: Save modifications to a new `types.xml` file in an `output` directory.

## Requirements

- **Python**: This application requires Python (version 3.6 or higher).
- **Tkinter**: The built-in `tkinter` library for creating the GUI.
- **ElementTree**: The built-in `xml.etree.ElementTree` module for XML parsing.

## Installation

1. Ensure Python is installed on your machine.
2. Create two directories named `input` and `output` in the same folder where the script will be run.
3. Place the `types.xml` file inside the `input` directory.
