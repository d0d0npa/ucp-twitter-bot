import random
import tempfile
import time
from typing import List
from typing import Optional

from mediawiki import MediaWiki
from mediawiki.mediawikipage import MediaWikiPage

from ucptwitbot import constant
from ucptwitbot import twitter_authentication
from ucptwitbot.ucp.ucp_article_select import UCPArticleSelectionStrategy
from ucptwitbot.util import create_image


class UcpTweet:
    """
    アンサイクロペディアに関することをツイートする
    """

    def __init__(self):
        self.twitter_client = twitter_authentication.set_authetication()
        self.ucp_ja_client = MediaWiki(url=constant.UCP_API)
        self.strategy = UCPArticleSelectionStrategy()

    def run(self):
        """
        ツイート処理
        """
        # MAX_SLEEP_TIME = 420.0

        # sleep_random(MAX_SLEEP_TIME)

        trend_article, hashtag = self.strategy.tweet_by_twitter_trend()
        if trend_article:
            self.tweet(trend_article, hashtags=[hashtag], with_image=True)
        else:
            random_article = self.strategy.choose_random_article()
            if random_article:
                self.tweet(random_article, with_image=True)

    def tweet(
        self,
        article: MediaWikiPage,
        hashtags: Optional[List[str]] = None,
        with_image: Optional[bool] = None,
    ) -> None:
        """
        該当記事をツイートする

        Args:
            article (MediaWikiPage): ツイートするアンサイクロペディアの記事
            hashtags (List[str]): ハッシュタグのリスト
            with_image(bool): イメージを付すか
        """
        SUMMARIZE_LENGTH_FOR_IMAGE = 100

        tweet_status = self.tweet_sentence(article)

        if hashtags:
            for tag in hashtags:
                tag = tag.removesuffix("!")
                tweet_status += f" #{tag}"

        print("Tweet : ", tweet_status)

        # Stable diffusionでイメージを生成
        media_ids = None
        if with_image:
            prompt = article.summarize(chars=SUMMARIZE_LENGTH_FOR_IMAGE)
            with tempfile.TemporaryDirectory() as tmp_dir:
                image_uri = create_image.generate_image_from_model(prompt)
                tmp_image_path = create_image.get_image(image_uri, tmp_dir)
                media = self.twitter_client.media_upload(filename=tmp_image_path)
                media_ids = [media.media_id]

            # ハッシュタグ追加
            image_hashtags = ["aiart", "aiartwork", "AIイラスト", "StableDiffusion"]
            for tag in image_hashtags:
                tweet_status += f" #{tag}"

        self.twitter_client.update_status(
            status=tweet_status, media_ids=media_ids
        )  # Twitterに投稿
        print("ツイート成功")

    def tweet_sentence(
        self,
        article: MediaWikiPage,
    ) -> str:
        """
        該当記事に関する内容のツイートする

        Args:
            article (MediaWikiPage): ツイートするアンサイクロペディアの記事

        Return:
            str: ツイートの内容
        """
        SUMMARIZE_LENGTH = 60

        # リンク先URLを取得する
        open_search_result = self.ucp_ja_client.opensearch(article.title, results=1)
        ucp_url = open_search_result[0][2]
        print("open search Result : ", ucp_url)

        # 要約文章を追加する
        tweet_status = (
            f"{article.title} {ucp_url}\n{article.summarize(chars=SUMMARIZE_LENGTH)}\n"
        )
        return tweet_status

    def generate_image_from_article(
        self,
        article: MediaWikiPage,
    ):
        """
        UCPの記事を基にイメージを生成する
        """
        pass


def sleep_random(max_sleep_time: float = 420.0) -> None:
    """uniformな確率で処理を一時停止する（投稿時間をランダムにするため）"""
    sleep_time = random.uniform(0, max_sleep_time)
    sleep_time = round(sleep_time, 3)
    print("sleep time : ", sleep_time)
    time.sleep(sleep_time)
