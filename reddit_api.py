import praw

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id="your_client_id",           # Replace with your client ID
    client_secret="your_client_secret",   # Replace with your client secret
    user_agent="your_user_agent"          # Replace with a descriptive user agent
)

# Fetch a specific subreddit and post
subreddit_name = "learnpython"
post_id = "post_id_here"  # Example: '12345abc'

# Get the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Fetch a post by ID
post = reddit.submission(id=post_id)

# Print post details
print(f"Title: {post.title}")
print(f"Author: {post.author}")
print(f"Upvotes: {post.score}")
print(f"URL: {post.url}")
print(f"Content: {post.selftext}")

# Fetch comments
post.comments.replace_more(limit=0)  # Flatten comment tree
for comment in post.comments.list():
    print(f"Comment by {comment.author}: {comment.body}")
