# MTG CSV Enricher

## Overview

This Python script allows you to enrich a CSV file exported from **ManaBox** (or any CSV file containing a `Scryfall ID` column) with additional Magic: The Gathering card data fetched from the Scryfall API. The script adds relevant information such as mana cost, type line, oracle text, power, and toughness to your CSV file.

## Who is this for?

- Magic: The Gathering players who manage their collections using ManaBox or other tools and want to add detailed card information.
- Anyone who has a CSV file of Magic cards with `Scryfall IDs` and wants to enrich it with additional card data.
  
No prior coding knowledge is required to run this script!

## Prerequisites

### Install Python

You will need to have Python installed on your computer to run this script. You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

During the installation, make sure to **check the box that says "Add Python to PATH"**. This is essential for running Python from your command line.

### Install `pip`

`pip` is a package manager for Python that allows you to install libraries like `requests`, which is required for this script. `pip` comes bundled with Python, but if it's not installed, you can install it by following these [instructions](https://pip.pypa.io/en/stable/installation/).

### Verify Installation

After installing Python and `pip`, open a command prompt (Windows) or terminal (MacOS/Linux) and type:

```bash
python --version
```

This should show the installed version of Python. Next, check that `pip` is installed by typing:

```bash
pip --version
```

## Installing the Required Library

This script uses the `requests` library to make API calls. Install it using `pip`:

```bash
pip install requests
```

Now you're ready to use the script!

## Usage

1. **Download or Clone the Script**  
   - Download this script from GitHub or clone the repository using the following command:
     ```bash
     git clone <repository_url>
     ```
   - Alternatively, just download the `csv_converter.py` file and place it in your working directory.

2. **Prepare Your CSV File**  
   - If you're using **ManaBox**, export your collection to a CSV file and ensure it includes a `Scryfall ID` column.
   - If you're using another CSV, just make sure that your CSV has a column named `Scryfall ID`, which should contain the unique identifiers from Scryfall for each card. Without this, the script won't work.

3. **Run the Script**  
   Open a command prompt (Windows) or terminal (MacOS/Linux), navigate to the directory where the script is located, and run it by typing:

   ```bash
   python3 csv_converter.py <your_csv_file.csv>
   ```

   You can also process multiple CSV files at once:

   ```bash
   python3 csv_converter.py <file1.csv> <file2.csv>
   ```

   If you want more detailed output, add the `-v` (verbose) flag:

   ```bash
   python3 csv_converter.py -v <your_csv_file.csv>
   ```

4. **Output**  
   - The script will read your CSV file, fetch the data from the Scryfall API for each card, and enrich your file by adding new columns like **Mana cost**, **Type line**, **Oracle text**, **Power**, and **Toughness** (depending on what you configured in the script).
   - A new CSV file with the enriched data will be written to your directory.

5. **Dealing with Errors**  
   The script retries requests up to three times in case of connection errors or timeouts. If a card's data cannot be fetched after three attempts, it will be skipped, and the script will continue with the next card.

## How to Customize the Data

The `DATA_TO_IMPORT` dictionary in the script determines which fields from the Scryfall API will be added to your CSV file. For example:

```python
DATA_TO_IMPORT = {
    "mana_cost": "Mana cost", 
    "type_line": "Type line", 
    "oracle_text": "Oracle text", 
    "power": "Power", 
    "toughness": "Toughness"
}
```

In this example, the keys (e.g., `"mana_cost"`) are Scryfall API fields, and the values (e.g., `"Mana cost"`) are the corresponding column names in your CSV file.

You can modify `DATA_TO_IMPORT` to fetch different information from the Scryfall API. For a complete list of available fields, visit the [Scryfall API documentation](https://scryfall.com/docs/api/cards/id). The script also contains an `ACCEPTED_PARAMETERS` list which has the same fields you can use.

## Notes on API Limits

To comply with Scryfall’s API limits, the script adds a small delay of 75 milliseconds between each request. Altering this delay could result in your IP being temporarily or permanently banned from Scryfall’s API.
