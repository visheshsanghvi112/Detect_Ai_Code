import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Load the standard file (shankar 33)
def load_file(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

# Function to transform the file structure
def transform_to_standard_format(file_to_transform, standard_columns):
    # Step 1: Rename columns to match the standard if necessary
    file_to_transform.columns = standard_columns[: len(file_to_transform.columns)]
    
    # Step 2: Add missing columns
    for col in standard_columns[len(file_to_transform.columns):]:
        file_to_transform[col] = None  # Fill missing columns with None or default values
    
    # Step 3: Reorder columns to match the standard
    file_to_transform = file_to_transform[standard_columns]
    
    return file_to_transform

# Standard file path
STANDARD_FILE_PATH = r"C:\Users\gener\Downloads\shankar 33.csv"

if __name__ == "__main__":
    # Load the standard file once
    print("Loading standard file (shankar 33)...")
    shankar = load_file(STANDARD_FILE_PATH)
    shankar_columns = shankar.columns
    print("Standard file loaded successfully!")
    
    # Hide the root Tkinter window
    Tk().withdraw()
    
    # Step 1: Select the file to transform
    print("\nSelect the file you want to transform...")
    transform_file_path = askopenfilename(title="Select the file to transform")
    if not transform_file_path:
        print("No file selected. Exiting.")
        exit()
    
    file_to_transform = load_file(transform_file_path)
    print(f"File '{transform_file_path}' loaded successfully!")
    
    # Step 2: Transform the selected file
    transformed_file = transform_to_standard_format(file_to_transform, shankar_columns)
    
    # Step 3: Automatically save the transformed file
    import os
    base_name, ext = os.path.splitext(transform_file_path)
    save_path = f"{base_name}_modified{ext}"
    
    transformed_file.to_csv(save_path, index=False)
    print(f"Transformed file saved successfully at: {save_path}")
