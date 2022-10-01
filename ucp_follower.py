import tweepy
import os

from ucp_twitter_bot import twitter_authentication

api = twitter_authentication.set_authetication()

for follower in tweepy.Cursor(api.followers).items():
    print(f"Check Follower: {follower.name}")
    if not follower.following:
        print(f"Following {follower.name}")
        follower.follow()

# フォローした人のIDを全取得
'''
for friend_id in tweepy.Cursor(api.friends).items():
    print(f"Check Friends :  {friend_id.name}")
    friendship = api.show_friendship(source_id = friend_id.id, target_id =api.me().id)
    #相手(friendship[0])はフォローしてないが、自分(friendship[1])がフォローしている場合
    if (not vars(friendship[0])['following'] and 
        vars(friendship[1])['following'] ):
        print(f"Unfollow : {friend_id.name}")
        api.destroy_friendship(friend_id.id)
'''