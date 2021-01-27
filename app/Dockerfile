FROM python:3.8

RUN mkdir /code
WORKDIR /code

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1

# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/app/requirements.txt
COPY ./entrypoint.sh /code/app/entrypoint.sh
COPY requirements.txt /code/

RUN pip install psycopg2 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /code/

ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]