from pathlib import Path
import pandas as pd

def load_integrated_dataset():
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "data" / "iac_integrated.csv"

    integrated_df = pd.read_csv(data_path)

    return integrated_df