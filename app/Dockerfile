FROM python:3.8-slim

RUN mkdir /code
WORKDIR /code

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/app/requirements.txt
COPY ./entrypoint.sh /code/app/entrypoint.sh
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y libpq-dev build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc
RUN apt install -y netcat
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    pip install psycopg2
RUN apt-get autoremove -y gcc

COPY . /code/

ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]