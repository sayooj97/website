import praw
import csv
import time
from datetime import datetime
import json

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Parameters
subreddit_name = "buildapc"
batch_size = 5
wait_time = 10
output_file = "reddit_comments.csv"
date_limit = datetime(2018, 12, 31)
cursor_file = "reddit_cursor.json"

# Load the cursor (if any) for resuming
try:
    with open(cursor_file, "r") as f:
        after = json.load(f).get("after", None)
        print(f"Resuming from after={after}")
except FileNotFoundError:
    after = None

# Open CSV file
with open(output_file, mode="a" if after else "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header only if starting fresh
    if not after:
        writer.writerow(["Post Title", "Post Author", "Post Upvotes", "Post URL", 
                         "Comment Author", "Comment Body", "Comment Upvotes"])

    # Fetch posts
    fetching = True
    while fetching:
        print(f"Fetching a batch of {batch_size} posts...")
        try:
            # Fetch posts using the after parameter for pagination
            posts = reddit.subreddit(subreddit_name).hot(limit=batch_size)
            last_post = None

            for post in posts:
                # Get the post's date
                post_date = datetime.utcfromtimestamp(post.created_utc)
                
                # Stop if post date is before the limit
                if post_date < date_limit:
                    print(f"Stopping: Post date {post_date} is earlier than {date_limit}")
                    fetching = False
                    break
                
                last_post = post
                print(f"Processing post: {post.title} (Date: {post_date})")

                # Fetch and write comments
                post.comments.replace_more(limit=0)  # Flatten nested comments
                for comment in post.comments.list():
                    comment_title = comment.body[:50]  # Adjust the number (50) as needed for length
                    print(f"Processing comment: {comment_title}...")
                    writer.writerow([
                        post.title, str(post.author), post.score, post.url,
                        str(comment.author), comment.body, comment.score
                    ])

            # Update the cursor
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
