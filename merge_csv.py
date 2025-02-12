import os
import pandas as pd

def merge_csv_files(input_folder: str, output_file: str):
    """
    Merges all CSV files in the specified folder into a single CSV file.
    Handles large datasets efficiently without dropping data.
    If duplicate column names exist, renames them by prefixing the filename (without extension).
    
    Args:
        input_folder (str): Path to the folder containing CSV files.
        output_file (str): Path to the output merged CSV file.
    """
    all_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    if not all_files:
        print("No CSV files found in the directory.")
        return
    
    df_list = []
    column_tracker = {}
    
    for file in all_files:
        try:
            file_name = os.path.splitext(os.path.basename(file))[0]
            df = pd.read_csv(file, dtype=str, low_memory=False)
            
            new_columns = []
            for col in df.columns:
                if col in column_tracker:
                    new_col_name = f"{file_name}_{col}"
                    print(f"Renaming duplicate column '{col}' in {file} to '{new_col_name}'")
                    new_columns.append(new_col_name)
                else:
                    new_columns.append(col)
                column_tracker[col] = column_tracker.get(col, 0) + 1
            
            df.columns = new_columns
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    merged_df = pd.concat(df_list, axis=0, ignore_index=True, sort=False)
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved as: {output_file}")

# Example usage
input_folder = "csv_files"  # Change this to your folder path
output_file = "merged_dataset.csv"  # Output file name
merge_csv_files(input_folder, output_file)
