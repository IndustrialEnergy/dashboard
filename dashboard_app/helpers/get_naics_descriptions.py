import pandas as pd
from pathlib import Path


def get_naics_descriptions():
    """
    Load NAICS descriptions from the naics_hierarchy.csv file.
    Returns a dictionary mapping NAICS codes to their descriptions and hierarchy levels.
    """
    # Get the path to the NAICS hierarchy file
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    naics_file = project_root / "data" / "processed" / "naics_hierarchy.csv"

    # Read the NAICS hierarchy file
    naics_df = pd.read_csv(naics_file, dtype={"naics_code": str})

    # Create a mapping of codes to descriptions and hierarchy levels
    naics_descriptions = {}
    for _, row in naics_df.iterrows():
        naics_code = str(row["naics_code"]).strip()
        industry_description = row["industry_description"].strip()
        hierarchy_level = row["hierarchy_level"].strip()
        naics_descriptions[naics_code] = {
            "description": industry_description,
            "level": hierarchy_level,
        }

    return naics_descriptions
