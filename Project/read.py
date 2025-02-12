import pandas as pd

def search_part(df, part_name):
    """
    Search for a specific part name in the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing part information.
    part_name (str): The part name to search for.

    Returns:
    pd.DataFrame: Filtered DataFrame with matching part names.
    """
    part_name = part_name.lower().strip()  # Convert input to lowercase for case-insensitive search
    filtered_df = df[df["part_name"].str.lower().str.contains(part_name, na=False)]
    
    if filtered_df.empty:
        print(f"No results found for '{part_name}'.")
        return None
    return filtered_df[["part_name", "sentiment_label", "original_comment","part_type"]]

if __name__ == "__main__":
    # Load DataFrame
    input_csv = "processed_comments.csv"  # Update with the actual CSV file path
    df_parts = pd.read_csv(input_csv)
    
    # Search for a part
    search_term = input("Enter part name to search: ")
    result_df = search_part(df_parts, search_term)
    
    # Display results
    if result_df is not None:
        print(result_df)
