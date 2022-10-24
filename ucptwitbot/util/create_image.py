import os
import shutil
import urllib

import replicate
import requests


MODEL_REPOS = "rinnakk/japanese-stable-diffusion"


def generate_image_from_model(prompt: str) -> str:
    model = replicate.models.get(MODEL_REPOS)
    image = model.predict(prompt=prompt, num_inference_steps=50, guidance_scale=7.5)

    return image[0]


def get_image(image_url: str, tmp_dir: str) -> str:
    parsed_url = urllib.parse.urlparse(image_url)
    filename = os.path.basename(parsed_url.path)

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True,
        # otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        print("created temporary directory", tmp_dir)
        tmp_path = os.path.join(tmp_dir, filename)
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print("Image sucessfully Downloaded: ", filename)
        return tmp_path
    else:
        print("Image Couldn't be retreived")
        # 下のraiseするエラーは適当に決めたので要検討
        raise RuntimeError


# generate_image_from_modelはURLだけ返すか
# /tmpに保存しておいて、後でアップロードする際に使用する（cloud functionでどうせイメージは廃棄されるので）
# ツイッターへのアップロードは後で行う。ダウンロード
