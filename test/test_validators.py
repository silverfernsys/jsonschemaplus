import glob, json, unittest
from os.path import join, dirname, abspath
from jsonschemaplus.validators import Draft4Validator
# , formats, types, values, get_type_validator, unique)


def path(*args):
    return join(dirname(abspath(__file__)), *args)


def paths(*args):
    return glob.glob(join(dirname(abspath(__file__)), *args))


class TestValidatorsWithSuite(unittest.TestCase):
    def test_draft4_validator(self):
        self.assertIsNotNone(Draft4Validator({'key': 'value'}))

    # def test_optionals(self):
    #     for file in paths('data', 'draft4', 'optional', '*.json'):
    #         data = json.loads(open(file).read())
    #         # print('data: %s' % data)
    #         for d in data:
    #             # print(d['schema'])
    #             if 'type' in d['schema']:
    #                 validator = types[d['schema']['type']]
    #                 self.assertIn(validator, types.values())
    #             elif 'format' in d['schema']:
    #                 validator =  formats[d['schema']['format']]
    #                 self.assertIn(validator, formats.values())
    #             else:
    #                 validator = None
    #             if validator:
    #                 for t in d['tests']:
    #                     # print('t: %s' % t)
    #                     # try:
    #                     self.assertEquals(validator(t['data']), t['valid'])
    #                     # except:
    #                     #   print('ERROR')

    # def test_type(self):
    #     data = json.loads(open(path('data', 'draft4', 'type.json')).read())
    #     for d in data:
    #         if 'type' in d['schema']:
    #             validator = get_type_validator(d['schema']['type'])
    #             for test in d['tests']:
    #                 self.assertEquals(validator(test['data']), test['valid'])

    # def test_uniqueItems(self):
    #     data = json.loads(open(path('data', 'draft4', 'uniqueItems.json')).read())
    #     for d in data:
    #         if 'uniqueItems' in d['schema']:
    #             validator = unique #get_type_validator(d['schema']['type'])
    #             for test in d['tests']:
    #                 # try:
    #                 self.assertEquals(validator(test['data']), test['valid'])
    #                 # except:
    #                 #     print('data: %s, valid: %s' % (test['data'], test['valid']))

    # def test_maximum(self):
    #     data = json.loads(open(path('data', 'draft4', 'maximum.json')).read())
    #     for d in data:
    #         if 'maximum' in d['schema']:
    #             other = d['schema']['maximum']
    #             exclusive = d['schema'].get('exclusiveMaximum', False)
    #             maximum = values['maximum']
    #             validator = lambda v: maximum(v, other=other, exclusive=exclusive)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_max_items(self):
    #     data = json.loads(open(path('data', 'draft4', 'maxItems.json')).read())
    #     for d in data:
    #         if 'maxItems' in d['schema']:
    #             count = d['schema']['maxItems']
    #             max_items = values['maxItems']
    #             validator = lambda v: max_items(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_max_length(self):
    #     data = json.loads(open(path('data', 'draft4', 'maxLength.json')).read())
    #     for d in data:
    #         if 'maxLength' in d['schema']:
    #             count = d['schema']['maxLength']
    #             max_length = values['maxLength']
    #             validator = lambda v: max_length(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_max_properties(self):
    #     data = json.loads(open(path('data', 'draft4', 'maxProperties.json')).read())
    #     for d in data:
    #         if 'maxProperties' in d['schema']:
    #             count = d['schema']['maxProperties']
    #             max_properties = values['maxProperties']
    #             validator = lambda v: max_properties(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])
    
    # def test_minimum(self):
    #     data = json.loads(open(path('data', 'draft4', 'minimum.json')).read())
    #     for d in data:
    #         if 'minimum' in d['schema']:
    #             other = d['schema']['minimum']
    #             exclusive = d['schema'].get('exclusiveMinimum', False)
    #             minimum = values['minimum']
    #             validator = lambda v: minimum(v, other=other, exclusive=exclusive)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_min_items(self):
    #     data = json.loads(open(path('data', 'draft4', 'minItems.json')).read())
    #     for d in data:
    #         if 'minItems' in d['schema']:
    #             count = d['schema']['minItems']
    #             min_items = values['minItems']
    #             validator = lambda v: min_items(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_min_length(self):
    #     data = json.loads(open(path('data', 'draft4', 'minLength.json')).read())
    #     for d in data:
    #         if 'minLength' in d['schema']:
    #             count = d['schema']['minLength']
    #             min_length = values['minLength']
    #             validator = lambda v: min_length(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_min_properties(self):
    #     data = json.loads(open(path('data', 'draft4', 'minProperties.json')).read())
    #     for d in data:
    #         if 'minProperties' in d['schema']:
    #             count = d['schema']['minProperties']
    #             min_properties = values['minProperties']
    #             validator = lambda v: min_properties(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_multiple_of(self):
    #     data = json.loads(open(path('data', 'draft4', 'multipleOf.json')).read())
    #     for d in data:
    #         if 'multipleOf' in d['schema']:
    #             count = d['schema']['multipleOf']
    #             multiple_of = values['multipleOf']
    #             validator = lambda v: multiple_of(v, count)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    # def test_pattern(self):
    #     data = json.loads(open(path('data', 'draft4', 'pattern.json')).read())
    #     for d in data:
    #         if 'pattern' in d['schema']:
    #             regex = d['schema']['pattern']
    #             pattern = values['pattern']
    #             validator = lambda v: pattern(v, regex)
    #             for t in d['tests']:
    #                 self.assertEquals(validator(t['data']), t['valid'])

    def test_enum(self):
        # This test doesn't handle nested enums!
        for data in json.loads(open(path('data', 'JSON-Schema-Test-Suite', 'draft4', 'enum.json')).read()):
            validator = Draft4Validator(data['schema'])
            for test in data['tests']:
                pass
                # print('\n')
                # print('data: %s' % test['data'])
                # print('schema: %s' % data['schema'])
                # is_valid = validator.is_valid(test['data'])
                # print('valid: %s, is_valid: %s' % (test['valid'], is_valid))
                # self.assertEquals(is_valid, test['valid'])
            # if 'enum' in d['schema']:
            #     enums = d['schema']['enum']
            #     enum = values['enum']
            #     validator = lambda v: enum(v, enums)
            #     for t in d['tests']:
            #         self.assertEquals(validator(t['data']), t['valid'])         


class TestValidators(unittest.TestCase):
    def test_draft4_validator(self):
        self.assertIsNotNone(Draft4Validator({'key': 'value'}))

    def print_details(self, validator, test_data, schema):
        is_valid = validator.is_valid(test_data['data'])
        if is_valid != test_data['valid']:
            print('data: %s' % test_data['data'])
            print('schema: %s' % schema)
            print('is_valid: %s, valid: %s' % (is_valid, test_data['valid']))

    def test_enum(self):
        for data in json.loads(open(path('data', 'simple', 'draft4', 'enum.json')).read()):
            validator = Draft4Validator(data['schema'])
            for test in data['tests']:
                self.print_details(validator, test, data['schema'])
                self.assertEquals(validator.is_valid(test['data']), test['valid'])

    def test_string(self):
        for data in json.loads(open(path('data', 'simple', 'draft4', 'string.json')).read()):
            validator = Draft4Validator(data['schema'])
            for test in data['tests']:
                self.print_details(validator, test, data['schema'])
                self.assertEquals(validator.is_valid(test['data']), test['valid'])

    def test_integer(self):
        for data in json.loads(open(path('data', 'simple', 'draft4', 'integer.json')).read()):
            validator = Draft4Validator(data['schema'])
            for test in data['tests']:
                self.print_details(validator, test, data['schema'])
                self.assertEquals(validator.is_valid(test['data']), test['valid'])

    def test_number(self):
        for data in json.loads(open(path('data', 'simple', 'draft4', 'number.json')).read()):
            validator = Draft4Validator(data['schema'])
            for test in data['tests']:
                self.print_details(validator, test, data['schema'])
                self.assertEquals(validator.is_valid(test['data']), test['valid'])

if __name__ == '__main__':
    unittest.main()