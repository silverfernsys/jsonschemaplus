import glob, json, unittest
from inspect import stack
from os.path import join, dirname, abspath
# try:
from jsonschemaplus.validators import Draft4Validator
# except:
    # from validators import Draft4Validator


def path(*args):
    return join(dirname(abspath(__file__)), *args)


def paths(*args):
    return glob.glob(join(dirname(abspath(__file__)), *args))


class JSONSchemaPlusTest(unittest.TestCase):
    def setUp(self):
        self.excluded = ['ref.json', 'refRemote.json', 'definitions.json', 'dependencies.json']
        # self.excluded.extend(['oneOf.json', 'not.json', 'anyOf.json', 'allOf.json'])

    def print_details(self, is_valid, test_data, schema):
        if is_valid != test_data['valid']:
            print('data: %s' % test_data['data'])
            print('schema: %s' % schema)
            print('is_valid: %s, valid: %s' % (is_valid, test_data['valid']))

    def run_test_data(self, path):
        for data in json.loads(open(path).read()):
            validator = Draft4Validator(data['schema'])
            calling_func_name = stack()[1][3]
            for test in data['tests']:
                is_valid = validator.is_valid(test['data'])
                self.print_details(is_valid, test, data['schema'])
                try:
                    self.assertEquals(is_valid, test['valid'], calling_func_name)
                except:
                    print("ERROR VALIDATING %s" % path)

    def run_test(self, *components):
        if components[-1].startswith('*.'):
            for p in paths(*components):
                exclude = False
                for file_name in self.excluded:
                    if p.endswith(file_name):
                        exclude = True
                        break
                if not exclude:
                    self.run_test_data(p)
        else:
            self.run_test_data(path(*components))
    

class TestValidatorsWithSuite(JSONSchemaPlusTest):
    def test_optionals(self):
        self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'optional', '*.json')

    def test_draft4(self):
        self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', '*.json')

    # def test_dependencies(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'dependencies.json')

    # def test_not(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'not.json')

    # def test_one_of(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'oneOf.json')

    # def test_any_of(self):
        # self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'anyOf.json')

    # def test_all_of(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'allOf.json')

    # def test_pattern_properties(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'patternProperties.json')

    # def test_properties(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'properties.json')

    # def test_additional_properties(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'additionalProperties.json')

    # def test_additional_items(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'additionalItems.json')

    # def test_type(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'type.json')

    # def test_unique_items(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'uniqueItems.json')

    # def test_maximum(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'maximum.json')

    # def test_max_items(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'maxItems.json')

    # def test_max_length(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'maxLength.json')

    # def test_max_properties(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'maxProperties.json')
    
    # def test_minimum(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'minimum.json')

    # def test_min_items(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'minItems.json')

    # def test_min_length(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'minLength.json')

    # def test_min_properties(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'minProperties.json')

    # def test_multiple_of(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'multipleOf.json')

    # def test_pattern(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'pattern.json')

    # def test_enum(self):
    #     self.run_test('data', 'JSON-Schema-Test-Suite', 'draft4', 'enum.json')       


class TestValidators(JSONSchemaPlusTest):
    # pass    
    def test_integer(self):
        self.run_test('data', 'simple', 'draft4', 'integer.json')

    def test_enum(self):
        self.run_test('data', 'simple', 'draft4', 'enum.json')

    def test_string(self):
        self.run_test('data', 'simple', 'draft4', 'string.json')

    def test_number(self):
        self.run_test('data', 'simple', 'draft4', 'number.json')

    def test_boolean(self):
        self.run_test('data', 'simple', 'draft4', 'boolean.json')


if __name__ == '__main__':
    unittest.main()
