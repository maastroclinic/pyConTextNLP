import json
import socket
from json import JSONDecodeError
import logging


class ContextClient(object):

    def __init__(self, host, port):
        self.BUFFER_SIZE = 2048
        self.TCP_IP =  host
        self.TCP_PORT = port
        self.connect()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            print('connected to pycontextnlp')
        except ConnectionRefusedError:
            print('connection refused, is pyContextNLP running on '
                  'host={0}'.format(self.TCP_IP)
                  + ' port={0}'.format(self.TCP_PORT)+'?')

    def annotate(self, text, targets):

        if not text:
            return None

        data = {}
        data['text'] = text
        data['targets'] = targets
        json_data = json.dumps(data)
        json_data_crlf = json_data+'\r\n'
        logging.debug('send data=()'.format(json_data_crlf))
        encoded = json_data_crlf.encode('utf-8')
        self.s.sendall(encoded)
        data_response = self.recvall()
        data_response_obj = {}
        try:
            data_response_obj['response'] = json.loads(data_response)
            logging.debug('received data=()'.format(data_response_obj['response']))
            return data_response_obj['response']
        except JSONDecodeError as err:
            print("JSONDecodeError", err, json_data)
            self.close()
            self.connect()
            return None

    def recvall(self):
        data = ''
        while True:
            ch = self.s.recv(2048)
            data += ch.decode('UTF-8')
            if data.endswith('\r\n') or not ch:
                data = data.replace('\r\n', '')
                return data

    def close(self):
        self.s.close()

    @staticmethod
    def create_target(direction, lex, regex, category):
        return [{'direction': direction, 'lex': lex, 'regex': regex, 'type': category}]
