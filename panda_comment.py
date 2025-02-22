import pandas as pd

# File path
input_csv = "cleaned_reddit_comments.csv"  # Change this to your actual CSV file

# Read only first 100 rows
df = pd.read_csv(input_csv, usecols=["cleaned_comment"], nrows=10)

# Save the output
df.to_csv("first_100_comments.csv", index=False)

print("✅ First 100 comments saved to 'first_100_comments.csv'")
