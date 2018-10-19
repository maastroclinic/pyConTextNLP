""" """
import pyConTextNLP.pyConText as pyConText
from textblob import TextBlob


def get_document_markups(document):
    """ Given a ConTextDocument return an ordered list of the ConTextmarkup objects consistituting the document"""
    tmp = [(e[1],e[2]['sentenceNumber']) for e in document.getDocument().edges(data=True) if
           e[2].get('category') == 'markup']
    tmp.sort(key=lambda x:x[1])
    return [t[0] for t in tmp]

def get_section_markups(document, sectionLabel):
    """ Given a ConTextDocument and sectionLabel, return an ordered list of the ConTextmarkup objects in that section"""
    tmp = [(e[1],e[2]['sentenceNumber']) for e in document.getDocument().out_edges(sectionLabel, data=True) if
           e[2].get('category') == 'markup']
    tmp.sort(key=lambda x:x[1])
    return [t[0] for t in tmp]

def conceptInDocument(document, concept):
    """tests whether concept is in any nodes of document"""
    pass

def perform_py_context_nlp(modifiers, targets, document):
    """"""
    blob = TextBlob(document.lower())
    rslts = []
    for s in blob.sentences:
        m = markup_sentence(s.raw, modifiers=modifiers, targets=targets)
        rslts.append(m)

    return rslts

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

def markup_context(rslts):
    context = pyConText.ConTextDocument()
    for r in rslts:
        context.addMarkup(r)
    return context