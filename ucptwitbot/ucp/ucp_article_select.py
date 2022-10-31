from datetime import datetime
from datetime import timezone
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

from mediawiki import MediaWiki
from mediawiki.exceptions import PageError
from mediawiki.mediawikipage import MediaWikiPage

from ucptwitbot import constant
from ucptwitbot import twitter_authentication
from ucptwitbot.ucp import ucp_utils


class UCPArticleSelectionStrategy:
    """
    UCPの記事を選ぶアルゴリズム
    """

    # 日本のWOEID
    JP_WOEID = 23424856

    def __init__(self):
        self.twitter_client = twitter_authentication.set_authetication()
        self.ucp_ja_client = MediaWiki(url=constant.UCP_API)

    def choose_random_article(self) -> Union[MediaWikiPage, None]:
        """
        アンサイクロペディアよりランダムに記事を取得する

        Returns:
            str: 選ばれた記事
        """
        N_RANDOM_PAGES = 10
        while True:
            random_pages = self.ucp_ja_client.random(pages=N_RANDOM_PAGES)
            print("Selected Pages : ", random_pages)

            articles_list = [
                article for article in random_pages if self._article_exists(article)
            ]

            # 特定のカテゴリに属する記事を除外する
            articles_list = self._remove_certain_category_article_from_list(
                articles_list,
            )

            # ツイート投稿履歴を調べ、20件以内に同じ記事を投稿していないか調べる
            # 投稿していた場合はツイートしない
            articles_list = self._check_duplicated_tweet(ucp_article_list=articles_list)

            if len(articles_list) > 0:
                print("UCP article was chosen")
                break

        return articles_list[0]

    def tweet_by_twitter_trend(self) -> Sequence[Union[MediaWikiPage, str, None]]:
        """
        Twitterのトレンド（日本）を取得し、それに合致するアンサイクロペディアの記事が
        存在した場合、その記事を返す。

        Returns:
            chosen_article(MediaWikiPage) :
                もし該当するページが見つかった場合はその記事のタイトルを返す。
                該当する記事が見つからなかった場合はNoneを返す
            trend (str) :
                該当記事のハッシュタグ
        """
        # TODO: print文の内容が適当なので修正した方が良い

        # トレンド一覧取得（地域:日本）
        trends = self.twitter_client.get_place_trends(self.JP_WOEID)[0]["trends"]
        # ハッシュタグを取り除く
        trends_list = [trend["name"].removeprefix("#") for trend in trends]
        print("Trend list : ", trends_list)

        # アンサイクロペディアの記事にトレンドにのった言葉が存在するか調べる
        ucp_trend_article_list = [
            trend for trend in trends_list if self._article_exists(trend)
        ]

        print("UCP Article list : ", ucp_trend_article_list)
        if len(ucp_trend_article_list) == 0:
            print("No UCP article match with Trend")
            return None, None

        # トレンドと記事の対応関係を示す辞書を作成する
        trend_ucp_article_dict = {
            self.ucp_ja_client.page(title).title: title
            for title in ucp_trend_article_list
        }

        # NRVなどではないか確認
        ucp_article_list: List[MediaWikiPage] = []
        ucp_article_list = self._remove_certain_category_article_from_list(
            ucp_trend_article_list
        )

        if len(ucp_trend_article_list) == 0:
            print("UCP article was NRV")
            return None, None

        # アンサイクロペディアの記事が作成されて24時間以内の場合は除外する
        prev_ucp_article_list = ucp_article_list
        ucp_article_list = []
        for article in prev_ucp_article_list:
            created_datetime = ucp_utils.article_created_time(article.title)
            time_passed = datetime.now(timezone.utc) - created_datetime
            if time_passed.days > 0:
                ucp_article_list.append(article)

        print("Articles that have passed enough time: ", ucp_article_list)

        if len(ucp_article_list) == 0:
            print("UCP article was too recent")
            return None, None

        # ツイート投稿履歴を調べ、20件以内に同じ記事を投稿していないか調べる
        # 投稿していた場合はツイートしない
        ucp_article_list = self._check_duplicated_tweet(
            ucp_article_list=ucp_article_list
        )

        print("Not duplicated tweet article: ", ucp_article_list)

        if len(ucp_article_list) == 0:
            print("UCP article already tweeted")
            return None, None

        chosen_article = ucp_article_list[0]
        trend = trend_ucp_article_dict[chosen_article.title]

        return (chosen_article, str(trend))

    def _remove_certain_category_article_from_list(
        self,
        article_list: Union[List[MediaWikiPage], List[str]],
        results: Optional[int] = None,
    ) -> List[MediaWikiPage]:
        """
        特定のカテゴリに属する記事は除外する
        constant.REMOVE_CATEGORIESに属する記事は除外される

        Args:
            article_list (List[MediaWikiPage]): 記事のリスト
            results (int) : Optional. Number of max random pages to return
        Returns:
            List[MediaWikiPage]: 特定のカテゴリが除外された記事
        """

        REMOVE_CATEGORIES = [
            "カテゴリ:どうしようもない記事",
            "カテゴリ:修正が必要な記事",
            "カテゴリ:拡張が必要な記事",
            "カテゴリ:要添削",
            "カテゴリ:ユーモアの足りない記事",
            "カテゴリ:即時削除",
            "カテゴリ:削除議論中のページ",
            "カテゴリ:日記/過去ログ",
            "カテゴリ:しりとり過去ログ",
            "カテゴリ:しりとり部屋/フリー部屋/過去ログ",
            "カテゴリ:しりとり部屋/3文字部屋/過去ログ",
            "カテゴリ:しりとり部屋/5文字部屋/過去ログ",
            "カテゴリ:しりとり部屋/8文字以上部屋/過去ログ",
            "カテゴリ:しりとり部屋/地名･駅名部屋/過去ログ",
            "カテゴリ:しりとり部屋/ことわざ・四字熟語部屋/過去ログ",
            "カテゴリ:しりとり部屋/フリー部屋 (プロ)/過去ログ",
            "カテゴリ:しりとり部屋/生き物部屋/過去ログ",
            "カテゴリ:しりとり部屋/食べ物部屋/過去ログ",
            "カテゴリ:曖昧さ回避",
        ]

        return_list: List[MediaWikiPage] = []

        # 条件に合致する記事を調べる
        for i_page_title in article_list:
            selected_flag = True
            try:
                i_page = self.ucp_ja_client.page(i_page_title)
            except PageError:
                continue

            # 「どうしようもない記事」、「カテゴリ日記」と「曖昧さ回避」に属する記事は削除する
            if not set(REMOVE_CATEGORIES).isdisjoint(set(i_page.categories)):
                selected_flag = False
            if selected_flag:
                return_list.append(i_page)
            if results:
                if len(return_list) >= results:
                    break

        print("excluded NRVs : ", return_list)

        return return_list

    def _article_exists(self, title: str) -> bool:
        """
        アンサイクロペディアの記事が存在するか

        Returns:
            bool : 存在しない場合はFalseを返す。
        """
        try:
            self.ucp_ja_client.page(title)
        except PageError:
            return False
        else:
            return True

    def _check_duplicated_tweet(
        self, counts: int = 20, ucp_article_list: List[MediaWikiPage] = None
    ) -> List[MediaWikiPage]:
        """
        直近の投稿と同じ記事を投稿していないかチェックする
        同じ記事を投稿していた場合は除外する

        Args:
            counts (int): 投稿数。5ならば直近5件を調べる
            ucp_article_list (List[MediaWikiPage]): 調査するUCPの記事のリスト
        Returns:
            List[MediaWikiPage] :
        """
        # ツイート投稿履歴を調べ、同じ記事を投稿していないか調べる
        # 投稿していた場合はツイート対象に含めない
        user_timeline = self.twitter_client.user_timeline(count=counts)
        ucp_tweeted_article_links = []
        for tweet in user_timeline:
            # @BotUCPはリンク先は一つしか貼らないので一つ目のリンクは必ずUCPのリンクとなる
            article_link = tweet.entities["urls"][0]["expanded_url"]
            ucp_tweeted_article_links.append(article_link)

        if ucp_article_list is None:
            raise ValueError("`ucp_article_list` is None")

        result_article = []
        for article in ucp_article_list:
            # Twitterの仕様として最後尾の「!」はリンクとして認識されない
            # そのパターンも除外する（例: ラブライブ!）
            url = article.url
            url = url.removesuffix("!")
            if not (url in ucp_tweeted_article_links):
                result_article.append(article)
        return result_article
