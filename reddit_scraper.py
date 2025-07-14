from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import praw
import prawcore

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit client using praw
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_user_data(username):
    try:
        user = reddit.redditor(username)

        # Fetch basic profile data 
        icon_img = ""
        try:
            icon_img = user.icon_img
        except prawcore.exceptions.NotFound:
            print(f" Could not fetch profile picture for {username}.")
        except Exception as e:
            print(f" Unexpected error while getting icon_img: {e}")

        submissions = []
        comments = []

        media_domains = ["i.redd.it", "imgur.com", "v.redd.it", "youtube.com", "youtu.be", "gfycat.com"]
        image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        video_extensions = [".mp4", ".webm"]

        try:
            for post in user.submissions.new(limit=20):
                media_info = ""

                if hasattr(post, "post_hint") and post.post_hint in ["image", "hosted:video", "rich:video"]:
                    media_info = f" [Media: {post.url}]"

                if any(post.url.lower().endswith(ext) for ext in image_extensions + video_extensions):
                    media_info = f" [Media: {post.url}]"

                domain = urlparse(post.url).netloc
                if any(media_domain in domain for media_domain in media_domains):
                    media_info = f" [External Media: {post.url}]"

                full_post = f"{post.title} - {post.selftext}{media_info}"
                submissions.append(full_post.strip())
        except prawcore.exceptions.NotFound:
            print(f" Could not fetch submissions for {username} (may be private or deleted).")
        except Exception as e:
            print(f" Error while fetching submissions: {e}")

        try:
            for comment in user.comments.new(limit=50):
                comments.append(comment.body.strip())
        except prawcore.exceptions.NotFound:
            print(f" Could not fetch comments for {username} (may be private or deleted).")
        except Exception as e:
            print(f" Error while fetching comments: {e}")

        return {
            "username": username,
            "icon_img": icon_img,
            "submissions": submissions,
            "comments": comments
        }

    except prawcore.exceptions.NotFound:
        print(f" Reddit user '{username}' not found or is fully private/banned.")
        return {
            "username": username,
            "icon_img": "",
            "submissions": [],
            "comments": []
        }
