import pandas as pd
text = pd.read_csv("processed_comments.csv")
print(text['part_type'].to_string())
# print(text.columns)