import praw
import pandas as pd
import csv
import time

# Reddit API credentials (Replace with your own)
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Input & output files
post_ids_file = "reddit_post_id.csv"  # Original file containing post IDs
new_post_ids_file = "new_post_ids.csv"  # File containing newly fetched post IDs
output_file = "reddit_comments.csv"  # File to save comments
wait_time = 5  # Sleep time to avoid rate limits

# Read original post IDs (already processed)
df_original = pd.read_csv(post_ids_file)
original_post_ids = set(df_original["post_id"].tolist())

# Read newly fetched post IDs
df_new = pd.read_csv(new_post_ids_file)
new_post_ids = set(df_new["post_id"].tolist())

# Remove duplicate post IDs (those that already exist in the original file)
post_ids_to_process = new_post_ids - original_post_ids  # New post IDs that haven't been processed yet

if not post_ids_to_process:
    print("No new posts to process. Exiting...")
    exit()

# Open CSV for writing comments
with open(output_file, mode="a", newline="", encoding="utf-8") as file:  # Append mode
    writer = csv.writer(file)

    for post_id in post_ids_to_process:
        try:
            print(f"Fetching comments for post ID: {post_id}")
            post = reddit.submission(id=post_id)
            post.comments.replace_more(limit=None)

            for comment in post.comments.list():
                writer.writerow([
                    post_id, post.title, str(post.author),
                    str(comment.author), comment.body, comment.score
                ])

            # Add post_id to the original file (to track that it has been processed)
            original_post_ids.add(post_id)

        except Exception as e:
            print(f"Error fetching post {post_id}: {e}. Skipping...")
            continue

        print(f"Finished fetching comments for {post_id}. Sleeping for {wait_time} seconds...")
        time.sleep(wait_time)

# Update the original file with newly processed post IDs
updated_df = pd.DataFrame({"post_id": list(original_post_ids)})
updated_df.to_csv(post_ids_file, index=False)

print(f"All comments saved to {output_file} and original post IDs updated.")
