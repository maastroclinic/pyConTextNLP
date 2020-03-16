# (from repository root) $ docker build . -f docker/processor/Dockerfile -t putssander/pycontextnlp-processor:latest
FROM springcloud/openjdk:latest

# Install the required packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    libssl-dev \
    git \
    curl && \
    apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin

# run SCDF with Kafka
RUN pip3 install kafka-python

# edited version of Py-JSON-NLP
RUN pip3 install git+https://github.com/putssander/Py-JSON-NLP.git

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN python3 -m textblob.download_corpora

COPY . / /app/
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENTRYPOINT ["python3", "/app/pyConTextNLP/io/processor/python_processor.py", "$@", "--"]
