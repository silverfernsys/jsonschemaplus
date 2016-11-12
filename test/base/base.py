from jsonschemaplus.validators import Draft4Validator
from test.helpers import path, paths
from inspect import stack
import unittest, json


class JSONSchemaPlusTest(unittest.TestCase):
    def run_is_valid(self, path):
        with open(path, 'r') as file:
            for data in json.loads(file.read()):
                validator = Draft4Validator(data['schema'])
                calling_func_name = stack()[1][3]
                for test in data['tests']:
                    is_valid = validator.is_valid(test['data'])
                    self.assertEqual(is_valid, test['valid'], calling_func_name)

    def run_error_count(self, path):
        with open(path, 'r') as file:
            for data in json.loads(file.read()):
                validator = Draft4Validator(data['schema'])
                calling_func_name = stack()[1][3]
                for test in data['tests']:
                    error_count = len(list(validator.errors(test['data'])))
                    # print('error_count: %s, test.error_count: %s' % (error_count, test['error_count']))
                    self.assertEqual(error_count, test['error_count'], calling_func_name)

    def run_validation(self, components):
        if components[-1].startswith('*.'):
            for p in paths(components):
                self.run_is_valid(p)
        else:
            self.run_is_valid(path(components))

    def run_errors(self, components):
        if components[-1].startswith('*.'):
            for p in paths(components):
                self.run_error_count(p)
        else:
            self.run_error_count(path(components))
