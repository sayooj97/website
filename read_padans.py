import pandas as pd
text = pd.read_csv("cleaned_text.csv")
df = text[['comments','upvotes']]
print(df.to_string())
# print(text.columns)z