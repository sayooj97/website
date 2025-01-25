import praw
import csv

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id="FhBxNA6ffJLwbIzvANW0OA",
    client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
    user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
)

# Fetch a specific subreddit and post
subreddit_name = "buildapc"
# post_id = "1i9g6nr"  # Example: '12345abc'
# post_id = reddit.subreddit()

# Get the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Fetch a post by ID
# post = reddit.submission(id=post_id)
posts = []
for post in subreddit.hot(limit=5):  # Change limit as needed
    print(f"Fetching comments for post: {post.title}")

    # Step 4: Fetch comments
    post.comments.replace_more(limit=0)  # Flatten the comment tree
    comments = []
    for comment in post.comments.list():  # Get all comments as a flat list
        comments.append({
            "Comment Author": str(comment.author),
            "Comment Body": comment.body,
            "Comment Upvotes": comment.score
        })

    # Append post details and comments to the list
    posts.append({
        "Post Title": post.title,
        "Post Author": str(post.author),
        "Post Upvotes": post.score,
        "Post URL": post.url,
        "Post Content": post.selftext,
        "Comments": comments
    })


save_file = "reddit_comments.csv"

# with open(save_file, mode="w", newline="",encoding="utf-8") as file:
#     writer = csv.DictWriter(file,fieldnames=["Title", "Author", "Upvotes", "Comments Count", "Post URL", "Content"])
#     writer.writeheader()
#     writer.writerows(posts)

# print(f"saved {len(posts)} post to {save_file}")
# Fetch comments
# post.comments.replace_more(limit=0)  # Flatten comment tree
# for comment in post.comments.list():
#     print(f"Comment by {comment.author}: {comment.body}")
with open(save_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Post Title", "Post Author", "Post Upvotes", "Post URL", "Post Content", "Comment Author", "Comment Body", "Comment Upvotes"])
    
    # Write each post and its comments
    for post in posts:
        for comment in post["Comments"]:
            writer.writerow([
                post["Post Title"], post["Post Author"], post["Post Upvotes"], post["Post URL"], post["Post Content"],
                comment["Comment Author"], comment["Comment Body"], comment["Comment Upvotes"]
            ])

print(f"Saved posts and comments to {save_file}")