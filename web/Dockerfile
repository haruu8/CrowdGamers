FROM python:3.8-slim

RUN mkdir /code
WORKDIR /code

# debconf: delaying package configuration, since apt-utils is not installed が表示されないように設定
ENV DEBCONF_NOWARNINGS yes

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

COPY ./entrypoint.sh /code/app/entrypoint.sh
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y libpq-dev build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc
RUN apt-get install -y netcat
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN apt-get autoremove -y gcc

COPY . /code/

ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]