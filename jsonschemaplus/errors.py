try:
    validation_pattern = unicode('<ValidationError(message=%s)>')
    schema_pattern = unicode('<SchemaError(message=%s)>')
except:
    validation_pattern = '<ValidationError(message=%s)>'
    schema_pattern = '<SchemaError(message=%s)>'    


class ValidationError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Validation error.'

    def __str__(self):
    	return validation_pattern % self.message

    def __unicode__(self):
    	return validation_pattern % self.message

    def __repr__(self):
        return validation_pattern % self.message


class SchemaError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Schema error.'

    def __str__(self):
    	return schema_pattern % self.message

    def __unicode__(self):
    	return schema_pattern % self.message

    def __repr__(self):
        return schema_pattern % self.message
