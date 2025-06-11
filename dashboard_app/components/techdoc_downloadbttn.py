import os

def get_td_from_local():
    file_path = "assets/Technical_Documentation.pdf"
    try:
        if os.path.exists(file_path):
            return file_path  # Return file path, not DataFrame
        else:
            print(f"File not found: {file_path}")
            return None
    except Exception as e:
        print(f"Error accessing file: {e}")
        return None