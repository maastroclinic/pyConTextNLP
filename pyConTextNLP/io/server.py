#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

"""

"""
import os
import warnings
import re
import pathlib
import argparse
import logging
from flask import Flask
from flask import request
from flask import jsonify


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

if os.environ.get('MODIFIERS'):
    args.modifiers = '' + os.environ.get('MODIFIERS')
    print('MODIFIERS as env = ' + args.modifiers)
if os.environ.get('TARGETS'):
    args.targets = '' + os.environ.get('TARGETS')
    print('TARGETS as env = ' + args.targets)


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


def process(dto):
    if 'meta' not in dto or 'DC.date' not in dto['meta']:
        context_concepts = process_default(dto)
        return context_concepts
    else:
        return process_jsonnlp(dto)


def process_default(dto):
    targets_document = get_target_documents_default(dto)
    if 'text' not in dto:
        raise ValueError("No key 'text' in given data")

    text = dto['text']
    results = utils.perform_py_context_nlp(modifiers, targets_document, text)
    context_concepts = conceptio.get_results(results, rule_info=False)
    logging.info('pyContextNLP annotated target size:{}'.format(len(context_concepts)))
    return context_concepts


def get_target_documents_default(dto):
    concepts_context_items = None
    if 'targets' in dto:
        concepts = dto['targets']
        concepts_context_items = conceptio.get_target_items(concepts)
        logging.info('additional target input size:{0}'.format(len(concepts_context_items)))
    else:
        logging.info("no additional input target set")

    if concepts_context_items:
        targets_document = targets + concepts_context_items
    else:
        targets_document = targets

    return targets_document


def process_jsonnlp(data):
    document = data['documents'][0]
    document['context'] = []
    for sentence in jsonnlp.get_sentences(document):
        sentence_string = jsonnlp.get_sentence_string(document, sentence[1])
        targets_document = targets + jsonnlp.get_targets(document, sentence[1])
        results = utils.perform_py_context_nlp(modifiers, targets_document, sentence_string)
        jsonnlp.add_sentence_results(document, sentence[1], results)
    data['documents'][0] = document
    return data


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def process_flask():
    if request.method == 'GET':
        content = {}
        if 'text' not in request.url:
            raise ValueError('You need to request param "text"')
        content['text'] = request.args.get('text')
    else:
        content = request.get_json(silent=True)
    return jsonify(process(content))


@app.route('/json-nlp', methods=['GET', 'POST'])
def process_flask_jsonnlp():
    content = request.get_json(silent=True)
    return jsonify(process_jsonnlp(content))


if __name__ == "__main__":
    app.run(debug=False, port=5003, host='0.0.0.0')
