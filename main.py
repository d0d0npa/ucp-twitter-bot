import base64

import functions_framework

from ucptwitbot import ucp_tweet
from ucptwitbot.ucp_favorite_tweet import favorite_tweet
from ucptwitbot.ucp_follower import following_follower_from_follower_list


@functions_framework.cloud_event
def function(cloud_event):
    print(
        "Message from pub-sub, "
        + base64.b64decode(cloud_event.data["message"]["data"]).decode()
        + "!"
    )
    favorite_tweet()
    ucp_tweet_client = ucp_tweet.UcpTweet()
    ucp_tweet_client.run()


@functions_framework.cloud_event
def daily(cloud_event):
    print(
        "Message from pub-sub, "
        + base64.b64decode(cloud_event.data["message"]["data"]).decode()
        + "!"
    )
    following_follower_from_follower_list()
