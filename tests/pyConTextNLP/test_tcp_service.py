import logging
import unittest
from pyConTextNLP.tests.tcp_client import ContextClient

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class TcpServiceTest(unittest.TestCase):
    """
    Run tcpService pyConTextNLP/io/tcpService.py or
    docker run --rm -p 9999:9999 maastrodocker/pycontextnlp
    set port to 9999, host can be different from localhost (check log)
    """

    def setUp(self):
        self.context_client = ContextClient('localhost', 9999)
        self.context_client.connect()

    def tearDown(self):
        self.context_client.close()

    def test_target_regex_simple(self):
        targets = [{'direction': '', 'lex': 'tum', 'regex': 'tum', 'type': 'TUMOR'}]
        sentence = 'Er is een tumor gevonden'
        rslts = self.context_client.annotate(sentence, targets)
        logging.info('result{}'.format(rslts))
        assert len(rslts) > 0

    def test_target_regex_advanced(self):
        targets = [{'direction': '', 'lex': 'wd', 'regex': 'weke\s{0,1}delen|wda', 'type': 'TUMOR'}]
        sentence = 'Er zijn weke delen zichtbaar'
        rslts = self.context_client.annotate(sentence, targets)
        logging.info('result{}'.format(rslts))
        assert len(rslts) > 0

    def test_target_regex_advanced2(self):
        targets = [{'direction': '', 'lex': 'aaa', 'regex': 'weke\s{0,1}delen|wda', 'type': 'TUMOR'}]
        sentence = 'Er zijn wda zichtbaar'
        rslts = self.context_client.annotate(sentence, targets)
        logging.info('result{}'.format(rslts))
        assert len(rslts) > 0

    def test_default_target(self):
        sentence = 'There is no evidence of pulmonary embolism'
        rslts = self.context_client.annotate(sentence, [])
        logging.info('result{}'.format(rslts))
        assert len(rslts) > 0

    def test_default_target_2(self):
        sentence = 'pulmonary embolism is found'
        rslts = self.context_client.annotate(sentence, [])
        logging.info('result{}'.format(rslts))
        assert len(rslts) > 0


if __name__ == '__main__':
    unittest.main()
