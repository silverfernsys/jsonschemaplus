from collections import Iterable
from copy import deepcopy
from jsonschemaplus.helpers import (email, hostname, ipv4, ipv6, rfc3339, uri, array, boolean, integer,
    null, number, object_, string, valid, maximum, minimum, max_items, min_items,
    max_length, min_length, max_properties, min_properties, multiple_of, enum, unique)
from jsonschemaplus.errors import ValidationError
from jsonschemaplus.schemas.metaschema import metaschema
from jsonschemaplus.schemas.hyperschema import hyperschema


formats = {
    'date-time': rfc3339,
    'email': email,
    'hostname': hostname,
    'ipv4': ipv4,
    'ipv6': ipv6,
    'uri': uri
}


# def build_validator(names):
#     validators = [types.get(name) for name in names if types.get(name)]

#     def validator(value):
#         for v in validators:
#             if v(value):
#                 return True
#         return False

#     return validator


# def get_type_validator(name):
#     if string(name):
#         return types.get(name)
#     else:
#         return build_validator(name)


# values = {
#     'maximum': maximum,
#     'minimum': minimum,
#     'maxItems': max_items,
#     'minItems': min_items,
#     'maxLength': max_length,
#     'minLength': min_length,
#     'maxProperties': max_properties,
#     'minProperties': min_properties,
#     'multipleOf': multiple_of,
#     'pattern': pattern,
#     'enum': enum,
#     'uniqueItems': unique
# }


# validators = {
#     'type': types
# }


# "array", "boolean", "integer", "null", "number", "object", "string"
# keys = {
#     'all': ['not', 'allOf', 'anyOf', 'oneOf'],
#     'object': ['default', 'required', 'properties', 'patternProperties',
#         'minProperties', 'maxProperties', 'additionalProperties',
#         'dependencies'],
#     'array': ['additionalItems', 'items', 'maxItems',
#         'minItems', 'uniqueItems'],
#     'integer': ['maximum', 'minimum', 'multipleOf', 'enum'],
#     'number': ['maximum', 'minimum', 'multipleOf', 'enum'],
#     'string': ['maxLength', 'minLength', 'enum']
# }


# Questions: can a dict or list be 'enum'ed?
class Draft4Validator(object):
    _all_keys = ['enum', 'type', 'allOf', 'anyOf', 'not', 'oneOf']
    _array_keys = ['items', 'maxItems', 'minItems', 'uniqueItems']
    _object_keys = ['dependencies', 'maxProperties', 'minProperties',
        'properties', 'required']
    _num_keys = ['maximum', 'minimum', 'multipleOf']
    _str_keys = ['maxLength', 'minLength']
    _null_keys = []
    
    _keys = {
        dict: _object_keys, list: _array_keys,
        int: _num_keys, float: _num_keys, long: _num_keys,
        str: _str_keys, unicode: _str_keys, type(None): _null_keys
    }

    def __init__(self, schema):
        self._schema = self._resolve(schema)
        self._flag = object()
        self._validators = {
            'allOf': self._all_of,
            'anyOf': self._any_of,
            'dependencies': self._dependencies,
            'enum': self._enum,
            'items': self._items,
            'maximum': self._maximum,
            'maxItems': self._max_items,
            'maxLength': self._max_length,
            'maxProperties': self._max_properties,
            'minimum': self._minimum,
            'minItems': self._min_items,
            'minLength': self._min_length,
            'minProperties': self._min_properties,
            'multipleOf': self._multiple_of,
            'not': self._not,
            'oneOf': self._one_of,
            'properties': self._properties,
            'required': self._required,
            'type': self._type,
            'uniqueItems': self._unique_items
        }

        self._types = {
            'array': array,
            'boolean': boolean,
            'integer': integer,
            'null': null,
            'number': number,
            'object': object_,
            'string': string,
            'valid': valid
        }

    def errors(self, data, flatten=True):
        if flatten:
            return self.flattened_errors(self._errors(data, self._schema))
        else:
            return self._errors(data, self._schema)

    def _errors(self, data, schema):
        try:
            # yield self._validators['enum'](data, schema)

            for key in self._keys[type(data)]:
                yield self._validators[key](data, schema)

            for key in self._all_keys:
                yield self._validators[key](data, schema)
        except KeyError:
            yield ValidationError('Invalid data type: %s' % data.__class__.__name__)

    # def _errors(self, data, schema):
    #     valid_props = self.keys.get(type(data))
    #     if valid_props:
    #         for prop in valid_props:
    #             validator = values.get(prop)
    #             value = schema.get(prop)
    #             if validator and value:
    #                 if not validator(data, value):
    #                     yield ValidationError('Error validating "%s". Expected "%s", got "%s".' % 
    #                         (prop, value, data))
    #             elif value and prop == 'items':
    #                 if type(value) == list:
    #                     if len(value) != len(data):
    #                         yield ValidationError('Error validating "%s". Length of "data" and ' 
    #                             '"items" do not match.' % prop)
    #                     else:
    #                         for i in range(len(value)):
    #                             possible_error = self._errors(data[i], value[i])
    #                             if possible_error:
    #                                 yield possible_error
    #                 elif type(value) == dict:
    #                     for i in range(len(data)):
    #                         possible_error = self._errors(data[i], value)
    #                         if possible_error:
    #                             yield possible_error

    #         # not
    #         not_schema = schema.get('not')
    #         if not_schema:
    #             yield self._not(data, not_schema)

    #         # allOf
    #         all_of_schema = schema.get('allOf')
    #         if all_of_schema:
    #             yield self._all_of(data, all_of_schema)

    #         # anyOf
    #         any_of_schema = schema.get('anyOf')
    #         if any_of_schema:
    #             yield self._any_of(data, any_of_schema)

    #         # oneOf
    #         one_of_schema = schema.get('oneOf')
    #         if one_of_schema:
    #             yield self._one_of(data, one_of_schema)
    #     else:
    #         yield ValidationError('Invalid data type: %s' % data.__class__.__name__)

    # def _enumz(self, data, schema):
    #     enums = schema.get('enum')
    #     if enums and not enum(data, enums):
    #         return ValidationError('%s is not in enum list %s'
    #             % (data, enums))

    def _enum(self, data, schema):
        enums = schema.get('enum')
        if enums and not enum(data, enums):
            yield ValidationError('%s is not in enum list %s'
                % (data, enums))

    def _maximum(self, data, schema):
        max_value = schema.get('maximum')
        exclusive = schema.get('exclusiveMaximum', False)
        if max_value and not maximum(data, max_value, exclusive):
            yield ValidationError('%s is greater than maximum of %s'
                % (data, max_value))

    def _max_items(self, data, schema):
        num_items = schema.get('minItems')
        if num_items and not max_items(data, num_items):
            yield ValidationError('%s contains more than a maximum of %s items.'
                % (data, num_items))

    def _max_length(self, data, schema):
        length = schema.get('maxLength')
        if length and not max_length(data, length):
            yield ValidationError('%s length not under maximum length of %s'
                % (data, length))

    def _minimum(self, data, schema):
        min_value = schema.get('minimum')
        exclusive = schema.get('exclusiveMinimum', False)
        if min_value and not minimum(data, min_value, exclusive):
            yield ValidationError('%s not at least minimum of %s'
                % (data, min_value))

    def _min_items(self, data, schema):
        num_items = schema.get('minItems')
        if num_items and not min_items(data, num_items):
            yield ValidationError('%s does not contain a minimum of %s items.'
                % (data, num_items))

    def _min_length(self, data, schema):
        length = schema.get('minLength')
        if length and not min_length(data, length):
            yield ValidationError('%s length not at least minimum length of %s'
                % (data, length))

    def _multiple_of(self, data, schema):
        multiple = schema.get('multipleOf')
        if multiple and not multiple_of(data, multiple):
            yield ValidationError('%s not multiple of %s.'
                % (data, multiple))

    def _unique_items(self, data, schema):
        if schema.get('uniqueItems', False):
            for i in range(len(array) - 1):
                for j in range(i + 1, len(array)):
                    if (array[i] == array[j] and
                        type(array[i]) == type(array[j])):
                            yield ValidationError('Items are not unique.')

    def _items(self, data, schema):
        item_type = schema.get('items')
        if type(item_type) == dict:
            for item in data:
                yield self._type(item, item_type)
        elif type(item_type) == list:
            if len(item_type) != len(data):
                yield ValidationError('items.length != data.length')
            else:
                for i in range(len(item_type)):
                    yield self._type(data[i], item_type[i])

    def _type(self, data, schema):
        validates = False
        type_name = schema.get('type', 'valid')
        if array(type_name):
            for name in type_name:
                try:
                    validator = self._types[name]
                    if validator(data):
                        validates = True
                        break
                except KeyError:
                    yield ValidationError('Unknown type %s' % name)
            if not validates:
                yield ValidationError('Type of data %s does not match '
                    'types in %s.' % (data.__class__.__name__, type_name))
        elif string(type_name):
            try:
                validator = self._types[type_name]
                if not validator(data):
                    yield ValidationError('Type of data %s does not match %s.'
                        % (data.__class__.__name__, type_name))
            except KeyError:
                yield ValidationError('Unknown type %s' % type_name)
        else:
            yield ValidationError('Unknown type: %s' % type_name)

    # def _object_type(self, data):
    #     if type(data) == dict:
    #         return 'object'
    #     elif type(data) == list:
    #         return 'array'
    #     elif (type(data) == int or type(data) == long):
    #         return 'integer'
    #     elif (type(data) == float):
    #         return 'float'
    #     elif type(data) == None:
    #         return 'null'
    #     elif type(data) == str or type(data) == unicode:
    #         return 'string'

    def _not(self, data, schema):
        not_schema = schema.get('not')
        if not_schema:
            if next(self._errors(data, not_schema), self._flag) == self._flag:
                yield ValidationError('Error validating "%s" with NOT schema "%s".'
                    % (data, not_schema))

    def _all_of(self, data, schema):
        all_of_schema = schema.get('allOf')
        if all_of_schema:
            error_found = False
            for subschema in all_of_schema:
                for error in self._errors(data, subschema):
                    if not error_found:
                        error_found = True
                        yield ValidationError('Error validating "%s" with allOf schema "%s".'
                            % (data, all_of_schema))
                    yield error

    def _any_of(self, data, schema):
        """ Yield an error if all schemas fail. """
        any_of_schema = schema.get('anyOf')
        if any_of_schema:
            error_count = 0
            for subschema in any_of_schema:
                if next(self._errors(data, subschema), self._flag) != self._flag:
                    error_count += 1
            if error_count == len(any_of_schema):
                yield ValidationError('Error validating "%s" with anyOf schema "%s".'
                    % (data, any_of_schema))

    def _one_of(self, data, schema):
        """ Yield an error if more than one or zero schemas validate. """
        one_of_schema = schema.get('oneOf')
        if one_of_schema:
            validate_count = 0
            for subschema in one_of_schema:
                if next(self._errors(data, subschema), self._flag) == self._flag:
                    validate_count += 1
            if validate_count != 1:
                yield ValidationError('Error validating "%s" with oneOf schema "%s".'
                    % (data, one_of_schema))

    def _required(self, data, schema):
        for key in schema.get('required', {}):
            if key not in data:
                yield ValidationError('Error validating "%s." Required property "%s" missing.'
                    % (data, key))

    def _properties(self, data, schema):
        properties = schema.get('properties', {})
        patterns = schema.get('patternProperties', {})
        additional = schema.get('additionalProperties')
        for key in data:
            if key in properties:
                yield self._errors(data[key], properties[key])
            else:
                subschema = self._regex_dict(key, patterns)
                if subschema:
                    yield self._errors(data[key], subschema)
                elif additional:
                    yield self._errors(data[key], additional)

    def _regex_dict(self, key, regex_dict):
        for regex in regex_dict:
            r = re.compile(regex)
            if r.search(key):
                return regex_dict[regex]
        return None

    def _max_properties(self, data, schema):
        maxProperties = schema.get('maxProperties', None)
        if maxProperties != None and len(data.keys()) > maxProperties:
            yield ValidationError('Error validating "%s." Number of keys greater than "%s."'
                % (data, schema))

    def _min_properties(self, data, schema):
        minProperties = schema.get('minProperties', None)
        if minProperties != None and len(data.keys()) < minProperties:
            yield ValidationError('Error validating "%s." Number of keys less than "%s."'
                % (data, schema))

    def _dependencies(self, data, schema):
        for key, value in schema.get('dependencies', {}).items():
            if key in data:
                if type(value) == list:
                    for dependency in value:
                        if dependency not in data:
                            yield ValidationError('Error validating "%s." Missing dependency "%s"'
                                ' of "%s" ' % (data, dependency, key))
                elif type(value) == dict:
                    gen = self._properties(data, value['properties'])
                    err = next(gen, self._flag)
                    if err != self._flag:
                        yield ValidationError('Error validating "%s." Incorrect dependencies.'
                            % data)
                        yield err
                    yield gen

    def flattened_errors(self, it):
        for i in it:
            if (isinstance(i, Iterable) and
                not isinstance(i, str)):
                for y in self.flattened_errors(i):
                    yield y
            else:
                yield i

    def validate(self, data):
        """Validate data against _schema.
        :param data: The data to validate.
        :return: None
        :raises: ValidationError if data does
        not conform to _schema.
        """
        self._validate(data, self._schema)

    def _validate_schema(self, schema):
        self._validate(schema, metaschema)
    
    def _validate(self, data, schema):
        error = next(self.errors(data, schema), self._flag)
        # print('error: %s, flag: %s' % (error, self._flag))
        if error != self._flag:
            # print('ERROR DOES NOT EQUAL FLAG!')
            raise error

    def is_valid(self, data):
        # print('data specific keys: %s' % self._keys[type(data)])
        # print('general keys: %s' % self._all_keys)

        try:
            self.validate(data)
            return True
        except ValidationError as e:
            print('e: %s' % e)
            return False

    def _resolve_refs(self, schema, root, parent=None):
        """Resolve schema references and modify supplied
        schema as a side effect.
        If function parses value that equals schema's root,
        _resolve_refs early exits because references have
        already been resolved.
        :param schema: The schema to resolve.
        :param root: The root of the schema.
        :param parent: The current schema's parent.
        :side effect: Modifies schema.
        :return: None
        :TODO: resolve all http ref values
        """
        ref = '$ref'
        if object_(schema):
            for key, value in schema.items():
                if key == ref:
                    if value == 'http://json-schema.org/draft-04/schema#':
                        schema.pop(key)
                        schema.update(metaschema)
                    elif value[0] == '#':
                        schema.pop(key)
                        subschema = self._path(root, value)
                        schema.update(subschema)
                    else:
                        self._resolve_refs(value, root, schema)
                elif value == root:
                    return
                else:
                    self._resolve_refs(value, root, schema)
        elif array(schema):
            for item in schema:
                if item != root:
                    self._resolve_refs(item, root, schema)

    def _resolve(self, schema):
        """Resolve schema references.
        :param schema: The schema to resolve.
        :return: The resolved schema.
        """
        schema_copy = deepcopy(schema)
        self._resolve_refs(schema_copy, schema_copy)
        return schema_copy

    def _path(self, schema, path):
        path = path[1:].split('/')[1:]
        subschema = schema
        for p in path:
            subschema = subschema.get(p)
        return subschema
