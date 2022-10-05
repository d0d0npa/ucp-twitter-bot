## UCP BOT

### 使用パッケージ
- [tweepy](http://docs.tweepy.org/en/latest/index.html)
- [MediaWiki](https://pymediawiki.readthedocs.io/en/latest/index.html)

## 概要
- `ucp_twitter_bot/ucp_tweet.py`
    - アンサイクロペディアの記事をランダムに選びツイートする
- `ucp_twitter_bot/ucp_follower.py`
    - 自動フォローする為のプログラム
- `ucp_twitter_bot/twitter_authentication.py`
    - twitterの認証を行う。
- `ucp_twitter_bot/ucp_favorite_tweet.py`
    - アンサイクロペディアに言及すると「いいね」をする機能。
- ucp_reply.py
    - Webhook(未実装)
- ucp_streaming_reply.py
    - 自動応答botのソースコード。とりあえず動く（はず）だが実用には耐えない状態（WIP）
- ucp_get_usercontribs.py
    - アンサイクロペディアの投稿者を調べるスクリプト。WIP。
- ucp_test.py
    - テストコード(未実装)

## やりたいこと
- [ ] 「おすすめは」と聞かれて「秀逸な記事」をランダムに返信する
- [ ] 「新着記事は」と聞かれて「新着記事」をランダムに選び返信する
- [ ] Twitterのトレンドを調べて、それに合わせて記事をツイートする
- [ ] 日替わりで特定のジャンルを紹介する
- [ ] 日替わりで特定の利用者の記事を紹介する
- [x] あらかじめ、どうしようもない記事とか日記を間引く
- [ ] 特定の日になると特定の話題をツイートする（例：バレンタイン、クリスマス、ハロウィン）
- [ ] UCPのスクショをとって投稿する


## ChangeLog
### 2022 Oct 6 (v0.0.4)
- アンサイクロペディアに言及した場合は「いいね」を付与する

### 2022 Oct 5 (v0.0.3)
- `Google Cloud Function`へスクリプトを移設
- `tox`や`pyproject`環境の設定

### 2021 Feb 11
以下の変更
- 特定のカテゴリに属する記事をツイートしないようにした。具体的には以下のカテゴリの記事
    - 'カテゴリ:どうしようもない記事'
    - 'カテゴリ:修正が必要な記事'
    - 'カテゴリ:拡張が必要な記事'
    - 'カテゴリ:要添削'
    - 'カテゴリ:ユーモアの足りない記事'
    - 'カテゴリ:即時削除'
    - 'カテゴリ:削除議論中のページ'
    - 'カテゴリ:日記/過去ログ'
    - 'カテゴリ:曖昧さ回避'

### 2020 May 30
初回リリース
- 実装機能
    - UCPのランダムな記事を選びTwitterに投稿する（ucp_tweet.py）
    - フォロワー返し(ucp_follower.py)
