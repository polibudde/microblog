FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV STATIC_URL /app/static

COPY ./app /app
WORKDIR /app

RUN pip install -r requirements.txt




