import re
import sys
from collections import Iterable
from copy import deepcopy
from jsonschemaplus.helpers import (email, hostname, ipv4, ipv6, rfc3339, uri, array, boolean, integer,
    null, number, object_, string, valid, maximum, minimum, max_items, min_items,
    max_length, min_length, max_properties, min_properties, multiple_of, enum, unique)
from jsonschemaplus.errors import ValidationError
from jsonschemaplus.schemas.metaschema import metaschema
from jsonschemaplus.schemas.hyperschema import hyperschema


if sys.version_info > (3,):
    long = int
    unicode = str


# Question: can a dict or list be 'enum'ed?
class Draft4Validator(object):
    _all_keys = ['enum', 'type', 'allOf', 'anyOf', 'not', 'oneOf']
    _array_keys = ['items', 'maxItems', 'minItems', 'uniqueItems']
    _boolean_keys = []
    _object_keys = ['dependencies', 'maxProperties', 'minProperties', 
        'properties', 'patternProperties', 'additionalProperties', 'required']
    _num_keys = ['maximum', 'minimum', 'multipleOf']
    _str_keys = ['format', 'maxLength', 'minLength', 'pattern']
    _null_keys = []
    _properties_keys = ['properties', 'patternProperties', 'additionalProperties']
    
    _keys = {
        dict: _object_keys, list: _array_keys, bool: _boolean_keys,
        int: _num_keys, float: _num_keys, long: _num_keys,
        str: _str_keys, unicode: _str_keys, type(None): _null_keys
    }



    formats = {
        'date-time': rfc3339,
        'email': email,
        'hostname': hostname,
        'ipv4': ipv4,
        'ipv6': ipv6,
        'uri': uri
    }

    def __init__(self, schema):
        self._schema = self._resolve(schema)
        self._flag = object()
        self._validators = {
            'allOf': self._all_of,
            'anyOf': self._any_of,
            'dependencies': self._dependencies,
            'enum': self._enum,
            'format': self._format,
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
            'pattern': self._pattern,
            'properties': self._properties,
            'patternProperties': self._properties,
            'additionalProperties': self._properties,
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

    def errors(self, data, flatten=True, schema=None):
        if schema is None:
            schema = self._schema
        return self.flattened_errors(self._errors(data, schema))

    def _errors(self, data, schema):
        try:
            processed_properties = False
            for key in self._keys[type(data)] + self._all_keys:
                if key in schema:
                    if key not in self._properties_keys:
                        yield self._validators[key](data, schema)
                    elif not processed_properties:
                        processed_properties = True
                        yield self._validators[key](data, schema)
        except KeyError as e:
            yield ValidationError('Invalid data type: %s' % data.__class__.__name__)

    def _enum(self, data, schema):
        enums = schema.get('enum')
        if enums and not enum(data, enums):
            yield ValidationError('%s is not in enum list %s'
                % (data, enums))

    def _format(self, data, schema):
        format_ = schema.get('format')
        if format_:
            validator = self.formats.get(format_)
            if validator:
                if not validator(data):
                    yield ValidationError('"%s" is not of format "%s".'
                        % (data, format_))
            else:
                yield ValidationError('Unrecognized format "%s".'
                    % (format_))

    def _maximum(self, data, schema):
        max_value = schema.get('maximum')
        exclusive = schema.get('exclusiveMaximum', False)
        if max_value and not maximum(data, max_value, exclusive):
            yield ValidationError('%s is greater than maximum of %s'
                % (data, max_value))

    def _max_items(self, data, schema):
        num_items = schema.get('maxItems')
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
            for i in range(len(data) - 1):
                for j in range(i + 1, len(data)):
                    if (data[i] == data[j] and
                        type(data[i]) == type(data[j])):
                            yield ValidationError('Items are not unique.')

    def _items(self, data, schema):
        item_type = schema.get('items')
        if type(item_type) == dict:
            for item in data:
                yield self._type(item, item_type)
        elif type(item_type) == list:
            additional_items = schema.get('additionalItems', True)
            if len(item_type) > len(data):
                yield ValidationError('items.length > data.length')
            else:
                for i in range(len(item_type)):
                    yield self._type(data[i], item_type[i])
                if len(item_type) < len(data):
                    if additional_items == False:
                        yield ValidationError('No additional items allowed.')
                    elif type(additional_items) == dict:
                        for i in range(len(item_type), len(data)):
                            yield self._type(data[i], additional_items)

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

    def _not(self, data, schema):
        not_schema = schema.get('not')
        if not_schema is not None:
            if next(self.flattened_errors(self._errors(data, not_schema)), self._flag) == self._flag:
                yield ValidationError('Error validating "%s" with NOT schema "%s".'
                    % (data, not_schema))

    def _all_of(self, data, schema):
        all_of_schema = schema.get('allOf')
        if all_of_schema is not None:
            error_found = False
            for subschema in all_of_schema:
                for error in self.flattened_errors(self._errors(data, subschema)):
                    if not error_found:
                        error_found = True
                        yield ValidationError('Error validating "%s" with allOf schema "%s".'
                            % (data, all_of_schema))
                    yield error

    def _any_of(self, data, schema):
        """ Yield an error if all schemas fail. """
        any_of_schema = schema.get('anyOf')
        if any_of_schema is not None:
            error_count = 0
            for subschema in any_of_schema:
                if next(self.flattened_errors(self._errors(data, subschema)), self._flag) != self._flag:
                    error_count += 1
            if error_count == len(any_of_schema):
                yield ValidationError('Error validating "%s" with anyOf schema "%s".'
                    % (data, any_of_schema))

    def _one_of(self, data, schema):
        """ Yield an error if more than one or zero schemas validate. """
        one_of_schema = schema.get('oneOf')
        if one_of_schema is not None:
            validate_count = 0
            for subschema in one_of_schema:
                if next(self.flattened_errors(self._errors(data, subschema)), self._flag) == self._flag:
                    validate_count += 1
            if validate_count != 1:
                yield ValidationError('Error validating "%s" with oneOf schema "%s".'
                    % (data, one_of_schema))

    def _required(self, data, schema):
        for key in schema.get('required', {}):
            if key not in data:
                yield ValidationError('Error validating "%s." Required property "%s" missing.'
                    % (data, key))

    def _pattern(self, data, schema):
        regex = schema.get('pattern')
        if regex:
            r = re.compile(regex)
            if not r.search(data):
                yield ValidationError('Error validating "%s." Does not match pattern "%s".'
                    % (data, regex))

    def _properties(self, data, schema):
        properties = schema.get('properties', {})
        patterns = schema.get('patternProperties', {})
        additional = schema.get('additionalProperties', True)
        for key in data:
            # print('key: %s' % key)
            if key in properties:
                # print('data[key]: %s, properties[key]: %s' % (data[key], properties[key]))
                yield self.flattened_errors(self._errors(data[key], properties[key]))
            subschemas = self._regex_dict(key, patterns)
            # print('subschemas: %s' % subschemas)
            if len(subschemas) > 0:
                for subschema in subschemas:
                    yield self.flattened_errors(self._errors(data[key], subschema))
            elif key not in properties:
                if type(additional) == bool:
                    if not additional:
                        yield ValidationError('Error validating "%s". Key %s not allowed.'
                            % (data, key))
                else:
                    yield self.flattened_errors(self._errors(data[key], additional))

    def _regex_dict(self, key, regex_dict):
        matches = []
        for regex in regex_dict:
            r = re.compile(regex)
            if r.search(key):
                matches.append(regex_dict[regex])
        return matches

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
        # print('*** error: %s' % error)
        if error != self._flag:
            raise error

    def is_valid(self, data):
        try:
            self.validate(data)
            return True
        except ValidationError:
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
