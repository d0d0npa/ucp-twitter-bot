import os

from dotenv import load_dotenv
import tweepy


load_dotenv(verbose=True)

dotenv_path = os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".env")
load_dotenv(dotenv_path)


def set_authetication():
    """
    アクセストークンを利用して認証を行う
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    # wait_on_rate_limit = レート制限が補充されるのを自動的に待つかどうか
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api
