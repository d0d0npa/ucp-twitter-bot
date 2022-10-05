import json
import time

import tweepy

from ucp_twitter_bot import twitter_authentication


# 取得したいキーワード
SEARCH_WORD_LIST = ["アンサイクロペディア"]
# 取得ツイート数３件
TWEET_ACQUISITION_COUNT = 100
# 以下の文章のツイートはいいねしない
TWEET_BLACK_LIST = ["「天皇はピカチュウ」「国民の41％はオタクで53.2％は変態」…アンサイクロペディア英語版「Japan」の項が言いたい放題"]
# 以下のユーザーのツイートはいいねしない
USER_BLACK_LIST = [
    "NoMiyamakiMagic",
    "BotUcp",
    "Kitakou_Kuso",
    "bunsyo_bot",
    "15_ICG",
    "oppaibando",
]
# いいねを付与する間隔
SLEEP_TIME = 2


def favorite_tweet():
    api = twitter_authentication.set_authetication()
    search_result = []
    for search in SEARCH_WORD_LIST:
        print(f"Searching... {search}")
        # サーチ結果 #
        search_result.extend(
            api.search_tweets(
                q=search, count=TWEET_ACQUISITION_COUNT, result_type="recent"
            )
        )

    favorite_tweet_list = []
    for tweet in search_result:
        ok_tweet_flag = True
        # 意図的にボットっぽい返信をするものはスルーする
        for i_black in TWEET_BLACK_LIST:
            if tweet.text == i_black:
                ok_tweet_flag = False
        # 特定のユーザーは除外する
        for i_black in USER_BLACK_LIST:
            if tweet.user.screen_name == i_black:
                ok_tweet_flag = False

        # いいね済はスルーする(そもそも、この項目なのか謎)
        print("いいね済: ", tweet.favorited)
        if tweet.favorited:
            ok_tweet_flag = False

        if ok_tweet_flag:
            favorite_tweet_list.append(tweet)

    for tweet in favorite_tweet_list:
        try:
            # いいねの処理 #
            api.create_favorite(id=tweet.id)
        # いいね済の場合はForbiddenされるので、ここで例外処理を行う
        except tweepy.errors.Forbidden as err:
            print(err)
        except Exception as err:
            print(err)
            raise err
        else:
            print("Tweet_liked")
            print(json.dumps(tweet._json, indent=2))

            print("Created: ", tweet.created_at)
            print("user :", tweet.user.name)
            print("screen name: ", tweet.user.screen_name)
            print("text :", tweet.text)
            time.sleep(SLEEP_TIME)


##########################################################################
# いいねは２４時間で１０００件まで。１０００件以上いいねをするとペナルティを受けます。 #
#######################################################################
