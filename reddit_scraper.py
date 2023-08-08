import os
import praw
from dotenv import load_dotenv
from utilities import *
import json


load_dotenv()

reddit_read_only = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),  # your client id
    client_secret=os.getenv("CLIENT_SECRET"),  # your client secret
    user_agent=os.getenv("USER_AGENT"),
)  # your user agent

subreddit = reddit_read_only.subreddit("thewallstreet")

top_posts = subreddit.hot(limit=5)

# submission_ids = get_todays_post(top_posts=top_posts, daily_post_type="Daily")

for submission_id in top_posts:
    submission_cls = reddit_read_only.submission(id=submission_id)
    comments_to_write = comments_to_dataframe(submission=submission_cls)
    if not comments_to_write.empty:

    
        write_dataframe_to_postgres(
            dataframe=comments_to_write,
            db_username = os.getenv("POSTGRES_USER"),
            db_password = os.getenv("POSTGRES_PASSWORD"),
            db_host = "postgres",  # The service name defined in the docker-compose.yml file
            db_port = "5432",
            db_name = "scraperdb"
            )
