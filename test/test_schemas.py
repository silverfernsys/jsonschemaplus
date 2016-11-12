from jsonschemaplus.validators import Draft4Validator
from test.helpers import path, paths
from os.path import dirname, abspath
from inspect import stack
import unittest, json


root = dirname(abspath(__file__))
   

class TestValidatorsWithSuite(unittest.TestCase):
    def run_is_schema_valid(self, path):
        with open(path, 'r') as file:
            for data in json.loads(file.read()):
                calling_func_name = stack()[1][3]
                for test in data['tests']:
                    validator = Draft4Validator(test['data'])
                    is_schema_valid = validator.is_schema_valid()
                    self.assertEqual(is_schema_valid, test['valid'], calling_func_name)

    def run_validation(self, components):
        if components[-1].startswith('*.'):
            for p in paths(components):
                self.run_is_schema_valid(p)
        else:
            self.run_is_schema_valid(path(components))

    def test_schemas(self):
        self.run_validation((root, 'data', 'other', 'draft4', 'schemas.json'))


if __name__ == '__main__':
    unittest.main()
