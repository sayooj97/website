import pandas as pd
text = pd.read_csv("reddit_comments.csv")
df = text[["Post Title","Post Upvotes"]]
print(df.to_string())
# print(text.columns)