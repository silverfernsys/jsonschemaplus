import unittest
from jsonschemaplus.validators import Draft4Validator


class TestValidators(unittest.TestCase):
    def test_draft4_validator(self):
    	self.assertIsNotNone(Draft4Validator({'key': 'value'}))
