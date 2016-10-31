class ValidationError(Exception):
    def __init__(self):
        self.message = 'Validation error.'


class SchemaError(Exception):
    def __init__(self):
        self.message = 'Schema error.'