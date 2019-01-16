#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

"""

"""
import os
import sys
import warnings
import re
import pathlib
import json
import argparse
import logging


import pyConTextNLP.io.conceptio as conceptio
import pyConTextNLP.itemData as itemData
import pyConTextNLP.utils as utils

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


def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


if not is_url(args.modifiers):
    args.modifiers = pathlib.Path(os.path.abspath(args.modifiers)).as_uri()
if not is_url(args.targets):
    args.targets = pathlib.Path(os.path.abspath(args.targets)).as_uri()

logging.info('loading targets=${0}'.format(args.targets))
targets = itemData.get_items(args.targets)
logging.info('loading modifiers=${0}'.format(args.modifiers))
modifiers = itemData.get_items(args.modifiers)

if (os.environ.get('GRPC','false')=='true'):
    from springcloudstream.grpc.stream import Processor
else:
    from springcloudstream.tcp.stream import Processor

warnings.filterwarnings("ignore")


def process(data):
    dto = json.loads(str(data))
    text = dto['text']

    concepts_context_items = None
    try:
        concepts = dto['targets']
        concepts_context_items = conceptio.get_target_items(concepts)
        logging.info('additional target input size:{0}'.format(len(concepts_context_items)))
    except:
        logging.info("no additional input target set")
        concepts = None

    if concepts_context_items:
        targets_document = targets + concepts_context_items
    else:
        targets_document = targets

    rslts = utils.perform_py_context_nlp(modifiers, targets_document, text)
    context_concepts = conceptio.get_results(rslts, rule_info=False)
    logging.info('pyContextNLP annotated target size:{}'.format(len(context_concepts)))

    return json.dumps(context_concepts) + '\r\n'


def get_processor_args(args):
    processor_args = []
    for current_arg in args:
        if "modifiers" not in current_arg and "targets" not in current_arg:
            processor_args.append(current_arg)
    return processor_args


Processor(process, get_processor_args(sys.argv)).start()