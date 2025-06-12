from pathlib import Path
import pandas as pd
import os
import numpy as np

# Converting to a categorical data type is a memory optimization technique that:
# - Stores each unique value only once
# - Uses integer codes to reference these values
# - Maintains the exact same data, just in a more memory-efficient format


def load_integrated_dataset():
    # get data path from environment variable or construct default path
    data_dir = os.getenv("DATA_DIR")

    if data_dir:
        data_path = Path(data_dir) / "iac_integrated.csv"
    else:
        # if DATA_DIR is not set, construct path relative to current file
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        data_dir = project_root / "data" / "final"
        data_path = data_dir / "iac_integrated.csv"

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at: {data_path}")
    # debug print
    # print(f"\nFile size: {data_path.stat().st_size:,} bytes")

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
            "impstatus": "string",  # force string type for impstatus
        },
        na_values=["nan", "NaN", "NAN", ""],  # explicitly handle NA values
    )

    # clean up impstatus column - replace NaN with 'Unknown'
    integrated_df["impstatus"] = integrated_df["impstatus"].fillna("K")

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
