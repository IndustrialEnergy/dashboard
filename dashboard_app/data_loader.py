from pathlib import Path
import pandas as pd
import os
import numpy as np

# Converting to a categorical data type is a memory optimization technique that:
# - Stores each unique value only once
# - Uses integer codes to reference these values
# - Maintains the exact same data, just in a more memory-efficient format


def load_integrated_dataset():

    # Get data path from environment variable or construct default path
    data_dir = os.getenv("DATA_DIR")

    if data_dir:
        print(f"Using DATA_DIR from environment: {data_dir}")
        data_path = Path(data_dir) / "iac_integrated.csv"
    else:
        # If DATA_DIR is not set, construct path relative to current file
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        data_dir = project_root / "data" / "final"
        data_path = data_dir / "iac_integrated.csv"
        print(f"DATA_DIR not set, using path relative to current file:")
        print(f"  Current file: {current_file}")
        print(f"  Project root: {project_root}")
        print(f"  Data dir: {data_dir}")

    print(f"Loading data from: {data_path}")  # Debug print

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    print(f"\nFile size: {data_path.stat().st_size:,} bytes")

    # Read first few lines of the file to check structure
    with open(data_path, "r") as f:
        print("\nFirst few lines of the file:")
        for i, line in enumerate(f):
            if i < 3:  # Print first 3 lines
                print(line.strip())
            else:
                break

    # load data with optimized dtypes for improved performance
    integrated_df = pd.read_csv(
        data_path,
        dtype={
            "fy": "Int16",
            "reference_year": "Int64",
            "base_year": "Int64",
            "naics_description": "category",
            "naics_imputed": "category",
            "state": "category",
            "arc2": "category",
            "specific_description": "category",
            "impcost_adj": "float32",
            "payback": "float32",
            "impstatus": "string",  # Force string type for impstatus
        },
        na_values=["nan", "NaN", "NAN", ""],  # Explicitly handle NA values
    )

    # Clean up impstatus column - replace NaN with 'Unknown'
    integrated_df["impstatus"] = integrated_df["impstatus"].fillna("K")

    print("\nDataset loaded successfully:")
    print(f"Shape: {integrated_df.shape}")
    print("\nData types:")
    print(integrated_df.dtypes)
    print("\nSample of data:")
    print(integrated_df[["fy", "state", "arc2", "naics_imputed", "impstatus"]].head())
    print("\nUnique values in key columns:")
    print(f"States: {sorted(integrated_df['state'].unique())}")
    print(f"Implementation statuses: {sorted(integrated_df['impstatus'].unique())}")
    print(f"ARC codes: {len(integrated_df['arc2'].unique())} unique values")
    print(f"NAICS codes: {len(integrated_df['naics_imputed'].unique())} unique values")

    # Validate critical columns
    if integrated_df["state"].isna().any():
        print("\nWARNING: Found NULL values in state column!")
    if integrated_df["impstatus"].isna().any():
        print("\nWARNING: Found NULL values in impstatus column!")
    if integrated_df["arc2"].isna().any():
        print("\nWARNING: Found NULL values in arc2 column!")

    # convert string columns that have < 100 unique values to categorical for improved performance
    skip_cols = [
        "naics_description",
        "naics_imputed",
        "state",
        "arc2",
        "specific_description",
        "impstatus",
        "emission_type",
        "sourccode",
    ]
    categorical_threshold = 100

    for col in integrated_df.select_dtypes(include=["object"]).columns:
        if (
            col not in skip_cols
            and integrated_df[col].nunique() < categorical_threshold
        ):
            integrated_df[col] = integrated_df[col].astype("category")

    return integrated_df


## put in url data_server that points to bren port: 3009 (data) and port: 3010 (client)
