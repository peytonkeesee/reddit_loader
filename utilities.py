import datetime
import pandas as pd
from sqlalchemy import create_engine


def get_todays_formatted_date():
    today = datetime.datetime.today()
    date_format = "%B %d, %Y"
    return today.strftime(date_format)


def get_todays_post(top_posts, daily_post_type):
    search_string = f"{daily_post_type} Discussion - ({get_todays_formatted_date()})"
    for post in top_posts:
        if post.title == search_string:
            return post


def process_comments(submission, comment, parent_id=None):
    comment_data = {
        "post_title": submission.title,
        "parent_id": parent_id,
        "comment_id": comment.id,
        "author": comment.author.name if comment.author else None,
        "body": comment.body
    }
    replies = []
    for reply in comment.replies:
        replies.extend(process_comments(submission, reply, parent_id=comment.id))
    return [comment_data] + replies



def comments_to_dataframe(submission):
    comments_data = []

    # Iterate through top-level comments of the submission
    for top_level_comment in submission.comments:
        comment_data = process_comments(submission, top_level_comment)
        comments_data.extend(comment_data)
    return pd.json_normalize(comments_data, sep="_")


def write_dataframe_to_postgres(
    dataframe, db_username, db_password, db_host, db_port, db_name
):
    db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    print(db_url)
    engine = create_engine(db_url)
    dataframe.to_sql("the_wall_street", con=engine, if_exists="replace", index=False)
    print("Data written to PostgreSQL database.")
  