from copy import deepcopy
import glob, json, unittest, json as json_
from inspect import stack
from os.path import join, dirname, abspath
from jsonschemaplus.validators import Draft4Validator
from jsonschemaplus.schemas.metaschema import metaschema

try:
    import mock
except:
    from unittest import mock


try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


def path(args):
    return join(dirname(abspath(__file__)), *args)


def paths(components, excluded=None):
    paths = glob.glob(join(dirname(abspath(__file__)), *components))
    if excluded:
        for filename in excluded:
            for path in paths:
                if path.endswith(filename):
                    paths.remove(path)
                    break
    return paths


class MockRequestResult(object):
    def __init__(self, url):
        components = ['data', 'JSON-Schema-Test-Suite', 'draft4', 'refRemote']
        components.extend(urlparse(url).path.split('/'))
        self._data = json_.loads(open(path(components)).read())

    def json(self):
        return self._data


class JSONSchemaPlusTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.paths = paths(('data', 'JSON-Schema-Test-Suite', 'draft4', '*.json'))

    # def print_details(self, is_valid, test_data, schema):
    #     if is_valid != test_data['valid']:
    #         print('data: %s' % test_data['data'])
    #         print('schema: %s' % schema)
    #         print('is_valid: %s, valid: %s' % (is_valid, test_data['valid']))

    def run_test_data(self, path):
        for data in json.loads(open(path).read()):
            validator = Draft4Validator(data['schema'])
            calling_func_name = stack()[1][3]
            for test in data['tests']:
                is_valid = validator.is_valid(test['data'])
                self.assertEquals(is_valid, test['valid'], calling_func_name)

    def run_test(self, components):
        if components[-1].startswith('*.'):
            for p in paths(components):
                self.run_test_data(p)
        else:
            self.run_test_data(path(components))
    

class TestValidatorsWithSuite(JSONSchemaPlusTest):
    def test_resolve_metaschema(self):
        v = Draft4Validator({})
        schema = deepcopy(metaschema)
        # First assert values before resolving references
        self.assertEquals(schema['definitions']['schemaArray']['items'], {'$ref': '#'})
        self.assertEquals(schema['definitions']['positiveIntegerDefault0']['allOf'][0],
            {'$ref': '#/definitions/positiveInteger'})
        self.assertEquals(schema['properties']['maxLength'],
            {'$ref': '#/definitions/positiveInteger'})
        self.assertEquals(schema['properties']['minLength'],
            {'$ref': '#/definitions/positiveIntegerDefault0'})
        self.assertEquals(schema['properties']['additionalItems']['anyOf'][1],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['items']['anyOf'][0],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['items']['anyOf'][1],
            {'$ref': '#/definitions/schemaArray'})
        self.assertEquals(schema['properties']['maxItems'],
            {'$ref': '#/definitions/positiveInteger'})
        self.assertEquals(schema['properties']['minItems'],
            {'$ref': '#/definitions/positiveIntegerDefault0'})
        self.assertEquals(schema['properties']['maxProperties'],
            {'$ref': '#/definitions/positiveInteger'})
        self.assertEquals(schema['properties']['minProperties'],
            {'$ref': '#/definitions/positiveIntegerDefault0'})
        self.assertEquals(schema['properties']['required'],
            {'$ref': '#/definitions/stringArray'})
        self.assertEquals(schema['properties']['additionalProperties']['anyOf'][1],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['definitions']['additionalProperties'],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['properties']['additionalProperties'],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['patternProperties']['additionalProperties'],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            {'$ref': '#'})
        self.assertEquals(schema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            {'$ref': '#/definitions/stringArray'})
        self.assertEquals(schema['properties']['type']['anyOf'][0],
            {'$ref': '#/definitions/simpleTypes'})
        self.assertEquals(schema['properties']['type']['anyOf'][1]['items'],
            {'$ref': '#/definitions/simpleTypes'})
        self.assertEquals(schema['properties']['allOf'], {'$ref': '#/definitions/schemaArray'})
        self.assertEquals(schema['properties']['anyOf'], {'$ref': '#/definitions/schemaArray'})
        self.assertEquals(schema['properties']['oneOf'], {'$ref': '#/definitions/schemaArray'})
        self.assertEquals(schema['properties']['not'], {'$ref': '#'})

        resolved_schema = v._resolve(schema)
        self.assertEquals(resolved_schema['definitions']['schemaArray']['items'], resolved_schema)
        self.assertEquals(resolved_schema['definitions']['positiveIntegerDefault0']['allOf'][0],
            v._path(resolved_schema, '#/definitions/positiveInteger'))
        self.assertEquals(resolved_schema['definitions']['positiveIntegerDefault0']['allOf'][0],
            resolved_schema['definitions']['positiveInteger'])
        self.assertEquals(resolved_schema['properties']['maxLength'],
            v._path(resolved_schema, '#/definitions/positiveInteger'))
        self.assertEquals(resolved_schema['properties']['maxLength'],
            resolved_schema['definitions']['positiveInteger'])
        self.assertEquals(resolved_schema['properties']['minLength'],
            v._path(resolved_schema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(resolved_schema['properties']['minLength'],
            resolved_schema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(resolved_schema['properties']['additionalItems']['anyOf'][1],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['additionalItems']['anyOf'][1],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][0],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][0],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][1],
            v._path(resolved_schema, '#/definitions/schemaArray'))
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][1],
            resolved_schema['definitions']['schemaArray'])
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][1],
            v._path(resolved_schema, '#/definitions/schemaArray'))
        self.assertEquals(resolved_schema['properties']['items']['anyOf'][1],
            resolved_schema['definitions']['schemaArray'])
        self.assertEquals(resolved_schema['properties']['maxItems'],
            v._path(resolved_schema, '#/definitions/positiveInteger'))
        self.assertEquals(resolved_schema['properties']['maxItems'],
            resolved_schema['definitions']['positiveInteger'])
        self.assertEquals(resolved_schema['properties']['minItems'],
            v._path(resolved_schema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(resolved_schema['properties']['minItems'],
            resolved_schema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(resolved_schema['properties']['maxProperties'],
            v._path(resolved_schema, '#/definitions/positiveInteger'))
        self.assertEquals(resolved_schema['properties']['maxProperties'],
            resolved_schema['definitions']['positiveInteger'])
        self.assertEquals(resolved_schema['properties']['minProperties'],
            v._path(resolved_schema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(resolved_schema['properties']['minProperties'],
            resolved_schema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(resolved_schema['properties']['required'],
            v._path(resolved_schema, '#/definitions/stringArray'))
        self.assertEquals(resolved_schema['properties']['required'],
            resolved_schema['definitions']['stringArray'])
        self.assertEquals(resolved_schema['properties']['additionalProperties']['anyOf'][1],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['additionalProperties']['anyOf'][1],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['definitions']['additionalProperties'],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['definitions']['additionalProperties'],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['properties']['additionalProperties'],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['properties']['additionalProperties'],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['patternProperties']['additionalProperties'],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['patternProperties']['additionalProperties'],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            resolved_schema)
        self.assertEquals(resolved_schema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            v._path(resolved_schema, '#/definitions/stringArray'))
        self.assertEquals(resolved_schema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            resolved_schema['definitions']['stringArray'])
        self.assertEquals(resolved_schema['properties']['type']['anyOf'][0],
            v._path(resolved_schema, '#/definitions/simpleTypes'))
        self.assertEquals(resolved_schema['properties']['type']['anyOf'][0],
            resolved_schema['definitions']['simpleTypes'])
        self.assertEquals(resolved_schema['properties']['type']['anyOf'][1]['items'],
            v._path(resolved_schema, '#/definitions/simpleTypes'))
        self.assertEquals(resolved_schema['properties']['type']['anyOf'][1]['items'],
            resolved_schema['definitions']['simpleTypes'])
        self.assertEquals(resolved_schema['properties']['allOf'],
            v._path(resolved_schema, '#/definitions/schemaArray'))
        self.assertEquals(resolved_schema['properties']['allOf'], resolved_schema['definitions']['schemaArray'])
        self.assertEquals(resolved_schema['properties']['anyOf'],
            v._path(resolved_schema, '#/definitions/schemaArray'))
        self.assertEquals(resolved_schema['properties']['anyOf'], resolved_schema['definitions']['schemaArray'])
        self.assertEquals(resolved_schema['properties']['oneOf'],
            v._path(resolved_schema, '#/definitions/schemaArray'))
        self.assertEquals(resolved_schema['properties']['oneOf'], resolved_schema['definitions']['schemaArray'])
        self.assertEquals(resolved_schema['properties']['not'], v._path(resolved_schema, '#'))
        self.assertEquals(resolved_schema['properties']['not'], resolved_schema)

    def test_path(self):
        v = Draft4Validator({})
        schema = {'properties': {'foo': {'$ref': '#'}}, 'additionalProperties': False}
        resolved_schema = v._resolve(schema)

        schema = {'properties': {'foo': {'type': 'integer'}, 'bar': {'$ref': '#/properties/foo'}}}
        resolved_schema = v._resolve(schema)

        schema = {'items': [{'type': 'integer'},{'$ref': '#/items/0'}]}
        resolved_schema = v._resolve(schema)

        schema = {'tilda~field': {'type': 'integer'}, 'slash/field': {'type': 'integer'},
            'percent%field': {'type': 'integer'}, 'properties':
            {'tilda': {'$ref': '#/tilda~0field'}, 'slash': {'$ref': '#/slash~1field'},
            'percent': {'$ref': '#/percent%25field'}}}
        resolved_schema = v._resolve(schema)
        self.assertEquals(resolved_schema['properties']['tilda'], resolved_schema['tilda~field'])
        self.assertEquals(resolved_schema['properties']['slash'], resolved_schema['slash/field'])
        self.assertEquals(resolved_schema['properties']['percent'], resolved_schema['percent%field'])

        schema = {'definitions': {'a': {'type': 'integer'}, 'b': {'$ref': '#/definitions/a'},
            'c': {'$ref': '#/definitions/b'}}, '$ref': '#/definitions/c'}
        resolved_schema = v._resolve(schema)
        self.assertEquals(resolved_schema['definitions']['b'], {'type': 'integer'})
        self.assertEquals(resolved_schema['definitions']['a'], resolved_schema['definitions']['b'])
        self.assertEquals(resolved_schema['definitions']['b'], resolved_schema['definitions']['c'])
        self.assertEquals(resolved_schema['definitions']['a'], resolved_schema['definitions']['c'])

        schema = {'$ref': 'http://json-schema.org/draft-04/schema#'}
        resolved_schema = v._resolve(schema)
        self.assertNotIn('$ref', resolved_schema)

        schema = {'properties': {'$ref': {'type': 'string'}}}
        resolved_schema = v._resolve(schema)
        self.assertEquals(schema, resolved_schema)

    def test_optionals(self):
        self.run_test(('data', 'JSON-Schema-Test-Suite', 'draft4', 'optional', '*.json'))

    @mock.patch('jsonschemaplus.requests.get')
    def test_draft4(self, mock_get):
        mock_get.side_effect = lambda url: MockRequestResult(url).json()
        self.run_test(self.paths)


class TestValidators(JSONSchemaPlusTest):   
    def test_integer(self):
        self.run_test(('data', 'simple', 'draft4', 'integer.json'))

    def test_enum(self):
        self.run_test(('data', 'simple', 'draft4', 'enum.json'))

    def test_string(self):
        self.run_test(('data', 'simple', 'draft4', 'string.json'))

    def test_number(self):
        self.run_test(('data', 'simple', 'draft4', 'number.json'))

    def test_boolean(self):
        self.run_test(('data', 'simple', 'draft4', 'boolean.json'))


class TestMockRequestResults(unittest.TestCase):
    def test_mock_request_results(self):
        m = MockRequestResult('http://localhost:1234/integer.json')
        data = json.loads(open(path(('data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'integer.json'))).read())
        self.assertEquals(m.json(), data)

        m = MockRequestResult('http://localhost:1234/subSchemas.json#/integer')
        data = json.loads(open(path(('data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'subSchemas.json'))).read())
        self.assertEquals(m.json(), data)

        m = MockRequestResult('http://localhost:1234/folder/folderInteger.json')
        data = json.loads(open(path(('data', 'JSON-Schema-Test-Suite',
            'draft4', 'refRemote', 'folder', 'folderInteger.json'))).read())
        self.assertEquals(m.json(), data)


if __name__ == '__main__':
    unittest.main()
