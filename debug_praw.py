import praw
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Define parameters
subreddit_name = "buildapc"
batch_size = 1  # Number of posts to fetch per batch
wait_time = 300  # Time to sleep between batches (in seconds)
output_file = "reddit_comments1.csv"
 # Stop fetching posts older than this date
# cursor_file = "reddit_cursor.json"

subreddit = reddit.subreddit(subreddit_name)
while True:
    post = subreddit.hot(limit = batch_size)
    last_post = None
    # print(last_post)
    for post in post:
        last_post = post
        after = last_post.name
        print(after)