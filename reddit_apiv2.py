import praw
import datetime

def initialize_reddit():
    """Initialize the Reddit API client using PRAW."""
    return praw.Reddit(
        client_id="FhBxNA6ffJLwbIzvANW0OA",
        client_secret="G_ZiIfzNayDoIFChj5TTw2CAaezY3Q",
        user_agent="AbleFloor5710/1.0 by u/AbleFloor5710"
    )

def fetch_all_posts(reddit, subreddit_name):
    """Fetch all posts from the beginning of the subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    post_data = []
    first_post = None
    
    for index, submission in enumerate(subreddit.new(limit=None)):  # Fetch posts from the beginning
        human_readable_date = datetime.datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        post_info = {
            'title': submission.title,
            'created_utc': human_readable_date
        }
        post_data.append(post_info)
        
        if index == 0:
            first_post = post_info  # Store the very first post
    
    return post_data, first_post

def display_posts(post_data, first_post):
    """Display the fetched posts with their creation dates, printing the first post at the end."""
    total_posts = len(post_data)
    
    for post in post_data[1:]:  # Print all posts except the first one
        print(f"Title: {post['title']}")
        print(f"Posted Date (UTC): {post['created_utc']}")
        print("-" * 50)
    
    if first_post:
        print("\nFirst Post in Subreddit:")
        print(f"Title: {first_post['title']}")
        print(f"Posted Date (UTC): {first_post['created_utc']}")
        print("-" * 50)
    
    print(f"Total Posts: {total_posts}")

def main():
    """Main function to execute the script."""
    reddit = initialize_reddit()
    subreddit_name = 'buildapc'
    post_data, first_post = fetch_all_posts(reddit, subreddit_name)
    display_posts(post_data, first_post)

if __name__ == "__main__":
    main()