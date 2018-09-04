import json
import os
import pathlib
import unittest

import nltk
from IPython.display import HTML
from textblob import TextBlob

import pyConTextNLP.display.html as html
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText

nltk.download('punkt')

path_report = '..\\resources\\report.txt'
path_targets_quickumls = '..\\resources\\report_quickumls_out.json'
path_modifiers_kb = '..\\..\\KB\\lexical_kb_05042016_nl.tsv'
path_result_pycontextnlp_xml = '..\\resources\\report_pycontextnlp_out.xml'
path_result_pycontextnlp_html = '..\\resources\\report_pycontextnlp_out.html'

class TestQuickUMLSIntegration(unittest.TestCase):

    report = {}
    modifiers = {}
    targets = {}

    def test_quickumls_to_xml(self):
        self.load_data_files()
        context = perform_py_context_nlp(self.report, self.modifiers, self.targets)
        write_result_xml(context, path_result_pycontextnlp_xml)
        # write_result_html(context, path_result_pycontextnlp_html)

    def load_data_files(self):
        absolute_path_string_abspath = os.path.abspath(path_modifiers_kb)
        self.modifiers = itemData.instantiateFromCSVtoitemData(pathlib.Path(absolute_path_string_abspath).as_uri())

        with open(path_targets_quickumls) as json_file:
            data_result = json.load(json_file)
        self.targets = itemData.instantiateFromQuickUMLSResponseToitemData(data_result['response'])

        with open(path_report, 'r') as reportfile:
            self.report = reportfile.read()


def perform_py_context_nlp(report, modifiers, targets):
    context = pyConText.ConTextDocument()
    blob = TextBlob(report.lower())
    rslts = []
    for s in blob.sentences:
        m = markup_sentence(s.raw, modifiers=modifiers, targets=targets)
        rslts.append(m)

    for r in rslts:
        context.addMarkup(r)

    return context


def markup_sentence(s, modifiers, targets, prune_inactive=True):
    """
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup


def write_result_html(context, path):
    def get_colors():
        return {
            "bowel_obstruction": "blue",
            "inflammation": "blue",
            "definite_negated_existence": "red",
            "probable_negated_existence": "indianred",
            "ambivalent_existence": "orange",
            "probable_existence": "forestgreen",
            "definite_existence": "green",
            "historical": "goldenrod",
            "indication": "pink",
            "acute": "golden"
        }

    # hmtl bug? AttributeError: 'NodeView' object has no attribute 'sort'
    data = HTML(html.mark_document_with_html(context, colors=get_colors(), default_color="black"))
    print('writing pycontextnlp html result to file:', path)
    with open(path, 'w') as outfile:
        outfile.write(data)


def write_result_xml(context, path):
    print('writing pycontextnlp xml result to file:', path)
    with open(path, 'w') as outfile:
        outfile.write(context.getXML())


if __name__ == '__main__':
    unittest.main()