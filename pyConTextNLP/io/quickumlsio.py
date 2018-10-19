import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConText as pyConText
from operator import itemgetter, attrgetter



def get_items_quickumls(concept_list):
    """
    takes QuickUMLS response in json format
    """
    context_items = []

    for concept in concept_list:
        for concept_item in concept:
            tmp = [concept_item['ngram'], concept_item['cui'], '', '']
            item = itemData.contextItem(tmp)
            context_items.append(item)
    return context_items

def getContextConcepts(rslts, concept_list, rule_info):

    concepts_flatlist = getFlatListConcepts(concept_list)
    print('concepts to match:', len(concepts_flatlist))

    if not concept_list:
        return []

    concept_index = 0
    concept = concepts_flatlist[concept_index]
    cui = concept.get('cui').upper().lower()
    start = concept.get('start')

    for rslt in rslts:

        if not rslt:
            continue

        nodelist = []
        for node in rslt.nodes:
            nodelist.append(node)

        sorted_nodes = sorted(nodelist, key=attrgetter('_tagObject__spanStart'))

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
