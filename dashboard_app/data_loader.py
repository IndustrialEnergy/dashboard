from pathlib import Path
import pandas as pd
import os
# import numpy as np

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
        },
    )

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
