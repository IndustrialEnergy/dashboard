# -------  IMPORT LIBRARIES -------

import pandas as pd
from pathlib import Path
import numpy as np
from janitor import clean_names
import re
from datetime import datetime
import sys
import json

# ------- define paths and file names -------

# define relative path
relative_path = Path("../../data/raw/")

# get absolute path
absolute_path = relative_path.resolve()

# declare file names
# use glob to match files starting with IAC_Database
iac_files = list(absolute_path.glob("IAC_Database*.xls"))

if not iac_files:
    print(
        f"INFO: No IAC_Database file found in {relative_path.resolve()}, skipping processing."
    )
    sys.exit(0)  # Exit cleanly with success code

iac_file = max(iac_files, key=lambda f: f.stat().st_mtime)

# extract last updatedtimestamp from filename
timestamp_match = re.search(r"IAC_Database_(\d{8})\.xls", iac_file.name)
if timestamp_match:
    file_timestamp = timestamp_match.group(1)
    last_updated_formatted = datetime.strptime(file_timestamp, "%Y%m%d").strftime(
        "%B %d, %Y"
    )
else:
    file_timestamp = "unknown"
    last_updated_formatted = "Unknown"

# continue processing if files found

# ------- import data -------
# import IAC database
all_sheets = pd.read_excel(iac_file, sheet_name=None)

# filter sheets that match the pattern
recc_sheets = {
    name: data for name, data in all_sheets.items() if name.startswith("RECC")
}
# combine matching sheets into a single DataFrame
iac_recc_df = pd.concat(
    [sheet.assign(RECC=name) for name, sheet in recc_sheets.items()], ignore_index=True
)

# import ASSESS table
iac_assess_df = all_sheets["ASSESS"]

# -------  normalize data -------


# Transform the iac_recc table from wide to long format
# Requirements
# 1. Keep all common columns
# 2. Create four rows for each input row (one for each energy source usage ranking: Primary, Secondary, Tertiary, Quaternary)
# 3. Maintain the relationship between energy source codes and their associated values: SOURCCODE, CONSERVED, SOURCONSV, SAVED
# 4. Order the columns to maintain the original dataframe structure
# Create a function to trasnform the recc table from wide to long format
def transform_recc_data(df):
    """
    Transform wide format usage data to long format by unpivoting usage-related columns.

    Parameters:
    df (pandas.DataFrame): Input DataFrame in wide format

    Returns:
    pandas.DataFrame: Transformed DataFrame in long format
    """

    # Common columns that will be repeated for each usage record
    common_cols = [
        "SUPERID",
        "ID",
        "AR_NUMBER",
        "APPCODE",
        "ARC2",
        "IMPSTATUS",
        "IMPCOST",
        "REBATE",
        "INCREMNTAL",
        "FY",
        "IC_CAPITAL",
        "IC_OTHER",
        "PAYBACK",
        "BPTOOL",
    ]

    # Create list of usage types
    usage_types = ["P", "S", "T", "Q"]

    # Initialize list to store transformed data
    transformed_data = []

    # Iterate through each row in the original dataframe
    for _, row in df.iterrows():
        # For each usage type, create a new record
        for usage in usage_types:
            new_row = {col: row[col] for col in common_cols}

            # Add usage-specific columns
            sourccode_col = f"{usage}SOURCCODE"
            conserved_col = f"{usage}CONSERVED"
            sourconsv_col = f"{usage}SOURCONSV"
            saved_col = f"{usage}SAVED"

            new_row["SOURCE_RANK"] = f"{usage}SOURCCODE"
            new_row["SOURCCODE"] = row.get(sourccode_col, "")
            new_row["CONSERVED"] = row.get(conserved_col, "")
            new_row["SOURCONSV"] = row.get(sourconsv_col, "")
            new_row["SAVED"] = row.get(saved_col, "")

            transformed_data.append(new_row)

    # Create new dataframe from transformed data
    result_df = pd.DataFrame(transformed_data)

    # Ensure columns are in the desired order
    column_order = (
        common_cols[:7]
        + ["SOURCE_RANK", "SOURCCODE", "CONSERVED", "SOURCONSV", "SAVED"]
        + common_cols[7:]
    )

    return result_df[column_order]


# Transform recc dataset from wide to long
iac_recc_tidy_df = transform_recc_data(iac_recc_df)

# #### Transform the iac_assess table from wide to long format
# Requirements
# 1. Keep all common columns
# 2. Convert *_plant_usage and *_plant_cost columns into rows under the plant_usage and plant_cost columns, and add a separate column for the source code.
# 4. Order the columns to maintain the original dataframe structure


def transform_assess_data(df):
    """
    Transform wide format plant data to long format by converting *_plant_usage
    and *_plant_cost columns into rows.

    Parameters:
    df (pandas.DataFrame): Input DataFrame in wide format

    Returns:
    pandas.DataFrame: Transformed DataFrame in long format
    """
    # Common columns that will be preserved
    id_vars = [
        "CENTER",
        "FY",
        "SIC",
        "NAICS",
        "STATE",
        "SALES",
        "EMPLOYEES",
        "PLANT_AREA",
        "PRODUCTS",
        "PRODUNITS",
        "PRODLEVEL",
        "PRODHOURS",
        "NUMARS",
    ]

    # Melt cost columns
    cost_df = pd.melt(
        df,
        id_vars=["ID"] + id_vars,
        value_vars=[col for col in df.columns if col.endswith("_plant_cost")],
        var_name="sourccode",  # match column name in RECC table
        value_name="plant_cost",
    )
    # Clean up sourccode by removing '_plant_cost'
    cost_df["sourccode"] = cost_df["sourccode"].str.replace("_plant_cost", "")

    # Melt usage columns
    usage_df = pd.melt(
        df,
        id_vars=["ID"] + id_vars,
        value_vars=[col for col in df.columns if col.endswith("_plant_usage")],
        var_name="sourccode",  # match column name in RECC table
        value_name="plant_usage",
    )
    # Clean up sourccode by removing '_plant_usage'
    usage_df["sourccode"] = usage_df["sourccode"].str.replace("_plant_usage", "")

    # Merge cost and usage dataframes
    result_df = cost_df.merge(
        usage_df, on=["ID"] + id_vars + ["sourccode"], how="outer"
    )

    # Create ordered categorical for sourccode
    source_order = (
        ["EC", "ED", "EF"]
        + [f"E{i}" for i in range(2, 13)]
        + [f"W{i}" for i in range(7)]
    )
    result_df["sourccode"] = pd.Categorical(
        result_df.sourccode, categories=source_order, ordered=True
    )

    # Remove rows where both plant_cost and plant_usage are NA
    result_df = result_df.dropna(subset=["plant_cost", "plant_usage"], how="all")

    # Sort by ID and sourccode and set ID as index
    # result_df = result_df.sort_values(by=['ID', 'sourccode']).set_index('ID')
    result_df = result_df.sort_values(by=["ID", "sourccode"])

    return result_df


# Transform assess dataset from wide to long
iac_assess_tidy_df = transform_assess_data(iac_assess_df)

# ------------------------ Clean data: ASSESS table ------------------------#

iac_assess_tidy_df = iac_assess_tidy_df.clean_names()
# strip whitespace from all string columns
for col in iac_assess_tidy_df.select_dtypes(include="object").columns:
    iac_assess_tidy_df[col] = iac_assess_tidy_df[col].str.strip()
# remove records that don't have any values for power sources other than primary

# ------------------------ Clean RECC table ------------------------#

# Replace old source coce for electricity values "E1" with "EC"
# Reason: E1 was replaced with EC, ED, and EF as of FY 95 (9/30/95)
# Reference: https://iac.university/technicalDocs/IAC_DatabaseManualv10.2.pdf
iac_recc_tidy_df.replace({"SOURCCODE": {"E1": "EC"}}, inplace=True)
iac_recc_tidy_df = iac_recc_tidy_df.clean_names()
# Remove records that don't have any values for power sources other than primary
iac_recc_tidy_df = iac_recc_tidy_df.dropna(
    subset=["sourccode", "conserved", "sourconsv", "saved"], how="all"
)

# ------------------------ Integrate IAC ASSESS and RECC datasets ------------------------#

iac_df = pd.merge(
    iac_assess_tidy_df,
    iac_recc_tidy_df,
    left_on=["sourccode", "id", "fy"],
    right_on=["sourccode", "id", "fy"],
    how="left",
)

iac_df.drop_duplicates(inplace=True)

# ------------------------ Clean integrated IAC dataset ------------------------#

# Filter out records prior to 1990 and rows with arc2 >= 3 (non-energy related)
# Reason: we don't have emissions and PPI data prior to 1990
cutoff_year = 1990
# convert "arc2" column to string to avoid issues with floating point precision
iac_df["arc2"] = iac_df["arc2"].astype(str)
iac_df = iac_df[(iac_df["fy"] >= cutoff_year) & (iac_df["arc2"].str.startswith("2"))]

# Filter out rows with sourccode "ED" and "EF" and not starting with "E"
iac_df = iac_df[
    iac_df["sourccode"].str.startswith("E") & ~iac_df["sourccode"].isin(["ED", "EF"])
]

print(iac_df["arc2"].dtype)
# print(iac_df[~iac_df['arc2'].str.startswith('2')])
print(iac_df["sourccode"].unique())
# print(iac_df['arc2'].unique())

# Calculate payback period
iac_df["payback_imputed"] = iac_df["payback"].combine_first(
    iac_df["impcost"] / iac_df["saved"]
)

iac_df["payback_imputed"] = pd.to_numeric(iac_df["payback_imputed"], errors="coerce")
iac_df["payback_imputed"] = iac_df["payback_imputed"].round(3)

# ------------------------ Save data to CSV ------------------------#

# Save the cleaned data to a CSV file
iac_df.to_csv("../../data/processed/iac.csv", index=False)

# ------------------------ Create Metadata ------------------------#

final_file_name = "iac_integrated.csv"
final_path = Path("../../data/final/")
# Create metadata
metadata = {
    "data_info": {
        "last_updated": last_updated_formatted,
        "source_file": iac_file.name,
        "processing_datetime": datetime.now().isoformat(),
    },
    "file_info": {
        "filename": final_file_name,
    },
}

# Save metadata to final folder
metadata_filepath = final_path / "iac_metadata.json"
with open(metadata_filepath, "w") as f:
    json.dump(metadata, f, indent=2)
