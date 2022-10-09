from datetime import datetime

import requests

from ucptwitbot import constant


def article_created_time(title: str) -> datetime:
    """
    記事が作成された日時を調べる

    Args:
        title (str): 記事のタイトル
    Return:
        datetime: 記事の作成日時 (UTC)
    """
    session = requests.Session()
    PARAM = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvlimit": 100,
        "titles": title,
        "rvprop": "timestamp",
    }

    continue_flag = True
    revisions_history = []

    while continue_flag:
        result = session.get(url=constant.UCP_API, params=PARAM)
        tmp_data = result.json()
        num_pages = list(tmp_data["query"]["pages"].keys())[0]
        tmp_revisions = tmp_data["query"]["pages"][num_pages]["revisions"]
        revisions_history.extend(tmp_revisions)
        # continueがなければ終了する
        if "continue" not in tmp_data:
            continue_flag = False
        # continueがあれば次のリストを取得する
        else:
            PARAM["rvcontinue"] = tmp_data["continue"]["rvcontinue"]

    posted_datetime_str = revisions_history[-1]["timestamp"]
    posted_datetime = datetime.strptime(posted_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    return posted_datetime
