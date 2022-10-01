import tweepy
from mediawiki import MediaWiki
import os
from ucp_twitter_bot import twitter_authentication

if __name__ == "__main__":
    api = twitter_authentication.set_authetication()

    ucp_ja = MediaWiki(url='https://ansaikuropedia.org/api.php')
    random_pages = ucp_ja.random(pages=10)
    print("Selected Pages : ",random_pages)

    # ランダムに記事を選択し、条件に合致するページを選択する
    selected_page = ''
    for i_page_title in random_pages:
        selected_flag = True
        i_page = ucp_ja.page(i_page_title)
        # 「どうしようもない記事」、「カテゴリ日記」と「曖昧さ回避」に属する記事は削除する
        nrv_categories = ['カテゴリ:どうしようもない記事',
                        'カテゴリ:修正が必要な記事',
                        'カテゴリ:拡張が必要な記事',
                        'カテゴリ:要添削',
                        'カテゴリ:ユーモアの足りない記事',
                        'カテゴリ:即時削除',
                        'カテゴリ:削除議論中のページ']
        remove_categories = nrv_categories
        remove_categories.append('カテゴリ:日記/過去ログ')
        remove_categories.append('カテゴリ:曖昧さ回避')
        if(not set(remove_categories).isdisjoint(set(i_page.categories))):
            selected_flag = False
        if(selected_flag):
            selected_page = i_page
            break

    open_search_result = ucp_ja.opensearch(selected_page.title, results=1)
    print("open search Result : ", open_search_result[0][2])

    page = ucp_ja.page(selected_page.title)

    tweet_status = ""
    tweet_status += page.title + ' ' + \
        open_search_result[0][2] + '\n' + \
        page.summarize(chars=60)

    print("Tweet : " , tweet_status)
    print("Images : ", page.images[0])
    #api.update_with_media(status=tweet_status, filename = page.images[0])
    api.update_status(status=tweet_status) #Twitterに投稿
    print("ツイート成功")
