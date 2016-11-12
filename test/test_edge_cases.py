from jsonschemaplus.validators import Draft4Validator
from inspect import stack
import unittest


class TestValidatorsWithEdgeCases(unittest.TestCase):
    def run_validation_with_object(self, obj, schema, valid):
        calling_func_name = stack()[1][3]
        validator = Draft4Validator(schema)
        is_valid = validator.is_valid(obj)
        self.assertEqual(is_valid, valid, calling_func_name)

    def test_unknown_data_type(self):
        obj = object()
        schema = {'type': 'object', 'properties': {'a': {'type': 'integer'}}}
        valid = False
        self.run_validation_with_object(obj, schema, valid)

    def test_unknown_type(self):
        obj = 123
        schema = {'type': ['object', 'unknown']}
        valid = False
        self.run_validation_with_object(obj, schema, valid)

        obj = 123
        schema = {'type': 'unknown'}
        valid = False
        self.run_validation_with_object(obj, schema, valid)

        obj = 123
        schema = {'type': {'data': 'bad'}}
        valid = False
        self.run_validation_with_object(obj, schema, valid)


if __name__ == '__main__':
    unittest.main()
