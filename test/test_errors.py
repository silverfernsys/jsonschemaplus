import sys, unittest
from jsonschemaplus.errors import ValidationError, SchemaError


if sys.version_info > (3,):
    validation_pattern = '<ValidationError(message=%s)>'
    schema_pattern = '<SchemaError(message=%s)>'
else:
    validation_pattern = u'<ValidationError(message=%s)>'
    schema_pattern = u'<SchemaError(message=%s)>'


class TestErrors(unittest.TestCase):
    def test_validation_error(self):
    	ve = ValidationError('msg')
    	self.assertIsNotNone(ve)
    	self.assertEquals(ve.__str__(), validation_pattern % 'msg')
    	self.assertEquals(ve.__unicode__(), validation_pattern % 'msg')
    	self.assertEquals(ve.__repr__(), validation_pattern % 'msg')

    def test_schema_error(self):
    	se = SchemaError('msg')
    	self.assertIsNotNone(se)
    	self.assertEquals(se.__str__(), schema_pattern % 'msg')
    	self.assertEquals(se.__unicode__(), schema_pattern % 'msg')
    	self.assertEquals(se.__repr__(), schema_pattern % 'msg')


if __name__ == '__main__':
	unittest.main()