import pandas as pd
import requests
import io
import zipfile
import os
import tempfile

def get_data_from_zip():
    url = "https://iac.university/storage/IAC_Database.zip"
    
    try:
        response = requests.get(url)
        
        # Create a temporary directory to extract files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the zip file
            zip_path = os.path.join(temp_dir, "iac_database.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path) as z:
                file_list = z.namelist()
                
                # Look for Excel files
                data_files = [f for f in file_list if f.endswith(('.xlsx', '.xls', '.csv'))]
                
                if data_files:
                    data_file = data_files[0]
                    z.extract(data_file, temp_dir)
                    
                    # Read the file based on its extension
                    if data_file.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(os.path.join(temp_dir, data_file))
                    else:  # CSV file
                        df = pd.read_csv(os.path.join(temp_dir, data_file))
                    
                    return df
    except Exception:
        pass
    
    # Return empty DataFrame if errored out
    return pd.DataFrame()
