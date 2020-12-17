FROM tiangolo/uwsgi-nginx-flask:python3.7
MAINTAINER Sander Puts

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . / /app/
RUN python -m download_corpora

ENV OPTIONAL_ARGS=''
ENV PYTHONPATH "${PYTHONPATH}:/app"

ENV LISTEN_PORT 5003
