from jsonschemaplus.resolver import resolve
from jsonschemaplus.schemas import metaschema
from jsonschemaplus.errors import SchemaError
from test.mocks import MockRequestResponse
import unittest


try:
    from urllib2 import URLError
    import mock
except:
    from urllib.error import URLError
    from unittest import mock


class TestResolve(unittest.TestCase):
    def test_resolve_metaschema(self):
        self.assertEquals(metaschema['definitions']['schemaArray']['items'], metaschema)
        self.assertEquals(metaschema['definitions']['positiveIntegerDefault0']['allOf'][0],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEquals(metaschema['definitions']['positiveIntegerDefault0']['allOf'][0],
            metaschema['definitions']['positiveInteger'])
        self.assertEquals(metaschema['properties']['maxLength'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEquals(metaschema['properties']['maxLength'],
            metaschema['definitions']['positiveInteger'])
        self.assertEquals(metaschema['properties']['minLength'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(metaschema['properties']['minLength'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(metaschema['properties']['additionalItems']['anyOf'][1],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['additionalItems']['anyOf'][1],
            metaschema)
        self.assertEquals(metaschema['properties']['items']['anyOf'][0],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['items']['anyOf'][0],
            metaschema)
        self.assertEquals(metaschema['properties']['items']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEquals(metaschema['properties']['items']['anyOf'][1],
            metaschema['definitions']['schemaArray'])
        self.assertEquals(metaschema['properties']['items']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEquals(metaschema['properties']['items']['anyOf'][1],
            metaschema['definitions']['schemaArray'])
        self.assertEquals(metaschema['properties']['maxItems'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEquals(metaschema['properties']['maxItems'],
            metaschema['definitions']['positiveInteger'])
        self.assertEquals(metaschema['properties']['minItems'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(metaschema['properties']['minItems'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(metaschema['properties']['maxProperties'],
            resolve.path(metaschema, '#/definitions/positiveInteger'))
        self.assertEquals(metaschema['properties']['maxProperties'],
            metaschema['definitions']['positiveInteger'])
        self.assertEquals(metaschema['properties']['minProperties'],
            resolve.path(metaschema, '#/definitions/positiveIntegerDefault0'))
        self.assertEquals(metaschema['properties']['minProperties'],
            metaschema['definitions']['positiveIntegerDefault0'])
        self.assertEquals(metaschema['properties']['required'],
            resolve.path(metaschema, '#/definitions/stringArray'))
        self.assertEquals(metaschema['properties']['required'],
            metaschema['definitions']['stringArray'])
        self.assertEquals(metaschema['properties']['additionalProperties']['anyOf'][1],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['additionalProperties']['anyOf'][1],
            metaschema)
        self.assertEquals(metaschema['properties']['definitions']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['definitions']['additionalProperties'],
            metaschema)
        self.assertEquals(metaschema['properties']['properties']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['properties']['additionalProperties'],
            metaschema)
        self.assertEquals(metaschema['properties']['patternProperties']['additionalProperties'],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['patternProperties']['additionalProperties'],
            metaschema)
        self.assertEquals(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][0],
            metaschema)
        self.assertEquals(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            resolve.path(metaschema, '#/definitions/stringArray'))
        self.assertEquals(metaschema['properties']['dependencies']['additionalProperties']['anyOf'][1],
            metaschema['definitions']['stringArray'])
        self.assertEquals(metaschema['properties']['type']['anyOf'][0],
            resolve.path(metaschema, '#/definitions/simpleTypes'))
        self.assertEquals(metaschema['properties']['type']['anyOf'][0],
            metaschema['definitions']['simpleTypes'])
        self.assertEquals(metaschema['properties']['type']['anyOf'][1]['items'],
            resolve.path(metaschema, '#/definitions/simpleTypes'))
        self.assertEquals(metaschema['properties']['type']['anyOf'][1]['items'],
            metaschema['definitions']['simpleTypes'])
        self.assertEquals(metaschema['properties']['allOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEquals(metaschema['properties']['allOf'], metaschema['definitions']['schemaArray'])
        self.assertEquals(metaschema['properties']['anyOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEquals(metaschema['properties']['anyOf'], metaschema['definitions']['schemaArray'])
        self.assertEquals(metaschema['properties']['oneOf'],
            resolve.path(metaschema, '#/definitions/schemaArray'))
        self.assertEquals(metaschema['properties']['oneOf'], metaschema['definitions']['schemaArray'])
        self.assertEquals(metaschema['properties']['not'], resolve.path(metaschema, '#'))
        self.assertEquals(metaschema['properties']['not'], metaschema)

    def test_resolve_schema(self):
        schema = {'properties': {'foo': {'$ref': '#'}}, 'additionalProperties': False}
        resolved_schema = resolve(schema, copy=True)
        self.assertNotEquals(schema, schema['properties']['foo'], 'foo does not point to root')
        self.assertEquals(resolved_schema, resolved_schema['properties']['foo'])
        self.assertNotEquals(schema, resolved_schema, 'test that resolve copy worked')

        schema = {'properties': {'foo': {'type': 'integer'}, 'bar': {'$ref': '#/properties/foo'}}}
        self.assertNotEquals(schema['properties']['foo'], schema['properties']['bar'])
        resolved_schema = resolve(schema)
        self.assertEquals(resolved_schema['properties']['foo'], resolved_schema['properties']['bar'])
        self.assertEquals(schema, resolved_schema)

        schema = {'items': [{'type': 'integer'},{'$ref': '#/items/0'}]}
        self.assertNotEquals(schema['items'][0], schema['items'][1])
        resolve(schema)
        self.assertEquals(schema['items'][0], schema['items'][1])

        schema = {'tilda~field': {'type': 'integer'}, 'slash/field': {'type': 'integer'},
            'percent%field': {'type': 'integer'}, 'properties':
            {'tilda': {'$ref': '#/tilda~0field'}, 'slash': {'$ref': '#/slash~1field'},
            'percent': {'$ref': '#/percent%25field'}}}
        self.assertNotEquals(schema['properties']['tilda'], schema['tilda~field'])
        self.assertNotEquals(schema['properties']['slash'], schema['slash/field'])
        self.assertNotEquals(schema['properties']['percent'], schema['percent%field'])
        resolve(schema)
        self.assertEquals(schema['properties']['tilda'], schema['tilda~field'])
        self.assertEquals(schema['properties']['slash'], schema['slash/field'])
        self.assertEquals(schema['properties']['percent'], schema['percent%field'])

        schema = {'definitions': {'a': {'type': 'integer'}, 'b': {'$ref': '#/definitions/a'},
            'c': {'$ref': '#/definitions/b'}}, '$ref': '#/definitions/c'}
        self.assertNotEquals(schema['definitions']['b'], {'type': 'integer'})
        self.assertNotEquals(schema['definitions']['a'], schema['definitions']['b'])
        self.assertNotEquals(schema['definitions']['b'], schema['definitions']['c'])
        self.assertNotEquals(schema['definitions']['a'], schema['definitions']['c'])
        resolve(schema)
        self.assertEquals(schema['definitions']['b'], {'type': 'integer'})
        self.assertEquals(schema['definitions']['a'], schema['definitions']['b'])
        self.assertEquals(schema['definitions']['b'], schema['definitions']['c'])
        self.assertEquals(schema['definitions']['a'], schema['definitions']['c'])

        schema = {'$ref': 'http://json-schema.org/draft-04/schema#'}
        resolve(schema)
        self.assertNotIn('$ref', schema)

        schema = {'properties': {'$ref': {'type': 'string'}}}
        metaschema = resolve(schema, copy=True)
        self.assertEquals(schema, metaschema, 'schema structure is not modified')

    @mock.patch('jsonschemaplus.resolver.get')
    def test_schema_error(self, mock_get):
        mock_get.side_effect = URLError('error')

        schema = {'id': '#/definitions/a', 'definitions': {'a': {'type': 'integer'}}}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEquals(context.exception.message, 'Error resolving schema with id: #/definitions/a')

        schema = {'id': 'http://example.com/schema#', 'definitions': {'a': {'id': '###'}}}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEquals(context.exception.message, 'Error resolving schema with id: ###')

        schema = {'$ref': 'http://badurl.com/#'}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEquals(context.exception.message, 'Error resolving schema with $ref: http://badurl.com/#')

        schema = {'$ref': 'invalid_uri'}
        with self.assertRaises(SchemaError) as context:
            resolve(schema)
        self.assertEquals(context.exception.message, 'Error resolving schema with $ref: invalid_uri')

    def test_path_errors(self):
        schema = {'type': 'object', 'properties': {'foo': {'type': 'integer', 'bar': {'$ref': '#/type'}}}}
        with self.assertRaises(SchemaError) as context:
            resolve.path(schema, '#/properties/foo/type/baz')
        self.assertEquals(context.exception.message, 'Invalid path #/properties/foo/type/baz')

        schema = {'type': 'object', 'properties': {'foo': {'type': 'array', 'items':
            [{'type': 'integer'}, {'type': 'float'}, {'type': 'string'}]}}}
        with self.assertRaises(SchemaError) as context:
            resolve.path(schema, '#/properties/foo/items/b')
        self.assertEquals(context.exception.message, 'Invalid path #/properties/foo/items/b')


if __name__ == '__main__':
    unittest.main()