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
    node_result_list = []
    for node in rslt.nodes:

        if node._tagObject__ConTextCategory != 'target':
            continue

        target = {}
        target['span_start'] = node._tagObject__spanStart
        target['span_end'] = node._tagObject__spanEnd
        target['span_end'] = node._tagObject__spanEnd
        target['category'] = node._tagObject__category

        tokens = get_phrase_tokens(data, sentence, node._tagObject__foundPhrase)
        print(tokens)

        context_item = {}
        context_item['target'] = {}
        context_item['target']['foundPhrase'] = node._tagObject__foundPhrase
        context_item['target']['tokens'] = tokens
        context_item['target']['category'] = node._tagObject__category
        context_item['modifiers'] = []
        context_modifiers = []

        for edge in rslt.edges():
            for tag in edge:
                if tag._tagObject__ConTextCategory == 'modifier':
                    modifier = {}
                    modifier['category'] = tag._tagObject__category
                    modifier['found_phrase'] = tag._tagObject__foundPhrase
                    modifier['tokens'] = get_phrase_tokens(data, sentence, tag._tagObject__foundPhrase)
                    if rule_info:
                        modifier['literal'] = tag._tagObject__item._contextItem__literal
                        modifier['re'] = tag._tagObject__item._contextItem__re
                        modifier['rule'] = tag._tagObject__item._contextItem__rule
                    context_modifiers.append(modifier)

        context_item['modifiers'] = context_modifiers
        node_result_list.append(context_item)
    return node_result_list


def get_phrase_tokens(data, sentence, phrase):
    tokens = []
    for token_id in sentence['tokens']:
        token = data['documents'][0]['tokenList'][token_id - 1]
        if token['text'].lower() == phrase:
            tokens.append(token['id'])
    return tokens
