import unittest
from jsonschemaplus.errors import ValidationError, SchemaError, validation_pattern, schema_pattern


class TestErrors(unittest.TestCase):
    def test_validation_error(self):
        v = ValidationError(ValidationError.Type.ENUM, ['a', 'b', 'c'], 'd', misc='something')
        t = (ValidationError.Type.ENUM.name, ['a', 'b', 'c'], 'd', None)
        self.assertEqual(v.__str__(), validation_pattern % t)
        self.assertEqual(v.__unicode__(), validation_pattern % t)
        self.assertEqual(v.__repr__(), validation_pattern % t)
        self.assertEqual(v.error, ValidationError.Type.ENUM)
        self.assertEqual(v.schema, ['a', 'b', 'c'])
        self.assertEqual(v.data, 'd')

    def test_schema_error(self):
        se = SchemaError('msg')
        self.assertIsNotNone(se)
        self.assertEqual(se.__str__(), schema_pattern % 'msg')
        self.assertEqual(se.__unicode__(), schema_pattern % 'msg')
        self.assertEqual(se.__repr__(), schema_pattern % 'msg')


if __name__ == '__main__':
    unittest.main()
