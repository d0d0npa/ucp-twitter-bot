import os

import requests


# Your Access Keys
page_id_1 = os.getenv("FB_PAGE_ID")
facebook_access_token_1 = os.getenv("FB_PAGE_ACCESS_TOKEN")
msg = "Test Post"
post_url = f"https://graph.facebook.com/{page_id_1}/feed"
payload = {"message": msg, "access_token": facebook_access_token_1}
r = requests.post(post_url, data=payload)
print(r.text)
