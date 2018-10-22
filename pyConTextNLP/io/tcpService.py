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

import pyConTextNLP.io.quickumlsio as quickumlsio
import pyConTextNLP.itemData as itemData
import pyConTextNLP.utils as utils

parser = argparse.ArgumentParser(description='Annotate your document with contextual information')
parser.add_argument('--modifiers', dest='modifiers', type=str, help='path or url of the modifiers (default https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml)', default='https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml')
parser.add_argument('--targets', dest='targets', type=str, help='path or url of targets (default https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml)', default='https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml')
parser.add_argument('--port', dest='port', type=int, help='port for service (default: 9999)', default=9999)

args = parser.parse_args()


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

targets = itemData.get_items(args.modifiers)
modifiers = itemData.get_items(args.targets)

if (os.environ.get('GRPC','false')=='true'):
    from springcloudstream.grpc.stream import Processor
else:
    from springcloudstream.tcp.stream import Processor

warnings.filterwarnings("ignore")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def process(data):
    targets_document = targets

    dto = json.loads(str(data))
    text = dto['text']
    quickumls_concepts = dto['quickumls_concepts']

    targets_document = targets_document + quickumlsio.get_items_quickumls(quickumls_concepts)

    rslts = utils.perform_py_context_nlp(modifiers, targets_document, text)
    context_concepts = quickumlsio.getContextConcepts(rslts, quickumls_concepts, rule_info=False)
    return json.dumps(context_concepts, cls=SetEncoder)


Processor(process, sys.argv).start()