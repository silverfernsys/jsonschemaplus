from test.base import JSONSchemaPlusTest
from os.path import dirname, abspath
import unittest


root = dirname(abspath(__file__))


class TestValidators(JSONSchemaPlusTest):   
    def test_command(self):
        self.run_test((root, 'data', 'complex', 'draft4', 'command.json'))

    def test_snapshot(self):
        self.run_test((root, 'data', 'complex', 'draft4', 'snapshot.json'))

    def test_state(self):
        self.run_test((root, 'data', 'complex', 'draft4', 'state.json'))

    def test_system(self):
        self.run_test((root, 'data', 'complex', 'draft4', 'system.json'))

    def test_test(self):
        self.run_test((root, 'data', 'complex', 'draft4', 'test.json'))


if __name__ == '__main__':
    unittest.main()
