from jsonschemaplus.resolver import resolve
from jsonschemaplus.schemas import metaschema
from jsonschemaplus.errors import SchemaError
from test.mocks import MockRequestResponse
import unittest


try:
    from urllib2 import URLError
except:
    from urllib.error import URLError


try:
    import mock
except:
    from unittest import mock


class TestResolve(unittest.TestCase):
    def test_resolve_metaschema(self):
        self.assertEqual(metaschema['definitions']['schemaArray']['items'], metaschema)
        self.assertEqual(metaschema['definitions']['positiveIntegerDefault0']['allOf'][0],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEqual(metaschema['definitions']['positiveIntegerDefault0']['allOf'][0],
            metaschema['definitions']['positiveInteger'])
        self.assertEqual(metaschema['properties']['maxLength'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEqual(metaschema['properties']['maxLength'],
            metaschema['definitions']['positiveInteger'])
        self.assertEqual(metaschema['properties']['minLength'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEqual(metaschema['properties']['minLength'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEqual(metaschema['properties']['additionalItems']['anyOf'][1],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['additionalItems']['anyOf'][1],
            metaschema)
        self.assertEqual(metaschema['properties']['items']['anyOf'][0],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['items']['anyOf'][0],
            metaschema)
        self.assertEqual(metaschema['properties']['items']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEqual(metaschema['properties']['items']['anyOf'][1],
            metaschema['definitions']['schemaArray'])
        self.assertEqual(metaschema['properties']['items']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEqual(metaschema['properties']['items']['anyOf'][1],
            metaschema['definitions']['schemaArray'])
        self.assertEqual(metaschema['properties']['maxItems'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEqual(metaschema['properties']['maxItems'],
            metaschema['definitions']['positiveInteger'])
        self.assertEqual(metaschema['properties']['minItems'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEqual(metaschema['properties']['minItems'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEqual(metaschema['properties']['maxProperties'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEqual(metaschema['properties']['maxProperties'],
            metaschema['definitions']['positiveInteger'])
        self.assertEqual(metaschema['properties']['minProperties'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEqual(metaschema['properties']['minProperties'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEqual(metaschema['properties']['required'],
            resolve.path(metaschema, '#/definitions/stringArray'))
        self.assertEqual(metaschema['properties']['required'],
            metaschema['definitions']['stringArray'])
        self.assertEqual(metaschema['properties']['additionalProperties']['anyOf'][1],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['additionalProperties']['anyOf'][1],
            metaschema)
        self.assertEqual(metaschema['properties']['definitions']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['definitions']['additionalProperties'],
            metaschema)
        self.assertEqual(metaschema['properties']['properties']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['properties']['additionalProperties'],
            metaschema)
        self.assertEqual(metaschema['properties']['patternProperties']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['patternProperties']['additionalProperties'],
            metaschema)
        self.assertEqual(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            metaschema)
        self.assertEqual(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/stringArray'))
        self.assertEqual(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            metaschema['definitions']['stringArray'])
        self.assertEqual(metaschema['properties']['type']['anyOf'][0],
            resolve.path(metaschema, '#/definitions/simpleTypes'))
        self.assertEqual(metaschema['properties']['type']['anyOf'][0],
            metaschema['definitions']['simpleTypes'])
        self.assertEqual(metaschema['properties']['type']['anyOf'][1]['items'],
            resolve.path(metaschema, '#/definitions/simpleTypes'))
        self.assertEqual(metaschema['properties']['type']['anyOf'][1]['items'],
            metaschema['definitions']['simpleTypes'])
        self.assertEqual(metaschema['properties']['allOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEqual(metaschema['properties']['allOf'], metaschema['definitions']['schemaArray'])
        self.assertEqual(metaschema['properties']['anyOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEqual(metaschema['properties']['anyOf'], metaschema['definitions']['schemaArray'])
        self.assertEqual(metaschema['properties']['oneOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEqual(metaschema['properties']['oneOf'], metaschema['definitions']['schemaArray'])
        self.assertEqual(metaschema['properties']['not'], resolve.path(metaschema, '#'))
        self.assertEqual(metaschema['properties']['not'], metaschema)

    def test_resolve_schema(self):
        schema = {'properties': {'foo': {'$ref': '#'}}, 'additionalProperties': False}
        resolved_schema = resolve(schema, copy=True)
        self.assertNotEqual(schema, schema['properties']['foo'], 'foo does not point to root')
        self.assertEqual(resolved_schema, resolved_schema['properties']['foo'])
        self.assertNotEqual(schema, resolved_schema, 'test that resolve copy worked')

        schema = {'properties': {'foo': {'type': 'integer'}, 'bar': {'$ref': '#/properties/foo'}}}
        self.assertNotEqual(schema['properties']['foo'], schema['properties']['bar'])
        resolved_schema = resolve(schema)
        self.assertEqual(resolved_schema['properties']['foo'], resolved_schema['properties']['bar'])
        self.assertEqual(schema, resolved_schema)

        schema = {'items': [{'type': 'integer'},{'$ref': '#/items/0'}]}
        self.assertNotEqual(schema['items'][0], schema['items'][1])
        resolve(schema)
        self.assertEqual(schema['items'][0], schema['items'][1])

        schema = {'tilda~field': {'type': 'integer'}, 'slash/field': {'type': 'integer'},
            'percent%field': {'type': 'integer'}, 'properties':
            {'tilda': {'$ref': '#/tilda~0field'}, 'slash': {'$ref': '#/slash~1field'},
            'percent': {'$ref': '#/percent%25field'}}}
        self.assertNotEqual(schema['properties']['tilda'], schema['tilda~field'])
        self.assertNotEqual(schema['properties']['slash'], schema['slash/field'])
        self.assertNotEqual(schema['properties']['percent'], schema['percent%field'])
        resolve(schema)
        self.assertEqual(schema['properties']['tilda'], schema['tilda~field'])
        self.assertEqual(schema['properties']['slash'], schema['slash/field'])
        self.assertEqual(schema['properties']['percent'], schema['percent%field'])

        schema = {'definitions': {'a': {'type': 'integer'}, 'b': {'$ref': '#/definitions/a'},
            'c': {'$ref': '#/definitions/b'}}, '$ref': '#/definitions/c'}
        self.assertNotEqual(schema['definitions']['b'], {'type': 'integer'})
        self.assertNotEqual(schema['definitions']['a'], schema['definitions']['b'])
        self.assertNotEqual(schema['definitions']['b'], schema['definitions']['c'])
        self.assertNotEqual(schema['definitions']['a'], schema['definitions']['c'])
        resolve(schema)
        self.assertEqual(schema['definitions']['b'], {'type': 'integer'})
        self.assertEqual(schema['definitions']['a'], schema['definitions']['b'])
        self.assertEqual(schema['definitions']['b'], schema['definitions']['c'])
        self.assertEqual(schema['definitions']['a'], schema['definitions']['c'])

        schema = {'$ref': 'http://json-schema.org/draft-04/schema#'}
        resolve(schema)
        self.assertNotIn('$ref', schema)

        schema = {'properties': {'$ref': {'type': 'string'}}}
        metaschema = resolve(schema, copy=True)
        self.assertEqual(schema, metaschema, 'schema structure is not modified')

    @mock.patch('jsonschemaplus.resolver.get')
    def test_schema_error(self, mock_get):
        mock_get.side_effect = URLError('error')

        schema = {'id': '#/definitions/a', 'definitions': {'a': {'type': 'integer'}}}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEqual(context.exception.message, 'Error resolving schema with id: #/definitions/a')

        schema = {'id': 'http://example.com/schema#', 'definitions': {'a': {'id': '###'}}}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEqual(context.exception.message, 'Error resolving schema with id: ###')

        schema = {'$ref': 'http://badurl.com/#'}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEqual(context.exception.message, 'Error resolving schema with $ref: http://badurl.com/#')

        schema = {'$ref': 'invalid_uri'}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEqual(context.exception.message, 'Error resolving schema with $ref: invalid_uri')

    def test_path_errors(self):
        schema = {'type': 'object', 'properties': {'foo': {'type': 'integer', 'bar': {'$ref': '#/type'}}}}
        with self.assertRaises(SchemaError) as context:
            resolve.path(schema, '#/properties/foo/type/baz')
        self.assertEqual(context.exception.message, 'Invalid path #/properties/foo/type/baz')

        schema = {'type': 'object', 'properties': {'foo': {'type': 'array', 'items':
            [{'type': 'integer'}, {'type': 'float'}, {'type': 'string'}]}}}
        with self.assertRaises(SchemaError) as context:
            resolve.path(schema, '#/properties/foo/items/b')
        self.assertEqual(context.exception.message, 'Invalid path #/properties/foo/items/b')


if __name__ == '__main__':
    unittest.main()