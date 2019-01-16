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
    results = []
    for rslt in rslts:
        results += add_result(rslt, rule_info)
    return results


def add_result(rslt, rule_info):
    target_result_list = []
    for node in rslt.nodes:

        if node._tagObject__ConTextCategory != 'target':
            continue

        target = {}
        target['found_phrase'] = node._tagObject__foundPhrase
        target['span_start'] = node._tagObject__spanStart
        target['span_end'] = node._tagObject__spanEnd
        target['span_end'] = node._tagObject__spanEnd
        target['category'] = node._tagObject__category

        for edge in rslt.edges():
            for tag in edge:
                if tag._tagObject__ConTextCategory == 'modifier':
                    target['modifier_category'] = tag._tagObject__category
                    target['modifier_found_phrase'] = tag._tagObject__foundPhrase
                    if rule_info:
                        target['modifier_context_literal'] = tag._tagObject__item._contextItem__literal
                        target['modifier_context_re'] = tag._tagObject__item._contextItem__re
                        target['modifier_context_rule'] = tag._tagObject__item._contextItem__rule
        target_result_list.append(target)

    return target_result_list

