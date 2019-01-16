import pyConTextNLP.itemData as itemData


def get_target_items(target_list):
    """
    takes concepts response in json format
    """
    target_items = []
    if not target_list:
        return target_items

    target_items = [itemData.contextItem((d["lex"],
                                       d["type"],
                                       r"%s"%d["regex"],
                                       d["direction"])) for d in target_list]
    return target_items


def get_results(rslts, rule_info):
    concept_list_context = []
    for rslt in rslts:
        concept_list_context += add_non_concepts(rslt, rule_info)
    return concept_list_context


def add_non_concepts(rslt, rule_info):
    concept_list_context = []
    for node in rslt.nodes:

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
                    concept['modifier_found_phrase'] = tag._tagObject__foundPhrase
                    if rule_info:
                        concept['modifier_context_literal'] = tag._tagObject__item._contextItem__literal
                        concept['modifier_context_re'] = tag._tagObject__item._contextItem__re
                        concept['modifier_context_rule'] = tag._tagObject__item._contextItem__rule
        concept_list_context.append(concept)

    return concept_list_context

