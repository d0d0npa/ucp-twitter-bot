import time

import tweepy

from ucp_twitter_bot import twitter_authentication


api = twitter_authentication.set_authetication()

# 'アンサイクロペディア'を３件ずついいね #
# 取得したいキーワード #
search_list = ["アンサイクロペディア"]
# ツイート数３件 #
tweet_count = 3
search = "アンサイクロペディア"
for search in search_list:
    print("Searching... {}".format(search))
    # サーチ結果 #
    search_result = api.search(q=search, count=tweet_count, result_type="recent")

    for tweet in search_result:
        ng_tweet_flag = False
        # 意図的にボットっぽい返信をするものはスルーする
        TWEET_BLACK_LIST = [
            "「天皇はピカチュウ」「国民の41％はオタクで53.2％は変態」…" + "アンサイクロペディア英語版「Japan」の項が言いたい放題"
        ]
        for i_black in TWEET_BLACK_LIST:
            if tweet.text == i_black:
                ng_tweet_flag = True
        # 特定のユーザーは除外する
        USER_BLACK_LIST = ["NoMiyamakiMagic"]
        for i_black in USER_BLACK_LIST:
            if tweet.user == i_black:
                ng_tweet_flag = True
        tweet_id = tweet.id
        try:
            # いいねの処理 #
            api.create_favorite(id=tweet_id)
            print("Tweet_liked")
            time.sleep(4)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

##########################################################################
# いいねは２４時間で１０００件まで。１０００件以上いいねをするとペナルティを受けます。 #
#######################################################################
