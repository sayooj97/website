import pandas as pd
df = pd.read_csv("reddit_comments.csv")

ddf = df[['Post Title', 'Comment Body']]
print(ddf)

ddf.to_csv("new.csv")