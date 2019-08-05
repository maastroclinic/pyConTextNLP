FROM jfloff/alpine-python:latest
MAINTAINER Sander Puts

COPY requirements.txt /opt/pyContextNLP/requirements.txt
WORKDIR /opt/pyContextNLP
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora

COPY . / /opt/pyContextNLP/
WORKDIR /opt/pyContextNLP

ENV PYTHONPATH /opt/pyContextNLP:$PYTHONPATH
ENV PORT=9999
ENV OPTIONAL_ARGS=''

CMD python /opt/pyContextNLP/pyConTextNLP/io/tcpService.py --port=$PORT $OPTIONAL_ARGS
