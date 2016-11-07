import re
import sys
from rfc3986 import is_valid_uri
from rfc3987 import get_compiled_pattern
from strict_rfc3339 import validate_rfc3339


if sys.version_info > (3,):
    long = int
    unicode = str


email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
ipv4_regex = get_compiled_pattern('^%(IPv4address)s$')
ipv6_regex = get_compiled_pattern('^%(IPv6address)s$')
hostname_regex = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)


rfc3339 = validate_rfc3339


# email = validate_email
def email(value):
	if email_regex.match(value):
		return True
	else:
		return False


def ipv4(value):
	return ipv4_regex.match(value) != None


def ipv6(value):
	return ipv6_regex.match(value) != None


def uri(value):
    return is_valid_uri(value, require_authority=True)


def hostname(value):        
    if value[-1] == '.':
        # strip exactly one dot from the right, if present
        value = value[:-1]
    # cannot be longer than 253 characters or all-numeric
    if len(value) > 253 or re.match(r'[\d.]+$', value):
        return False

    return all(hostname_regex.match(v) for v in value.split("."))


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


def unique(array):
	for i in range(len(array) - 1):
		for j in range(i + 1, len(array)):
			if (array[i] == array[j] and
				type(array[i]) == type(array[j])):
				return False
	return True


def enum(value, enums):
	if value in enums:
		return True
	else:
		return False


def maximum(value, other, exclusive=False):
	if number(value):
		if exclusive:
			return value < other
		else:
			return value <= other
	else:
		return True


def minimum(value, other, exclusive=False):
	if number(value):
		if exclusive:
			return value > other
		else:
			return value >= other
	else:
		return True


def max_properties(value, count):
	if object_(value):
		return len(value.keys()) <= count
	else:
		return True


def min_properties(value, count):
	if object_(value):
		return len(value.keys()) >= count
	else:
		return True


def max_length(value, length):
	if string(value):
		return len(value) <= length
	else:
		return True


def min_length(value, length):
	if string(value):
		return len(value) >= length
	else:
		return True


def max_items(value, length):
	if array(value):
		return len(value) <= length
	else:
		return True


def min_items(value, length):
	if array(value):
		return len(value) >= length
	else:
		return True


def multiple_of(value, mod):
	if number(value):
		if mod < 1:
			value = value * (1 / mod)
			mod = 1
		return (value % mod == 0)
	else:
		return True

