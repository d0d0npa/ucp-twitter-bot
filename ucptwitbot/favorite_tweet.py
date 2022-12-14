import time

import tweepy

from ucptwitbot import twitter_authentication


# 取得したいキーワード
SEARCH_WORD_LIST = ["アンサイクロペディア"]
# 取得ツイート数
TWEET_ACQUISITION_COUNT = 100
# 以下の文章のツイートはいいねしない
TWEET_BLACK_LIST = [
    "「天皇はピカチュウ」「国民の41％はオタクで53.2％は変態」…アンサイクロペディア英語版「Japan」の項が言いたい放題",
    "「天皇はピカチュウ」？「国民の41％はオタクで53.2％は変態？」…アンサイクロペディア英語版「Japan」の項が言いたい放題だ！",
    "「天皇はピカチュウ」「国民の41％はオタクで53.2％は変態」…アンサイクロペディア英語版では「Japan」のことがカオスになってる件。。。",
]
# 以下のユーザーのツイートはいいねしない
USER_BLACK_LIST = [
    "NoMiyamakiMagic",
    "BotUcp",
    "Kitakou_Kuso",
    "bunsyo_bot",
    "15_ICG",
    "oppaibando",
    "hitominpin",
    "nagisa_1993",
    "urako_bot",
    "kuso_shindai",
    "hentaigen_bot",
    "rikadai3",
    "A_hitler_bot",
    "nappa__GOD",
]
# 以下のソースのツイートはいいねしない
SOURCE_BLACK_LIST = [
    "twittbot.net",
    "Peing",
    "Botbird tweets",
]

# いいねを付与する間隔
SLEEP_TIME = 2


def favorite_tweet():
    """
    「アンサイクロペディア」に言及した場合はいいねを付与する
    """
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
        # ボット投稿はスルーする
        for i_black in SOURCE_BLACK_LIST:
            if tweet.source == i_black:
                ok_tweet_flag = False
        # 意図的にボットっぽい返信をするものはスルーする
        for i_black in TWEET_BLACK_LIST:
            if tweet.text == i_black:
                ok_tweet_flag = False
        # 特定のユーザーは除外する
        for i_black in USER_BLACK_LIST:
            if tweet.user.screen_name == i_black:
                ok_tweet_flag = False

        # いいね済はスルーする(そもそも、この項目なのか謎)
        if tweet.favorited:
            ok_tweet_flag = False

        if ok_tweet_flag:
            favorite_tweet_list.append(tweet)

    for tweet in favorite_tweet_list:
        try:
            # いいねの処理
            api.create_favorite(id=tweet.id)
        except tweepy.errors.Forbidden:
            # いいね済の場合はForbiddenされるので、ここで例外処理を行う
            # 調べる数が多いのでerror文をprintせず、ツイート内容だけ表示
            print("Faved Created: ", tweet.created_at)
            print("Faved tweet: ", tweet.text)
            time.sleep(SLEEP_TIME)
        except tweepy.errors.Unauthorized as err:
            # ブロックされた場合Unauthorizedと出るので例外処理を行う
            # 本当の権限不足かは注意
            # TODO: ちゃんとしたロガーを実装する
            print("Error Message: \n", err)
            print("user :", tweet.user.screen_name)
            print("text :", tweet.text)
            time.sleep(SLEEP_TIME)
        except Exception as err:
            print(err)
            raise err
        else:
            print("Tweet_liked")
            # print(json.dumps(tweet._json, indent=2))

            print("Created: ", tweet.created_at)
            print("user :", tweet.user.name)
            print("screen name: ", tweet.user.screen_name)
            print("text :", tweet.text)
            time.sleep(SLEEP_TIME)


##########################################################################
# いいねは２４時間で１０００件まで。１０００件以上いいねをするとペナルティを受けます。 #
#######################################################################
