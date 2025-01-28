import praw
import csv
import time

# Step 1: Set up Reddit API client
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Step 2: Choose the subreddit you want to scrape
wait_time = 5
subreddit_name = 'buildapc'  # Replace with the subreddit you're interested in
subreddit = reddit.subreddit(subreddit_name)

# Step 3: Open a CSV file to write the data
with open('reddit_comments.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Post Title', 'Comment ID', 'Comment Body', 'Comment Author'])  # CSV headers

    # Step 4: Loop through the posts and extract comments
    for submission in subreddit.new(limit=None):  # Adjust the limit as needed
        print(f"Fetching comments for post: {submission.title}")
        
        # Iterate over all comments in the post
        submission.comments.replace_more(limit=0)  # Avoiding 'MoreComments' objects
        for comment in submission.comments.list():
            writer.writerow([submission.title, comment.id, comment.body, comment.author])
        print(f"sleeping for {wait_time}")
        time.sleep(wait_time)

print("Comments have been saved to 'reddit_comments.csv'.")
