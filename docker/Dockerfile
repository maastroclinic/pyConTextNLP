FROM jfloff/alpine-python:recent
MAINTAINER Sander Puts

WORKDIR /opt
ADD . / pyContextNLP/

WORKDIR /opt/pyContextNLP
RUN pip install -r  requirements.txt
RUN python -m textblob.download_corpora

ENV PYTHONPATH /opt/pyContextNLP:$PYTHONPATH
ARG PORT=9999
ENV PORT=$PORT

WORKDIR /opt/pyContextNLP
CMD python /opt/pyContextNLP/pyConTextNLP/io/tcpService.py --port=$PORT