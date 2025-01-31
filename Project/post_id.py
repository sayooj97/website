import pandas as pd
import csv

post_id = pd.read_csv("reddit_post_id.csv")
new = pd.read_csv("new_post_ids.csv")

post_id_df = set(post_id['post_id'].tolist())
new_df = set(new['post_id'].tolist())

post_id_process = new_df - post_id_df

print(f"{len(post_id_process)}")