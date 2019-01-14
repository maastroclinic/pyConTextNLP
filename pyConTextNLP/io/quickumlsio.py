import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConText as pyConText
from operator import itemgetter, attrgetter
import re

re_cui = re.compile('C\d{7}', re.IGNORECASE)


def get_items_quickumls(concept_list):
    """
    takes QuickUMLS response in json format
    """
    context_items = []
    if not concept_list:
        return context_items

    for concept in concept_list:
        for concept_item in concept:
            tmp = [concept_item['ngram'], concept_item['cui'], '', '']
            item = itemData.contextItem(tmp)
            context_items.append(item)
    return context_items


def getContextConcepts(rslts, concept_list, rule_info):

    concept_list_context = []
    for rslt in rslts:
        if not rslt:
            continue

        nodelist_concepts = []
        nodelist_regex = []

        for node in rslt.nodes:
            node_category = node._tagObject__category[0].upper().lower()
            if re_cui.match(node_category):
                nodelist_concepts.append(node)
            else:
                nodelist_regex.append(node)

        if concept_list:
            concept_list_context += match_concepts(rslt, concept_list, nodelist_concepts, rule_info)

        concept_list_context += add_non_concepts(rslt, nodelist_regex, rule_info)

    return concept_list_context


def add_non_concepts(rslt, nodelist_regex, rule_info):
    concept_list_context = []
    for node in nodelist_regex:

        if node._tagObject__ConTextCategory != 'target':
            continue

        concept = {}
        concept['found_phrase'] = node._tagObject__foundPhrase
        concept['span_start'] = node._tagObject__spanStart
        concept['span_end'] = node._tagObject__spanEnd
        concept['span_end'] = node._tagObject__spanEnd
        concept['category'] = node._tagObject__category

        for edge in rslt.edges():
            for tag in edge:
                if tag._tagObject__ConTextCategory == 'modifier':
                    concept['modifier_category'] = tag._tagObject__category
                    concept['modifier_foundPhrase'] = tag._tagObject__foundPhrase
                    if rule_info:
                        concept['modifier_context_literal'] = tag._tagObject__item._contextItem__literal
                        concept['modifier_context_re'] = tag._tagObject__item._contextItem__re
                        concept['modifier_context_rule'] = tag._tagObject__item._contextItem__rule
        concept_list_context.append(concept)

    return concept_list_context

def match_concepts(rslt, concept_list, nodelist_concepts, rule_info):

    concepts_flatlist = getFlatListConcepts(concept_list)
    print('concepts to match:', len(concepts_flatlist))

    concept_index = 0
    concept = concepts_flatlist[concept_index]
    cui = concept.get('cui').upper().lower()
    start = concept.get('start')

    sorted_nodes = sorted(nodelist_concepts, key=attrgetter('_tagObject__spanStart'))
    for node in sorted_nodes:

        node_cui = node._tagObject__category[0].upper().lower()

        if cui == node_cui:
            tmp_start = start

            while start == tmp_start:
                print('match ', concept_index, cui, concept.get('ngram'), node)

                for edge in rslt.edges():
                    for tag in edge:
                        if tag._tagObject__ConTextCategory == 'modifier':
                            concept['modifier_category'] = tag._tagObject__category
                            concept['modifier_foundPhrase'] = tag._tagObject__foundPhrase
                            if rule_info:
                                concept['modifier_context_literal'] = tag._tagObject__item._contextItem__literal
                                concept['modifier_context_re'] = tag._tagObject__item._contextItem__re
                                concept['modifier_context_rule'] = tag._tagObject__item._contextItem__rule

                concept_index = concept_index + 1
                if concept_index == len(concepts_flatlist):
                    break

                concept = concepts_flatlist[concept_index]
                cui = concept.get('cui').upper().lower()
                start = concept.get('start')

    return concepts_flatlist


def getFlatListConcepts(concept_list):
    flat = []
    for concept in concept_list:
        for concept_item in concept:
            flat.append(concept_item)

    flat_sorted = sorted(flat, key=itemgetter('start'))
    return flat_sorted
