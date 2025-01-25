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

# Define parameters
subreddit_name = "buildapc"
batch_size = 5  # Number of posts to fetch per batch
wait_time = 5  # Time to sleep between batches (in seconds)
output_file = "reddit_comments.csv"
date_limit = datetime(2023, 12, 31)  # Stop fetching posts older than this date
cursor_file = "reddit_cursor.json"

try:
    with open(cursor_file, "r") as f:
        resume_data = json.load(f)
        after = resume_data.get("after", None)
        print(f"Resuming from after={after}")
except FileNotFoundError:
    after = None  # Start fresh if no cursor file is found

# Open the CSV file for appending (if resuming) or writing (if fresh start)
with open(output_file, mode="a" if after else "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header row only if starting fresh
    if not after:
        writer.writerow(["Post Title", "Post Author", "Post Upvotes", "Post URL", "Post Content", 
                         "Comment Author", "Comment Body", "Comment Upvotes"])
    
    # Fetch posts in batches
    subreddit = reddit.subreddit(subreddit_name)
    fetching = True

    while fetching:
        print(f"Fetching a batch of {batch_size} posts...")
        posts = subreddit.hot(limit=batch_size, params={"after": after})
        
        for post in posts:
            # Convert post's creation time to a datetime object
            post_date = datetime.utcfromtimestamp(post.created_utc)
            
            # Stop fetching if the post's date is older than the limit
            if post_date < date_limit:
                print(f"Stopping: Post date {post_date} is earlier than {date_limit}")
                fetching = False
                break
            
            print(f"Processing post: {post.title} (Date: {post_date})")

            # Fetch and flatten comments
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
                comments.append({
                    "Comment Author": str(comment.author),
                    "Comment Body": comment.body,
                    "Comment Upvotes": comment.score
                })
            
            # Write post and comments to CSV
            for comment in comments:
                writer.writerow([
                    post.title, str(post.author), post.score, post.url, post.selftext,
                    comment["Comment Author"], comment["Comment Body"], comment["Comment Upvotes"]
                ])
            
            # Save the pagination cursor
            after = post.name

        # Save the current cursor to the cursor file
        with open(cursor_file, "w") as f:
            json.dump({"after": after}, f)
        
        if fetching:
            print(f"Batch completed. Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)  # Sleep before fetching the next batch

print(f"Saved posts and comments to {output_file}")