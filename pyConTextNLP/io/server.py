#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

"""

"""
import os
import warnings
import re
import pathlib
import json
import argparse
import logging
from flask import Flask
from flask import request


import pyConTextNLP.io.conceptio as conceptio
import pyConTextNLP.io.jsonnlp as jsonnlp

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

warnings.filterwarnings("ignore")


def process(data):
    dto = json.loads(str(data))
    if not dto['meta']['DC.date']:
        context_concepts = process_default(dto)
        return json.dumps(context_concepts)
    else:
        data = process_jsonnlp(dto)
        return json.dumps(data)


def process_default(dto):
    targets_document = get_target_documents_default(dto)
    text = dto['text']
    results = utils.perform_py_context_nlp(modifiers, targets_document, text)
    context_concepts = conceptio.get_results(results, rule_info=False)
    logging.info('pyContextNLP annotated target size:{}'.format(len(context_concepts)))
    return context_concepts


def get_target_documents_default(dto):
    concepts_context_items = None
    try:
        concepts = dto['targets']
        concepts_context_items = conceptio.get_target_items(concepts)
        logging.info('additional target input size:{0}'.format(len(concepts_context_items)))
    except:
        logging.info("no additional input target set")

    if concepts_context_items:
        targets_document = targets + concepts_context_items
    else:
        targets_document = targets

    return targets_document


def process_jsonnlp(data):
    data['documents'][0]['context'] = []
    for sentence in jsonnlp.get_sentences(data):
        text = jsonnlp.get_sentence_string(data, sentence[1])
        logging.info(text)
        targets_document = targets #to implement based on entities? maybe it should be targets_sentence
        results = utils.perform_py_context_nlp(modifiers, targets_document, text)
        jsonnlp.add_sentence_results(data, sentence[1], results)
    return data


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def process_flask():
    content = request.get_json(silent=True)
    return process(json.dumps(content))


@app.route('/json-nlp', methods=['GET', 'POST'])
def process_flask_jsonnlp():
    content = request.get_json(silent=True)
    return process(json.dumps(content))


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
