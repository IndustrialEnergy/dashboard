# -------  IMPORT LIBRARIES ------- 

import pandas as pd
from pathlib import Path
import numpy as np
from janitor import clean_names
import os
import sys

# ------- define paths and file names -------

# define relative path
relative_path = Path('../../data/processed/')
# get absolute path
absolute_path = relative_path.resolve()

def check_required_files(file_path, required_files):
    missing_files = []
    for file in required_files:
        if not (file_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("ERROR. The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("Please ensure all required files are present before running the data integration script.")
        sys.exit(1)  # Exit with error code
    
    return True

# Define required files
required_files = [
    'iac.csv',
    'ec_emission_factors.csv',
    'fuel_emission_factors.csv',
    'ppi.csv',
    'arc_descriptions.csv',
    'sic_to_naics.csv'
]

# Check files before proceeding
check_required_files(absolute_path, required_files)

# Only proceed with reading files if all exist
iac_df = pd.read_csv(absolute_path/'iac.csv')
ec_emission_factors_df = pd.read_csv(absolute_path/'ec_emission_factors.csv')
fuel_emission_factors_df = pd.read_csv(absolute_path/'fuel_emission_factors.csv')
ppi_df = pd.read_csv(absolute_path/'ppi.csv')
arc_df = pd.read_csv(absolute_path/'arc_descriptions.csv')
naics_df = pd.read_csv(absolute_path/'sic_to_naics.csv')


# -------  calculate & integrate emissions ------- #

# Fuel emissions 
# Add fuel emission factors to the iac_df
integrated_df = pd.merge(iac_df, fuel_emission_factors_df[['sourccode','emission_type','emission_factor','emission_factor_units']],
                                  on='sourccode',
                                  how='left')

# Calculate fuel emissions avoided
integrated_df['emissions_avoided'] = integrated_df['emission_factor'] * integrated_df['conserved']

print(integrated_df[integrated_df['superid']=='AM007902'])

# Electricity emissions
# Combine ec_emission_factors_df with the integrated iac table
integrated_df = pd.merge(integrated_df, ec_emission_factors_df[['state','year','emission_type','emission_factor','emission_factor_units','sourccode']],
                         left_on=['fy','state','sourccode'],
                         right_on=['year','state','sourccode'],
                         how='left')

print(integrated_df[integrated_df['superid']=='AM007902'])

# Merge overlapping columns
integrated_df['emission_type'] = integrated_df['emission_type_x'].combine_first(integrated_df['emission_type_y'])
integrated_df['emission_factor_units'] = integrated_df['emission_factor_units_x'].combine_first(integrated_df['emission_factor_units_y'])
integrated_df['emission_factor'] = integrated_df['emission_factor_x'].combine_first(integrated_df['emission_factor_y'])

# Drop the old duplicate columns
integrated_df.drop(columns=['emission_type_x', 'emission_type_y', 'emission_factor_units_x', 'emission_factor_units_y', 'year','emission_factor_x','emission_factor_y'], 
                   inplace=True)

# calculate emissions avoided for electricity
integrated_df.loc[integrated_df['sourccode'] == 'EC', 'emissions_avoided'] = (
    integrated_df['emission_factor'] * integrated_df['conserved']
)

integrated_df['emissions_avoided'] = pd.to_numeric(integrated_df['emissions_avoided'], errors='coerce')
integrated_df['emissions_avoided'] = integrated_df['emissions_avoided'].round(8)

integrated_df['emission_factor'] = pd.to_numeric(integrated_df['emission_factor'], errors='coerce')
integrated_df['emission_factor'] = integrated_df['emission_factor'].round(8)

# -------  calculate & integrate PPI-adjusted implementation cost ------- #

# handle current year ppi data
# e.g. if the current year data is not released or updated in the dataset, use the data from the most recent year
# set a reference_year
reference_year = max(ppi_df['year'])

# check which years are in PPI data
ppi_years = set(ppi_df['year'])

# Find the max FY in recc data
max_fy = integrated_df['fy'].max()

# Create a new column that only adjusts the most recent year if needed
integrated_df['base_year'] = integrated_df['fy'].apply(
    lambda y: reference_year if y == max_fy and y not in ppi_years else y
)

# create a dataframe with ppi values in a reference year
ppi_ref_year_df = ppi_df[ppi_df['year']==reference_year] 
ppi_ref_year_df = ppi_ref_year_df[['arc2', 'year', 'ppi']].rename(columns={'year': 'reference_year', 'ppi': 'reference_ppi'})

print(ppi_ref_year_df.head())

# add reference_year and reference year ppi values to recc_ppi_df
ppi_df = pd.merge(ppi_df,ppi_ref_year_df[['arc2','reference_year','reference_ppi']],
                       on='arc2',
                       how='left')

ppi_df = ppi_df.rename(columns={'year': 'base_year', 'ppi': 'base_ppi'})

# merge ppi_df with integrated_df
integrated_df = pd.merge(integrated_df, ppi_df[['arc2', 'reference_year', 'reference_ppi', 'base_year', 'base_ppi']],
                         left_on=['arc2','base_year'],
                         right_on=['arc2','base_year'],
                         how='left'
                         )
# calculate ppi adjusted implementation cost
integrated_df['impcost_adj'] = integrated_df['impcost'] * (integrated_df['reference_ppi'] / integrated_df['base_ppi']).round(2)
integrated_df['impcost_adj'] = pd.to_numeric(integrated_df['impcost_adj'], errors='coerce')
integrated_df['impcost_adj'] = integrated_df['impcost_adj'].round(2)

# -------  integrate ARC descriptions ------- #
integrated_df = pd.merge(integrated_df, arc_df,
                         left_on='arc2',
                         right_on='specific_code',
                         how='left'
                         )


# -------  integrate NAICS and SIC descriptions ------- #



# -------  Integrated dataset: Validate ------- #

# print(iac_df['arc2'].dtype)
# #print(iac_df[~iac_df['arc2'].str.startswith('2')])
# print(iac_df['sourccode'].unique())
# #print(iac_df['arc2'].unique())
print(integrated_df[integrated_df['superid']=='AM007902'])
print(integrated_df[integrated_df['superid']=='AM007903'])
print(integrated_df[integrated_df['id']=='AM0079'])


#------------------------ Save data to CSV ------------------------#

# Save the cleaned data to a CSV file
integrated_df.to_csv("../../data/final/iac_integrated.csv", index=False)