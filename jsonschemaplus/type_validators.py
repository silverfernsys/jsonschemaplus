def integer(value):
	return (type(value) == int or type(value) == long)


def array(value):
	return type(value) == list


def boolean(value):
	return type(value) == bool


def null(value):
	return value == None


def number(value):
	return (type(value) == float or integer(value))


def object_(value):
	return type(value) == dict


def string(value):
	return (type(value) == str or type(value) == unicode)


def valid(value):
	return (integer(value) or array(value) or
		boolean(value) or null(value) or number(value) or
		object_(value) or string(value))
