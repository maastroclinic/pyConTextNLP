import pyConTextNLP.io.conceptio as conceptio


def get_sentences(document):
    return document['sentences'].items()


def get_sentence_string(document, sentence):
    sentence_string = ''
    for token_id in sentence['tokens']:
        sentence_string += document['tokenList'][token_id - 1]['text']
        if document['tokenList'][token_id - 1]['misc']['SpaceAfter']:
            sentence_string += ' '
    return sentence_string


def add_sentence_results(document, sentence, results):
    context_list = []
    start_id = len(document['context']) + 1

    for result in results:
        context_list.append(get_result(result, False, document, sentence))
    for list_item in context_list:
        for item in list_item:
            item.update({'id': start_id})
            document['context'].append(item)
            document = update_tokens(document, item)
            start_id += 1
    return document


def get_sentence_entity_phrases(document, sentence, entity_types):
    phrases = []
    entity_phrase = None
    for token_id in sentence['tokens']:
        token = document['tokenList'][token_id - 1]
        if "B" is token['entity_iob'] and token['entity'] in entity_types:
            entity_phrase = {'direction': '', 'lex': token['text'], 'regex': '', 'type': token['entity']}
        if "I" is token['entity_iob'] and token['entity'] in entity_types:
            entity_phrase.update({'text': entity_phrase['lex'] + ' ' + token['text']})
        if "O" is token['entity_iob'] and entity_phrase:
            phrases.append(entity_phrase)
            entity_phrase = None

    if entity_phrase:
        phrases.append(entity_phrase)

    return phrases


def get_targets(document, sentence, entity_types):
    phrases = get_sentence_entity_phrases(document, sentence, entity_types)
    return conceptio.get_target_items(phrases)


def update_tokens(document, item):
    for i, token_id in enumerate(item['target']['tokens']):
        current_token = document['tokenList'][token_id - 1]
        current_token['entity_iob'] = 'B' if i == 0 else 'I'
        current_token['entity'] = 'ONTOLOGY'
        current_token['misc'].update({'uri': item['target']['category']})
        document['tokenList'][token_id - 1] = current_token
    return document


def get_result(rslt, rule_info, document, sentence):
    node_result_list = []
    for node in rslt.nodes:

        if node._tagObject__ConTextCategory != 'target':
            continue

        target = {}
        target['span_start'] = node._tagObject__spanStart
        target['span_end'] = node._tagObject__spanEnd
        target['span_end'] = node._tagObject__spanEnd
        target['category'] = node._tagObject__category

        tokens = get_phrase_tokens(document, sentence, node._tagObject__foundPhrase, node._tagObject__spanStart, node._tagObject__spanEnd)

        context_item = {}
        context_item['id'] = None
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
                    modifier['tokens'] = get_phrase_tokens(document, sentence, tag._tagObject__foundPhrase, tag._tagObject__spanStart, tag._tagObject__spanEnd)
                    if rule_info:
                        modifier['literal'] = tag._tagObject__item._contextItem__literal
                        modifier['re'] = tag._tagObject__item._contextItem__re
                        modifier['rule'] = tag._tagObject__item._contextItem__rule
                    context_modifiers.append(modifier)

        context_item['modifiers'] = context_modifiers
        node_result_list.append(context_item)
    return node_result_list


def get_phrase_tokens(document, sentence, phrase, phrase_start, phrase_end):
    tokens = []
    if len(sentence['tokens']) is 0:
        return tokens

    first_token_id = sentence['tokens'][0]
    first_token = document['tokenList'][first_token_id - 1]
    sentence_offset = first_token['characterOffsetBegin']
    for token_id in sentence['tokens']:  # always sorted?
        token = document['tokenList'][token_id - 1]
        token_start = token['characterOffsetBegin'] - sentence_offset
        token_end = token['characterOffsetEnd'] - sentence_offset

        if phrase_start >= token_start and phrase_start < token_end:
            tokens.append(token['id'])
        elif phrase_end > token_start and phrase_end <= token_end:
            tokens.append(token['id'])

        if token_end >= phrase_end:
            return tokens

    return tokens
