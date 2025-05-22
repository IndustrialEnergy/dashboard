# -------  IMPORT LIBRARIES ------- 

import pandas as pd
from pathlib import Path
import numpy as np
from janitor import clean_names
import sys

# ------- define paths and file names -------

# define relative path
relative_path = Path('../../data/raw/')

# get absolute path
absolute_path = relative_path.resolve()

# declare file names
# use glob to match files starting with annual_generation_state
ec_generation_files = list(absolute_path.glob("annual_generation_state*.xls"))
if not ec_generation_files:
    print(f"INFO: No generation file found in {relative_path.resolve()}, skipping processing.")
    sys.exit(0)  # Exit cleanly with success code

ec_emissions_files = list(absolute_path.glob("emission_annual*.xlsx"))
if not ec_emissions_files:
    print(f"INFO: No emissions file found in {relative_path.resolve()}, skipping processing.")
    sys.exit(0)  # Exit cleanly with success code

ec_generation_file = max(ec_generation_files, key=lambda f: f.stat().st_mtime)
ec_emissions_file = max(ec_emissions_files, key=lambda f: f.stat().st_mtime)
# continue processing if files found

# ------- import data -------

def find_sheet(sheet_names, keyword):
    for name in sheet_names:
        if keyword in name:
            return name
    raise ValueError(f"No sheet containing '{keyword}' found.")

# Load all sheets from the file
all_sheets = pd.read_excel(ec_generation_file, sheet_name=None)

# Extract the sheet names
sheet_names = all_sheets.keys()
# Find the correct sheet based on keyword
target_sheet = find_sheet(sheet_names, "Generation")
# Load the matched sheet into a DataFrame, skipping the first row
generation_df = pd.read_excel(ec_generation_file, sheet_name=target_sheet, skiprows=1)

# Repeat the process for emissions data
all_sheets = pd.read_excel(ec_emissions_file, sheet_name=None)
sheet_names = all_sheets.keys()
target_sheet = find_sheet(sheet_names, "Emissions")
emissions_df = pd.read_excel(ec_emissions_file, sheet_name=target_sheet)

# -------  normalize data ------- 

# Keep all common columns
# Convert emission type columns into rows under the emission type columns and emissions columns
# Add a column for units
# Order the columns to maintain the original dataframe structure

# emissions_df.columns = [col.replace('\n(Metric Tons)', '') 
#                         for col in emissions_df.columns]
emissions_df.columns = [str(col).replace('\n(Metric Tons)', '').strip() for col in emissions_df.columns]

print(emissions_df.columns)
# Melt the dataframe
emissions_tidy_df = pd.melt(
    emissions_df,
    id_vars = ['State', 'Year', 'Producer Type', 'Energy Source'],
    value_vars = ['CO2', 'SO2', 'NOx'],
    var_name = 'emission_type',
    value_name = 'amount'
    )

#------------------------  Clean data: Electricity Generation table ------------------------#

generation_df = generation_df.clean_names()
generation_df = generation_df.rename(columns={'generation_megawatthours_': 'generation_megawatthours'})
generation_df['units'] = 'MWh' # add a column for units
# strip whitespace from all string columns
for col in generation_df.select_dtypes(include='object').columns:
    generation_df[col] = generation_df[col].str.strip()

#------------------------ Clean data: Electricity Emissions table ------------------------#

emissions_tidy_df = emissions_tidy_df.clean_names()
# strip whitespace from all string columns
for col in emissions_tidy_df.select_dtypes(include='object').columns:
   emissions_tidy_df[col] = emissions_tidy_df[col].str.strip()

#------------------------ Calculate emission factors for electricity ------------------------#

ec_emissions_df =  emissions_tidy_df[( emissions_tidy_df['producer_type']=='Total Electric Power Industry')& # units = metric ton
                                  ( emissions_tidy_df['energy_source']=='All Sources')]

ec_generation_df = generation_df[(generation_df['type_of_producer']=='Total Electric Power Industry')&
                                  (generation_df['energy_source']=='Total')]

# calculate emission factors
# Total Emissions/Total Electricity Generated
ec_emission_factors_df = pd.merge(ec_generation_df,ec_emissions_df[['year','state','emission_type','amount']])
ec_emission_factors_df['emission_factor'] = ec_emission_factors_df['amount'] / ec_emission_factors_df['generation_megawatthours']

# add column emission_factor_units
ec_emission_factors_df['emission_factor_units'] = 'kg/kWh'
ec_emission_factors_df['sourccode'] = 'EC'

#------------------------ Save data to CSV ------------------------#

# Save the cleaned data to a CSV file
ec_emission_factors_df.to_csv("../../data/processed/ec_emission_factors.csv", index=False)