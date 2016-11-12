import unittest
from jsonschemaplus.errors import ValidationError, SchemaError

  
try:
    validation_pattern = unicode('<ValidationError(message=%s)>')
    schema_pattern = unicode('<SchemaError(message=%s)>')
except:
    validation_pattern = '<ValidationError(message=%s)>'
    schema_pattern = '<SchemaError(message=%s)>'


class TestErrors(unittest.TestCase):
    def test_validation_error(self):
    	ve = ValidationError('msg')
    	self.assertIsNotNone(ve)
    	self.assertEqual(ve.__str__(), validation_pattern % 'msg')
    	self.assertEqual(ve.__unicode__(), validation_pattern % 'msg')
    	self.assertEqual(ve.__repr__(), validation_pattern % 'msg')

    def test_schema_error(self):
    	se = SchemaError('msg')
    	self.assertIsNotNone(se)
    	self.assertEqual(se.__str__(), schema_pattern % 'msg')
    	self.assertEqual(se.__unicode__(), schema_pattern % 'msg')
    	self.assertEqual(se.__repr__(), schema_pattern % 'msg')


if __name__ == '__main__':
	unittest.main()
