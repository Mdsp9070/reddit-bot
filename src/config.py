import praw
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("APP_ID"),
    client_secret=os.getenv("APP_SECRET"),
    password=os.getenv("PASS"),
    username=os.getenv("ME"),
    user_agent="word-count bot by /u/Mdsp9070"
)
