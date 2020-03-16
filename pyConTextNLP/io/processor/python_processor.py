#!/usr/bin/env python
import json
import logging
import os
import os
import warnings
import re
import pathlib
import argparse
import logging

from kafka import KafkaConsumer, KafkaProducer

from util.http_status_server import HttpHealthServer
from util.task_args import get_kafka_binder_brokers, get_input_channel, get_output_channel

from pyConTextNLP.io import jsonnlp

import pyConTextNLP.io.conceptio as conceptio
import pyConTextNLP.io.jsonnlp as jsonnlp

import pyConTextNLP.itemData as itemData
import pyConTextNLP.utils as utils


logging.basicConfig()
logger = logging.getLogger('python-processor')
logger.setLevel(level=logging.INFO)

print("ENV", os.environ, flush=True)

consumer = KafkaConsumer(get_input_channel(), bootstrap_servers=[get_kafka_binder_brokers()])
producer = KafkaProducer(bootstrap_servers=[get_kafka_binder_brokers()])
HttpHealthServer.run_thread()


# print("sleep", flush=True)
# sleep(60)
# print("awake", flush=True)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
parser = argparse.ArgumentParser(description='Annotate your document with contextual information')
parser.add_argument('--modifiers',
                    dest='modifiers',
                    help='path or url of the modifiers (default https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml)',
                    default='https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml')

parser.add_argument('--targets',
                    dest='targets',
                    help='path or url of targets (default https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml)',
                    default='https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml')

args, unknown = parser.parse_known_args()

if os.environ.get('MODIFIERS'):
    args.modifiers = '' + os.environ.get('MODIFIERS')
    print('MODIFIERS as env = ' + args.modifiers)
if os.environ.get('TARGETS'):
    args.targets = '' + os.environ.get('TARGETS')
    print('TARGETS as env = ' + args.targets)

if os.environ.get('ENTITY_TYPES'):
    entity_types = os.environ.get('ENTITY_TYPES').split(',')
else:
    entity_types = ['PRODUCT', 'ONTOLOGY']
print('ENTITY_TYPES = ', entity_types)


def is_url(url):
    regex = re.compile(r'^(?:http|ftp)s?://', re.IGNORECASE)
    return re.match(regex, url)

if not is_url(args.modifiers):
    args.modifiers = pathlib.Path(os.path.abspath(args.modifiers)).as_uri()
if not is_url(args.targets):
    args.targets = pathlib.Path(os.path.abspath(args.targets)).as_uri()

logging.info('loading targets=${0}'.format(args.targets))
targets = itemData.get_items(args.targets)
logging.info('loading modifiers=${0}'.format(args.modifiers))
modifiers = itemData.get_items(args.modifiers)

warnings.filterwarnings("ignore")


def process_json_nlp(document):
    context_result = []
    for sentence in jsonnlp.get_sentences(document):
        sentence_string = jsonnlp.get_sentence_string(document, sentence[1])
        targets_document = targets + jsonnlp.get_targets(document, sentence[1], entity_types)
        results = utils.perform_py_context_nlp(modifiers, targets_document, sentence_string)
        jsonnlp.add_sentence_results_context(document, sentence[1], results, context_result)
    return document, context_result


def is_json(unknown):
    try:
        json.loads(unknown)
    except ValueError:
        return False
    logger.info('json')
    return True


while True:
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        jsonnlp_document = data["json-nlp"]['documents'][0]
        try:
            jsonnlp_document, context_result = process_json_nlp(jsonnlp_document)
            logger.info("results %s", str(context_result))
            data['context'] = context_result
            data["json-nlp"]['documents'][0] = jsonnlp_document
        except Exception as e:
            logger.error('error', e)

        result_json = json.dumps(data)
        producer.send(get_output_channel(), result_json.encode('utf-8'))



