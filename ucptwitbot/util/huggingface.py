import os
import time
from typing import Union

import requests


# WIP: バッチ処理の対応ができていない。
def summarize_article(input: str) -> Union[str, None]:
    SLEEP_TIME = 30
    API_URL = (
        "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
    )
    TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    RETRY_COUNT = 3

    headers = {"Authorization": f"Bearer {TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    is_able_to_get_suumary = False
    for _ in range(RETRY_COUNT):
        output = query(
            {
                "inputs": input,
            }
        )
        if isinstance(output, list):
            is_able_to_get_suumary = True
            break
        else:
            print("Got Error Result :", output)
            time.sleep(SLEEP_TIME)

    if is_able_to_get_suumary:
        return output[0]["summary_text"]
    else:
        return None
