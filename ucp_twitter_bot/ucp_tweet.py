import random
import time

from mediawiki import MediaWiki

from ucp_twitter_bot import twitter_authentication


def tweet_from_random_article() -> None:
    api = twitter_authentication.set_authetication()

    ucp_ja = MediaWiki(url="https://ansaikuropedia.org/api.php")
    random_pages = ucp_ja.random(pages=10)
    print("Selected Pages : ", random_pages)

    # ランダムに記事を選択し、条件に合致するページを選択する
    selected_page = ""
    for i_page_title in random_pages:
        selected_flag = True
        i_page = ucp_ja.page(i_page_title)
        # 「どうしようもない記事」、「カテゴリ日記」と「曖昧さ回避」に属する記事は削除する
        remove_categories = [
            "カテゴリ:どうしようもない記事",
            "カテゴリ:修正が必要な記事",
            "カテゴリ:拡張が必要な記事",
            "カテゴリ:要添削",
            "カテゴリ:ユーモアの足りない記事",
            "カテゴリ:即時削除",
            "カテゴリ:削除議論中のページ",
            "カテゴリ:日記/過去ログ",
            "カテゴリ:曖昧さ回避",
        ]
        if not set(remove_categories).isdisjoint(set(i_page.categories)):
            selected_flag = False
        if selected_flag:
            selected_page = i_page
            break

    # リンク先URLを取得する
    open_search_result = ucp_ja.opensearch(selected_page.title, results=1)
    print("open search Result : ", open_search_result[0][2])

    page = ucp_ja.page(selected_page.title)

    tweet_status = ""
    tweet_status += (
        page.title + " " + open_search_result[0][2] + "\n" + page.summarize(chars=60)
    )

    print("Tweet : ", tweet_status)

    sleep_random()

    # TODO: 画像の取得
    # print("Images : ", page.images[0])
    # api.update_with_media(status=tweet_status, filename = page.images[0])
    api.update_status(status=tweet_status)  # Twitterに投稿
    print("ツイート成功")


def sleep_random() -> None:
    """uniformな確率で処理を一時停止する（投稿時間をランダムにするため）"""
    sleep_time = random.uniform(0, 500)
    sleep_time = round(sleep_time, 3)
    print("sleep time : ", sleep_time)
    time.sleep(sleep_time)
