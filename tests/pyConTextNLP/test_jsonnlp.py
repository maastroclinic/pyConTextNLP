import logging
import unittest
from pyConTextNLP.tests.tcp_client import ContextClient
import json
import pyConTextNLP.io.jsonnlp as jsonnlp
import pyConTextNLP.io.server as server



logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class JsonNlpTest(unittest.TestCase):
    """

    """

    # def setUp(self):
    #     self.context_client = ContextClient('localhost', 9999)
    #     self.context_client.connect()
    #
    # def tearDown(self):
    #     self.context_client.close()

    # def test_target_regex_simple(self):
    #     targets = [{'direction': '', 'lex': 'tum', 'regex': 'tum', 'type': 'TUMOR'}]
    #     sentence = 'Er is een tumor gevonden'
    #     rslts = self.context_client.annotate(sentence, targets)
    #     logging.info('result{}'.format(rslts))
    #     assert len(rslts) > 0

    with open('../resources/radiology-report-response.json') as json_file:
        data = json.load(json_file)
        # print(json.dumps(data, indent=4))
        # jsonnlp.iterate(data)
        server.process_jsonnlp(data)
        print(json.dumps(data, indent=4))



if __name__ == '__main__':
    unittest.main()