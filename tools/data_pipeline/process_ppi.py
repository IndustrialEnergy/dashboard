# -------  IMPORT LIBRARIES ------- 

import pandas as pd
from pathlib import Path
from janitor import clean_names
import sys

# ------- define paths and file names -------

# define relative path
relative_path = Path('../../data/raw/')

# get absolute path
absolute_path = relative_path.resolve()

# declare file names
# use glob to match files starting with annual_generation_state
ppi_files = list(absolute_path.glob("ARC_PPI*.xlsx"))
if not ppi_files:
    print(f"INFO: No file with PPI data found in {relative_path.resolve()} (Expected file name 'ARC_PPI*.xlsx'), skipping processing.")
    sys.exit(0)  # Exit cleanly with success code

ppi_file = max(ppi_files, key=lambda f: f.stat().st_mtime) # select the most recent file if multiple files exist
# continue processing if files found

# ------- import data -------

def find_sheet(sheet_names, keyword):
    for name in sheet_names:
        if keyword in name:
            return name
    raise ValueError(f"No sheet containing '{keyword}' found.")

# Load all sheets from the file
all_sheets = pd.read_excel(ppi_file, sheet_name=None)

# Extract the sheet names
sheet_names = all_sheets.keys()
# Find the correct sheet based on keyword
target_sheet = find_sheet(sheet_names, "ppi")
# Load the matched sheet into a DataFrame, skipping the first row
ppi_df = pd.read_excel(ppi_file, sheet_name=target_sheet, skiprows=6, dtype={"ARC": str}) # data to load starts from row 7

# -------  normalize data ------- 

#### Transform the ppi table from wide to long format
# 1. Keep all common columns
# 2. Convert year columns into rows under the year and ppi columns
# 3. Order the columns to maintain the original dataframe structure

# select columns that are integers >= 1990
year_columns = [col for col in ppi_df.columns if isinstance(col, int) and col >= 1990]

ppi_tidy_df = pd.melt(
    ppi_df,
    id_vars=['ARC', 'Description', 'Series ID', 'Industry', 'Product'],
    value_vars=year_columns,
    var_name='year',
    value_name='ppi'
    )

ppi_tidy_df = ppi_tidy_df.sort_values(by=['year', 'ARC'])

#------------------------  Clean data: PPI data ------------------------#

ppi_tidy_df.rename(columns={'ARC': 'ARC2'}, inplace=True) # rename the column ARC to ARC2 to match the IAC data
ppi_tidy_df['ppi'] = pd.to_numeric(ppi_tidy_df['ppi'], errors='coerce')
ppi_tidy_df['ARC2'] = pd.to_numeric(ppi_tidy_df['ARC2'], errors='coerce')
ppi_tidy_df = ppi_tidy_df.clean_names()

ppi_tidy_df['ppi'] = ppi_tidy_df['ppi'].round(2)
ppi_tidy_df['arc2'] = ppi_tidy_df['arc2'].round(4)
ppi_tidy_df['arc2'] = ppi_tidy_df['arc2'].astype(str) # convert "arc2" column to string to avoid issues with floating point precision

#------------------------ Clean data: validate ------------------------#

# print(len(ppi_tidy_df[ppi_tidy_df['arc2']=='2.7142'])) # should be >=35
# print(ppi_tidy_df[ppi_tidy_df['arc2']=='2.1123']) # should not be empty
# print(ppi_tidy_df['ppi'].dtype) # expected to be float64
# print(ppi_tidy_df['arc2'].dtype) # expected to be string (object)

#------------------------ Save data to CSV ------------------------#

# Save the cleaned data to a CSV file
ppi_tidy_df.to_csv("../../data/processed/ppi.csv", index=False)