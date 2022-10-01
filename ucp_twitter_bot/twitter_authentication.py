import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True)

dotenv_path = os.path.join(os.path.join(os.path.dirname(__file__), '..'), '.env')
load_dotenv(dotenv_path)

def set_authetication():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # wait_on_rate_limit = レート制限が補充されるのを自動的に待つかどうか #
    # wait_on_rate_limit_notify = Tweepyがレート制限の補充を待っているときに通知を出力するかどうか #
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return (api)
