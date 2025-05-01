from pathlib import Path
import pandas as pd
# import numpy as np

# Converting to a categorical data type is a memory optimization technique that:
# - Stores each unique value only once
# - Uses integer codes to reference these values
# - Maintains the exact same data, just in a more memory-efficient format

def load_integrated_dataset():
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "data" / "iac_integrated_dash.csv"

    # load data with optimized dtypes for improved performance
    integrated_df = pd.read_csv(
        data_path,
        dtype={
            "fy": "int16",
            "sector": "category", 
            "state": "category",
            "arc2": "category",
            "arc_description": "category",
            "impcost_adj": "float32",
            "payback": "float32",
        },
    )

    # convert string columns that have < 100 unique values to categorical for improved performance
    skip_cols = ["sector", "state", "arc2", "arc_description", "impstatus"]
    categorical_threshold = 100

    for col in integrated_df.select_dtypes(include=["object"]).columns:
        if col not in skip_cols and integrated_df[col].nunique() < categorical_threshold:
            integrated_df[col] = integrated_df[col].astype("category")

    return integrated_df
