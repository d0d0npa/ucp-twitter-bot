FROM python:3


ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# ローカルのユーザーIDとDockerのユーザーIDを統一させる
RUN useradd -s /bin/bash --uid $USER_UID -m $USERNAME \
    && usermod -aG sudo $USERNAME

# 開発に必要なパッケージをインストールする
RUN apt-get update \
    && apt-get -y install \
    git \
    apt-transport-https \
    ca-certificates \
    gnupg

# Cloud SDKのインストール
# https://cloud.google.com/sdk/docs/install?hl=ja#deb
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
    && apt-get update -y \
    && apt-get install google-cloud-sdk -y

RUN pip install pipenv

#Python Packageのインストール
COPY requirements.txt /tmp
COPY requirements_dev.txt /tmp

RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements_dev.txt
