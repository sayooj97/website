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
post_ids_file = "reddit_post_id.csv"  # File containing post IDs
output_file = "reddit_comments.csv"  # File to save comments
wait_time = 5  # Sleep time to avoid rate limits

# Read post IDs from CSV
df = pd.read_csv(post_ids_file)
post_ids = df["post_id"].tolist()

# Open CSV for writing comments
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Post ID", "Post Title", "Post Author", "Comment Author", "Comment Body", "Comment Upvotes"])

    # Process each post ID
    for post_id in post_ids:
        try:
            print(f"Fetching comments for post ID: {post_id}")
            post = reddit.submission(id=post_id)

            # Expand all "More Comments" links
            post.comments.replace_more(limit=None)

            # Fetch all comments
            for comment in post.comments.list():
                comment_preview = comment.body[:50]
                print(f"Processing comment: {comment_preview}...")

                writer.writerow([
                    post_id, post.title, str(post.author),
                    str(comment.author), comment.body, comment.score
                ])

        except Exception as e:
            print(f"Error fetching post {post_id}: {e}. Skipping...")
            continue  # Move to the next post if an error occurs

        print(f"Finished fetching comments for {post_id}. Sleeping for {wait_time} seconds...")
        time.sleep(wait_time)

print(f"All comments saved to {output_file}")
