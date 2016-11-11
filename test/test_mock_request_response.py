import unittest, json
from os.path import dirname, abspath
from test.helpers import path
from test.mocks import MockRequestResponse


root = dirname(abspath(__file__))


class TestMockRequestResponse(unittest.TestCase):
    def test_mock_request_response(self):
        components = [root, 'data', 'JSON-Schema-Test-Suite', 'draft4', 'refRemote']

        m = MockRequestResponse(components, 'http://localhost:1234/integer.json')
        data = json.loads(open(path((root, 'data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'integer.json'))).read())
        self.assertEquals(m.json(), data)

        data = json.loads(open(path((root, 'data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'subSchemas.json'))).read())
        self.assertEquals(m.json('http://localhost:1234/subSchemas.json#/integer'), data)

        data = json.loads(open(path((root, 'data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'folder', 'folderInteger.json'))).read())
        self.assertEquals(m.json('http://localhost:1234/folder/folderInteger.json'), data)


if __name__ == '__main__':
    unittest.main()
