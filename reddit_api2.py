import praw
import csv
import json
import time
from datetime import datetime

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Parameters
subreddit_name = "buildapc"  # Change this to your desired subreddit
output_file = "reddit_comments.csv"
cursor_file = "reddit_cursor.json"
batch_size = 5  # Number of posts to fetch per batch
wait_time = 5  # Wait time (in seconds) between requests

# Load the cursor for resuming
try:
    with open(cursor_file, "r") as f:
        after = json.load(f).get("after", None)
        print(f"Resuming from after={after}")
except FileNotFoundError:
    after = None  # Start fresh if no cursor file is found

# Open the CSV file for appending (if resuming) or writing (if starting fresh)
with open(output_file, mode="a" if after else "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header row only if starting fresh
    if not after:
        writer.writerow(["Post Title", "Post URL", "Comment Author", "Comment Body", "Comment Upvotes"])

    # Fetch posts in batches
    fetching = True
    while fetching:
        print(f"Fetching a batch of {batch_size} posts...")
        try:
            # Fetch posts using the after parameter for pagination
            subreddit = reddit.subreddit(subreddit_name)
            posts = subreddit.hot(limit=batch_size)

            last_post = None  # Track the last post processed

            for post in posts:
                # Skip if already processed in a previous session
                if after and post.name <= after:
                    continue

                print(f"Processing post: {post.title}")
                last_post = post  # Update the last processed post

                # Fetch and process comments
                post.comments.replace_more(limit=0)  # Flatten comments
                for comment in post.comments.list():
                    comment_title = comment.body[:50]
                    print(f"Processing comment: {comment_title}...")
                    writer.writerow([
                        post.title, post.url, str(comment.author), comment.body, comment.score
                    ])

            # Update the cursor with the last processed post
            if last_post:
                after = last_post.name
                with open(cursor_file, "w") as f:
                    json.dump({"after": after}, f)

        except Exception as e:
            print(f"Error occurred: {e}. Retrying after {wait_time} seconds...")
            time.sleep(wait_time)
            continue

        print(f"Batch completed. Sleeping for {wait_time} seconds...")
        time.sleep(wait_time)

print(f"Data saved to {output_file}")
