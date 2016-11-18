from enum import Enum


try:
    validation_pattern = unicode('<ValidationError(error=%s, schema=%s, data=%s, details=%s)>')
    schema_pattern = unicode('<SchemaError(message=%s)>')
except:
    validation_pattern = '<ValidationError(error=%s, schema=%s, data=%s, details=%s)>'
    schema_pattern = '<SchemaError(message=%s)>'    


class ValidationError(Exception):
    Type = Enum('ValidationErrorType', 'ALL_OF ANY_OF DEPENDENCIES ENUM ' \
        'FORMAT ITEMS ADDITIONAL_ITEMS MAXIMUM MAX_ITEMS MAX_LENGTH ' \
        'MAX_PROPERTIES MINIMUM MIN_ITEMS MIN_LENGTH MIN_PROPERTIES MULTIPLE_OF ' \
        'NOT ONE_OF PATTERN PROPERTIES PATTERN_PROPERTIES ADDITIONAL_PROPERTIES ' \
        'REQUIRED TYPE UNIQUE_ITEMS')

        # 'allOf anyOf dependencies ' \
        # 'enum format items additionalItems maximum maxItems maxLength maxProperties minimum ' \
        # 'minItems minLength minProperties multipleOf NOT oneOf pattern properties ' \
        # 'patternProperties additionalProperties required type uniqueItems')

    def __init__(self, error, schema, data, **kwargs):
        self.error = error
        self.schema = schema
        self.data = data
        self.details = None
        self.__dict__.update(kwargs)

    def __str__(self):
    	return validation_pattern % (self.error.name, self.schema, self.data, self.details)

    def __unicode__(self):
    	return validation_pattern % (self.error.name, self.schema, self.data, self.details)

    def __repr__(self):
        return validation_pattern % (self.error.name, self.schema, self.data, self.details)


class SchemaError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Schema error.'

    def __str__(self):
    	return schema_pattern % self.message

    def __unicode__(self):
    	return schema_pattern % self.message

    def __repr__(self):
        return schema_pattern % self.message
