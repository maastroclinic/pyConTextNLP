FROM tiangolo/uwsgi-nginx-flask:python3.7
MAINTAINER Sander Puts

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora

COPY . / /app/
WORKDIR /app

ENV OPTIONAL_ARGS=''
ENV PYTHONPATH "${PYTHONPATH}:/app"

ENV LISTEN_PORT 5003
