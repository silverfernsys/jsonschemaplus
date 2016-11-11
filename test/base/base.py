from jsonschemaplus.validators import Draft4Validator
from test.helpers import path, paths
from inspect import stack
import unittest, json


class JSONSchemaPlusTest(unittest.TestCase):
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