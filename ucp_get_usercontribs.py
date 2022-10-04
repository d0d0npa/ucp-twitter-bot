import re

import requests


session = requests.Session()

URL = "https://ansaikuropedia.org/api.php"
# 利用者の投稿履歴を調べる
user = "かぼ"
PARAM = {
    "action": "query",
    "format": "json",
    "list": "usercontribs",
    "ucuser": user,
    "uclimit": 500,
}

continue_flag = True
usercontribs = []
while continue_flag:
    result = session.get(url=URL, params=PARAM)
    DATA = result.json()
    tmp_usercontribs = DATA["query"]["usercontribs"]
    usercontribs.extend(tmp_usercontribs)
    # continueがなければ終了する
    if "continue" not in DATA:
        continue_flag = False
    # continueがあれば次のリストを取得する
    else:
        PARAM["uccontinue"] = DATA["continue"]["uccontinue"]


new_pages = []
for uc in usercontribs:
    # 新規投稿、かつ100バイト以上
    if "new" in uc.keys() and uc["size"] > 100:
        new_pages.append(uc["title"])
        print(uc["title"])

# 以下の記事空間に属する記事は取り除く
PATTERN_LIST = [
    "ファイル:.*",
    "ファイル・トーク:.*",
    "利用者:.*",
    "利用者・トーク:.*",
    "MediaWiki:.*",
    "Game talk:.*",
    "トーク:.*",
    "テンプレート:.*",
    "テンプレート・トーク:.*",
    "カテゴリ:.*",
    "UnBooks talk:.*",
    "日記/過去ログ/.*",
    "Forum:.*",
    "Forum talk:.*",
    "Uncyclopedia:.*",
    "Uncyclopedia・トーク:.*",
    "Portal:.*",
    "Portal talk:.*",
    "ヘルプ:.*",
    "ヘルプ・トーク:.*",
    "UnNews:バ科ニュース.*",
    "UnNews:訃報.*",
]
result_new_pages = []
for i_page in new_pages:
    i_match_pattern_flag = False
    for i_pattern in PATTERN_LIST:
        repatter = re.compile(i_pattern)
        result = repatter.match(i_page)
        if result:
            i_match_pattern_flag = True
    if not i_match_pattern_flag:
        result_new_pages.append(i_page)

# ユーザーの新規投稿記事一覧
print(result_new_pages)
