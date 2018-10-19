FROM jfloff/alpine-python:recent
MAINTAINER Sander Puts

WORKDIR /opt
ADD . / pyContextNLP/

WORKDIR /opt/pyContextNLP
RUN pip install -r  requirements.txt
RUN python -m textblob.download_corpora

ENV PYTHONPATH /opt/pyContextNLP:$PYTHONPATH

WORKDIR /opt/pyContextNLP
CMD python /opt/pyContextNLP/pyConTextNLP/io/tcpService.py --port=9999