import pandas as pd
import os

def get_data_from_local():
    # Define the relative path to the CSV file
    file_path = "data/final/iac_integrated.csv"
    
    try:
        # Check if file exists
        if os.path.exists(file_path):
            # Read the CSV file
            df = pd.read_csv(file_path)
            return df
        else:
            print(f"File not found: {file_path}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return pd.DataFrame()
