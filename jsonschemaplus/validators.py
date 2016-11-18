import re
import sys
from collections import Iterable
from copy import deepcopy
from inspect import stack
from jsonschemaplus.helpers import (email, hostname, ipv4, ipv6, rfc3339, uri, array, boolean, integer,
    null, number, object_, string, valid, maximum, minimum, max_items, min_items,
    max_length, min_length, max_properties, min_properties, multiple_of, enum, unique)
from jsonschemaplus.errors import ValidationError, SchemaError
from jsonschemaplus.schemas import metaschema, hyperschema
from jsonschemaplus.parsers import url
from jsonschemaplus.requests import get
from jsonschemaplus.resolver import resolve
from jsonschemaplus.gen import ParserIterator


try:
    from itertools import izip as zip
except:
    pass


if sys.version_info > (3,):
    long = int
    unicode = str


class Draft4Validator(object):
    _substitutions = {'%25': '%', '~1': '/', '~0': '~'}
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
        self._schema = resolve(schema)
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
            'string': string
        }

        self._regex_cache = {}

    def errors(self, data, schema=None):
        if schema is None:
            schema = self._schema
        return ParserIterator(self._errors(data, schema))

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
            yield ValidationError(ValidationError.Type.TYPE, self._types.keys(), data)

    def _enum(self, data, schema):
        enums = schema.get('enum')
        if enums and not enum(data, enums):
            yield ValidationError(ValidationError.Type.ENUM, enums, data)

    def _format(self, data, schema):
        format_ = schema.get('format')
        validator = self.formats.get(format_)
        if validator:
            if not validator(data):
                yield ValidationError(ValidationError.Type.FORMAT, format_, data)
        else:
            # TODO: this should be moved to schema validation!
            yield ValidationError(ValidationError.Type.FORMAT, format_, data)

    def _maximum(self, data, schema):
        max_value = schema.get('maximum')
        exclusive = schema.get('exclusiveMaximum', False)
        if max_value is not None and not maximum(data, max_value, exclusive):
            yield ValidationError(ValidationError.Type.MAXIMUM, max_value, data, exclusive=exclusive)

    def _max_items(self, data, schema):
        num_items = schema.get('maxItems')
        if num_items is not None and not max_items(data, num_items):
            yield ValidationError(ValidationError.Type.MAX_ITEMS, num_items, data)

    def _max_length(self, data, schema):
        length = schema.get('maxLength')
        if length is not None and not max_length(data, length):
            yield ValidationError(ValidationError.Type.MAX_LENGTH, length, data)

    def _minimum(self, data, schema):
        min_value = schema.get('minimum')
        exclusive = schema.get('exclusiveMinimum', False)
        if min_value is not None and not minimum(data, min_value, exclusive):
            yield ValidationError(ValidationError.Type.MINIMUM, min_value, data, exclusive=exclusive)

    def _min_items(self, data, schema):
        num_items = schema.get('minItems')
        if num_items is not None and not min_items(data, num_items):
            yield ValidationError(ValidationError.Type.MIN_ITEMS, num_items, data)

    def _min_length(self, data, schema):
        length = schema.get('minLength')
        if length is not None and not min_length(data, length):
            yield ValidationError(ValidationError.Type.MIN_LENGTH, length, data)

    def _multiple_of(self, data, schema):
        multiple = schema.get('multipleOf')
        if multiple is not None and not multiple_of(data, multiple):
            yield ValidationError(ValidationError.Type.MULTIPLE_OF, multiple, data)

    def _unique_items(self, data, schema):
        if schema.get('uniqueItems', False):
            for i, x in enumerate(data[0:-1]):
                for y in data[i + 1:]:
                    if(x == y and type(x) == type(y)):
                        yield ValidationError(ValidationError.Type.UNIQUE_ITEMS, True, data)
    
    def _items(self, data, schema):
        items = schema.get('items')
        if type(items) == dict:
            for item in data:
                yield self.errors(item, items)
        else:
            additional = schema.get('additionalItems', True)
            if len(items) > len(data):
                yield ValidationError(ValidationError.Type.ITEMS, items, data)
            else:
                for x, y in zip(data, items):
                    yield self.errors(x, y)
                len_data = len(data)
                len_items = len(items)
                if len_data > len_items:
                    if additional == False:
                        yield ValidationError(ValidationError.Type.ADDITIONAL_ITEMS, False, data[len_items:])
                    elif type(additional) == dict:
                        for x in data[len_items:]:
                            yield self.errors(x, additional)

    def _type(self, data, schema):
        type_ = schema.get('type')
        if array(type_):
            validates = False
            for t in type_:
                validator = self._types[t]
                if validator(data):
                    validates = True
                    break
            if not validates:
                yield ValidationError(ValidationError.Type.TYPE, t, data)
        else:
            validator = self._types[type_]
            if not validator(data):
                yield ValidationError(ValidationError.Type.TYPE, type_, data)

    def _not(self, data, schema):
        not_schema = schema.get('not')
        if not self.errors(data, not_schema).lookahead():
            yield ValidationError(ValidationError.Type.NOT, not_schema, data)

    def _all_of(self, data, schema):
        all_of_schema = schema.get('allOf')
        invalid_schemas = []
        errors = []
        for subschema in all_of_schema:
            subschema_errors = self.errors(data, subschema)
            if subschema_errors.lookahead():
                invalid_schemas.append(subschema)
                errors.append(subschema_errors)
        if len(errors):
            yield ValidationError(ValidationError.Type.ALL_OF, invalid_schemas, data, errors=errors)

    def _any_of(self, data, schema):
        any_of_schema = schema.get('anyOf')
        error_count = 0
        for subschema in any_of_schema:
            subschema_errors = self.errors(data, subschema)
            if subschema_errors.lookahead():
                error_count += 1
        if error_count == len(any_of_schema):
            yield ValidationError(ValidationError.Type.ANY_OF, any_of_schema, data)

    def _one_of(self, data, schema):
        one_of_schema = schema.get('oneOf')
        validate_count = 0
        validated_subschemas = []
        for subschema in one_of_schema:
            subschema_errors = self.errors(data, subschema)
            if not subschema_errors.lookahead():
                validate_count += 1
                validated_subschemas.append(subschema)
        if validate_count != 1:
            yield ValidationError(ValidationError.Type.ONE_OF, schema, data, validated=validated_subschemas)

    def _required(self, data, schema):
        for key in schema.get('required', {}):
            if key not in data:
                yield ValidationError(ValidationError.Type.REQUIRED, key, data)

    def _pattern(self, data, schema):
        regex = schema.get('pattern')

        try:
            r = self._regex_cache(regex)
        except:
            r = re.compile(regex)
            self._regex_cache[regex] = r

        if not r.search(data):
            yield ValidationError(ValidationError.Type.PATTERN, regex, data)

    def _properties(self, data, schema):
        properties = schema.get('properties', {})
        patterns = schema.get('patternProperties', {})
        additional = schema.get('additionalProperties', True)
        for key in data:
            if key in properties:
                yield self.errors(data[key], properties[key])
            subschemas = self._regex_keys(key, patterns)
            if len(subschemas) > 0:
                for subschema in subschemas:
                    yield self.errors(data[key], subschema)
            elif key not in properties:
                if type(additional) == bool:
                    if not additional:
                        yield ValidationError(ValidationError.Type.ADDITIONAL_PROPERTIES, False, key)
                else:
                    yield self.errors(data[key], additional)

    def _regex_keys(self, key, regex_dict):
        matches = []
        for regex in regex_dict:
            try:
                r = self._regex_cache[regex]
            except:
                r = re.compile(regex)
                self._regex_cache[regex] = r

            if r.search(key):
                matches.append(regex_dict[regex])
        return matches

    def _max_properties(self, data, schema):
        maxProperties = schema.get('maxProperties', None)
        len_data = len(data)
        if maxProperties != None and len_data > maxProperties:
            yield ValidationError(ValidationError.Type.MAX_PROPERTIES, maxProperties, len_data)

    def _min_properties(self, data, schema):
        minProperties = schema.get('minProperties', None)
        len_data = len(data)
        if minProperties != None and len_data < minProperties:
            yield ValidationError(ValidationError.Type.MIN_PROPERTIES, minProperties, len_data)

    def _dependencies(self, data, schema):
        # TODO: ensure the logic in this function is solid.
        # Write more detailed tests to ensure code handles corner cases.
        for key, value in schema.get('dependencies', {}).items():
            if key in data:
                if type(value) == list:
                    for dependency in value:
                        if dependency not in data:
                            # TODO: This makes no sense! What about dependencies that don't validate?!
                            yield ValidationError(ValidationError.Type.DEPENDENCIES, dependency, data)
                        else:
                            yield self.errors(data, dependency)
                else:
                    errors = ParserIterator(self._properties(data, value))
                    error = errors.lookahead()
                    if error:
                        # TODO: I disagree with this now. It's not that the dependency is missing, but
                        # that the schema of the dependency didn't validate. So just yield the subschema's
                        # errors and remove this dependency error.
                        yield ValidationError(ValidationError.Type.DEPENDENCIES, error.schema, error.data, errors=errors)

    def validate(self, data):
        """Validate data against schema.
        :param data: The data to validate.
        :return: None
        :raises: ValidationError if data does not conform to _schema."""
        self._validate(data, self._schema)

    def _validate_schema(self, schema):
        self._validate(schema, metaschema)
    
    def _validate(self, data, schema):
        errors = self.errors(data, schema)
        error = errors.lookahead()
        if error:
            raise error

    def is_valid(self, data):
        """Validate data against schema.
        :param data: The data to validate.
        :return: boolean True if valid, False otherwise."""
        try:
            self.validate(data)
            return True
        except ValidationError:
            return False

    def is_schema_valid(self):
        """Validate schema against metaschema.
        :return boolean True if valid, False otherwise."""
        try:
            self._validate_schema(self._schema)
            return True
        except ValidationError:
            return False
