import pandas as pd
text = pd.read_csv("synthetic_pc_reviews_updated.csv")
df = text[['Processor', 'Motherboard', 'Sentiment']]
print(df.to_string())
# print(text.columns)