class ValidationError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Validation error.'

    def __str__(self):
    	return '<ValidationError(message={self.message})>'.format(self=self)

    def __unicode__(self):
    	return '<ValidationError(message={self.message})>'.format(self=self)

    def __repr__(self):
        return '<ValidationError(message={self.message})>'.format(self=self)


class SchemaError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Schema error.'

    def __str__(self):
    	return '<SchemaError(message={self.message})>'.format(self=self)

    def __unicode__(self):
    	return '<SchemaError(message={self.message})>'.format(self=self)

    def __repr__(self):
        return '<SchemaError(message={self.message})>'.format(self=self)