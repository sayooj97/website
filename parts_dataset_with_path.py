import pandas as pd
import glob
import os

# Get all CSV file paths
pc_parts = glob.glob("csv_files/*.csv")
output_dir = "new"
output_file = os.path.join(output_dir, "parts_name_list.csv")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store data from multiple files
data_dict = {}

# Process each file
for pc_part in pc_parts:
    df = pd.read_csv(pc_part)
    file_name = os.path.basename(pc_part).replace(".csv", "")  # Remove .csv extension

    if "name" in df.columns:
        # Rename 'name' column to the file name
        df.rename(columns={"name": file_name}, inplace=True)

        # Store the column values
        data_dict[file_name] = df[file_name].tolist()

# Convert to DataFrame
final_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))

# Save to CSV
final_df.to_csv(output_file, index=False)
print(f"Final CSV saved at {output_file}")
