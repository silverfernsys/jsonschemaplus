import re
from jsonschemaplus.type_validators import array, number, object_, string


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


# def pattern(value, regex):
# 	r = re.compile(regex)
# 	if string(value):
# 		if r.search(value):
# 			return True
# 		else:
# 			return False
# 	else:
# 		return True
