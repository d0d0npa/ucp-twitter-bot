import base64

import functions_framework

from ucp_twitter_bot.ucp_favorite_tweet import favorite_tweet
from ucp_twitter_bot.ucp_follower import following_follower_from_follower_list
from ucp_twitter_bot.ucp_tweet import tweet_from_random_article


@functions_framework.cloud_event
def function(cloud_event):
    print(
        "Message from pub-sub, "
        + base64.b64decode(cloud_event.data["message"]["data"]).decode()
        + "!"
    )
    favorite_tweet()
    tweet_from_random_article()


@functions_framework.cloud_event
def daily(cloud_event):
    print(
        "Message from pub-sub, "
        + base64.b64decode(cloud_event.data["message"]["data"]).decode()
        + "!"
    )
    following_follower_from_follower_list()
