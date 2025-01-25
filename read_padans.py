import pandas as pd
text = pd.read_csv("reddit_comments.csv")
print(text["Comment Body"])