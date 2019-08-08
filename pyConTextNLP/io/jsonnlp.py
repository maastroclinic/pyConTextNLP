import json

def get_sentences(data):
    return data['documents'][0]['sentences'].items()


def get_sentence_string(data, sentence):
    sentence_string = ''
    for token in sentence['tokens']:
        sentence_string += data['documents'][0]['tokenList'][token - 1]['text']
        if data['documents'][0]['tokenList'][token - 1]['misc']['SpaceAfter']:
            sentence_string += ' '
    return sentence_string


# this does work, offset issues by new lines and other unknowns, spacy can sentence split on new line but currently
# not configurable in microservice api
# def get_sentence_string_offset(data, sentence):
#     token_begin = sentence['tokens'][0]
#     token_end = sentence['tokens'][-1]
#
#     offset_begin = data['documents'][0]['tokenList'][token_begin - 1]['characterOffsetBegin']
#     offset_end = data['documents'][0]['tokenList'][token_end - 1]['characterOffsetEnd']
#     text = data['documents'][0]['text']
#     text = text.replace('\n', '')
#     text = text[offset_begin:offset_end]
#     return text


def add_sentence_results(data, sentence, results):
    context_list = []
    start_id = len(data['documents'][0]['context']) + 1

    for result in results:
        context_list.append(get_result(result, False, data, sentence))
    for list_item in context_list:
        for item in list_item:
            item.update({'id': start_id})
            data['documents'][0]['context'].append(item)
            start_id =+ 1
    return data


def get_result(rslt, rule_info, data, sentence):
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

        tokens = get_target_tokens(data, sentence, target)
        print(tokens)

        context = {}
        context['target'] = {}
        context['target']['foundPhrase'] = node._tagObject__foundPhrase
        context['target']['tokens'] = tokens
        context['target']['category'] = node._tagObject__category
        context['modifiers'] = []
        context_modifiers = []

        for edge in rslt.edges():


            for tag in edge:
                if tag._tagObject__ConTextCategory == 'modifier':

                    modifier = {}
                    modifier['category'] = tag._tagObject__category
                    modifier['found_phrase'] = tag._tagObject__foundPhrase
                    modifier['tokens'] = []

                    if rule_info:
                        modifier['modifier_context_literal'] = tag._tagObject__item._contextItem__literal
                        modifier['modifier_context_re'] = tag._tagObject__item._contextItem__re
                        modifier['modifier_context_rule'] = tag._tagObject__item._contextItem__rule
                    context_modifiers.append(modifier)

        context['modifiers'] = context_modifiers
        target_result_list.append(context)
    return target_result_list


def get_target_tokens(data, sentence, target):
    tokens = []
    for token_id in sentence['tokens']:
        token = data['documents'][0]['tokenList'][token_id - 1]
        if token['text'] == target['found_phrase']:
            tokens.append(token['id'])
    return tokens
