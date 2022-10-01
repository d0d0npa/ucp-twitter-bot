# -*- coding: utf_8 -*-

import os
import sys
import urllib.request
from urllib.parse import urlparse
import tweepy
from ucp_twitter_bot import twitter_authentication

class ReplyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #print(status)
        api = twitter_authentication.set_authetication()
        ## 挨拶するとハローと返信する
        if ('こんにちは' in status.text or 'こんにちわ' in status.text):
            tweet_status = ""
            tweet_status = '@' + status.user.screen_name + '\n' + ' ハロー'
            api.update_status(status=tweet_status,in_reply_to_status_id = status.id_str)
    def checkTweetType(self, status):
        if ("retweeted_status" in status._json.keys()):
            type_ = "retweet"
        elif status.in_reply_to_user_id != None:
            type_ = "reply"
        else:
            type_ = "normal"
        self.type = type_
if __name__ == "__main__":
    api = twitter_authentication.set_authetication()

    #フォロワーのツイートをみる
    followee_ids = api.friends_ids(screen_name=api.me().screen_name)
    watch_list = [str(user_id) for user_id in followee_ids]
    watch_list.append(str(api.me().id))

    myStreamListener = ReplyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    #myStream.filter(follow=watch_list)
    myStream.filter(track=['@BotUcp'])