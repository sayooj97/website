import pandas as pd
import glob
import os

# Get all CSV file paths
pc_parts = glob.glob("csv_files/*.csv")
output_file = "parts_name_list.csv"

# Process each file
for pc_part in pc_parts:
    df = pd.read_csv(pc_part)
    file_name = os.path.basename(pc_part)

    print(f"Columns in {file_name}: {list(df.columns)}\n")
    old_col = input(f"Enter the column name to rename from {list(df.columns)}:\n")

    if old_col in df.columns:
        new_column = input(f"Enter the new name for '{old_col}' in {file_name}:\n")

        # Rename the column
        df.rename(columns={old_col: new_column}, inplace=True)
        print(f"Renamed '{old_col}' to '{new_column}' in {file_name}")

        # Extract the renamed column
        renamed_df = df[[new_column]].copy()
        renamed_df["source_file"] = file_name  # Track source file

        # Check if the output file exists
        file_exists = os.path.isfile(output_file)

        # Append to CSV file
        renamed_df.to_csv(output_file, mode='a', index=False, header=not file_exists)

        print(f"Renamed column from {file_name} appended to '{output_file}'.\n")

    else:
        print(f"Column '{old_col}' not found in {file_name}, skipping...\n")

print("All renaming operations completed.")
