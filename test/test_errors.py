import unittest
from jsonschemaplus.errors import ValidationError, SchemaError


class TestErrors(unittest.TestCase):
    def test_validation_error(self):
    	self.assertIsNotNone(ValidationError())

    def test_schema_error(self):
    	self.assertIsNotNone(SchemaError())