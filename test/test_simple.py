from os.path import dirname, abspath
from test.base import JSONSchemaPlusTest
import unittest

root = dirname(abspath(__file__))


class TestValidators(JSONSchemaPlusTest):   
    def test_integer(self):
        self.run_test((root, 'data', 'simple', 'draft4', 'integer.json'))

    def test_enum(self):
        self.run_test((root, 'data', 'simple', 'draft4', 'enum.json'))

    def test_string(self):
        self.run_test((root, 'data', 'simple', 'draft4', 'string.json'))

    def test_number(self):
        self.run_test((root, 'data', 'simple', 'draft4', 'number.json'))

    def test_boolean(self):
        self.run_test((root, 'data', 'simple', 'draft4', 'boolean.json'))


if __name__ == '__main__':
    unittest.main()
