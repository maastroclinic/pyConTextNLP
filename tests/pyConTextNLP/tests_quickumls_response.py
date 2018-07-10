import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx
import json
import pathlib
import os

absolute_path_string_abspath = os.path.abspath("..\..\KB\lexical_kb_04292013.tsv")
print(absolute_path_string_abspath)

modifiers = itemData.instantiateFromCSVtoitemData(pathlib.Path(absolute_path_string_abspath).as_uri())

data_result = ""
with open('data_result.txt') as json_file:
    data_result = json.load(json_file)


targets = itemData.instantiateFromQuickUMLSResponseToitemData(data_result['response'])

report = ""
with open('data.txt', 'r') as reportfile:
    report = reportfile.read()

markup = pyConText.ConTextMarkup()
isinstance(markup, nx.DiGraph)

markup.setRawText(report)
print(markup)
print(len(markup.getRawText()))

markup.cleanText()
print(markup)
print(len(markup.getText()))

markup.markItems(modifiers, mode="modifier")
print(markup.nodes(data=True))

markup.markItems(targets, mode="target")
print(markup.nodes(data=True))

markup.pruneMarks()
markup.dropMarks('Exclusion')
# apply modifiers to any targets within the modifiers scope
markup.applyModifiers()
markup.pruneSelfModifyingRelationships()

print(markup)
