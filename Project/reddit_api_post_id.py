import praw
import pandas as pd
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)
subreddit_name = "buildapc"
limit = None
output_file = "new_post_ids.csv"

post_id = [post.id for post in reddit.subreddit(subreddit_name).new(limit=limit)]

df = pd.DataFrame(post_id, columns=["post_id"])
df.to_csv(output_file, index = False)
print(f"saved {len(post_id)}")