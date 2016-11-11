from os.path import dirname, abspath
from test.mocks import MockRequestResponse
from test.base import JSONSchemaPlusTest
import unittest


try:
    import mock
except:
    from unittest import mock


root = dirname(abspath(__file__))
   

class TestValidatorsWithSuite(JSONSchemaPlusTest):
    def test_optionals(self):
        self.run_test((root, 'data', 'JSON-Schema-Test-Suite', 'draft4', 'optional', '*.json'))

    @mock.patch('jsonschemaplus.resolver.get')
    def test_draft4(self, mock_get):
        m = MockRequestResponse((root, 'data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote'))
        mock_get.side_effect = lambda url: m.json(url)
        self.run_test((root, 'data', 'JSON-Schema-Test-Suite', 'draft4', '*.json'))


if __name__ == '__main__':
    unittest.main()
