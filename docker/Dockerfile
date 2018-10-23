FROM jfloff/alpine-python:recent
MAINTAINER Sander Puts

WORKDIR /opt
ADD . / pyContextNLP/

WORKDIR /opt/pyContextNLP
RUN pip install -r  requirements.txt
RUN python -m textblob.download_corpora

ENV PYTHONPATH /opt/pyContextNLP:$PYTHONPATH
ENV PORT=9999
ENV OPTIONAL_ARGS=''

WORKDIR /opt/pyContextNLP
CMD python /opt/pyContextNLP/pyConTextNLP/io/tcpService.py --port=$PORT $OPTIONAL_ARGS
