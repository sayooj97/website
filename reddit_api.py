import praw
import csv

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Fetch a specific subreddit and post
subreddit_name = "GadgetsIndia"
# post_id = "1i9g6nr"  # Example: '12345abc'
# post_id = reddit.subreddit()

# Get the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Fetch a post by ID
# post = reddit.submission(id=post_id)
posts = []

# Print post details
for post in subreddit.hot(limit=50):
     posts.append({
        "Title": post.title,
        "Author": str(post.author),
        "Upvotes": post.score,
        "Comments Count": post.num_comments,
        "Post URL": post.url,
        "Content": post.selftext,
    })

save_file = "reddit_comments.csv"

with open(save_file, mode="w", newline="",encoding="utf-8") as file:
    writer = csv.DictWriter(file,fieldnames=["Title", "Author", "Upvotes", "Comments Count", "Post URL", "Content"])
    writer.writeheader()
    writer.writerows(posts)

print(f"saved {len(posts)} post to {save_file}")
# Fetch comments
# post.comments.replace_more(limit=0)  # Flatten comment tree
# for comment in post.comments.list():
#     print(f"Comment by {comment.author}: {comment.body}")
