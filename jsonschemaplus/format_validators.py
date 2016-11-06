import re
from rfc3986 import is_valid_uri
from rfc3987 import get_compiled_pattern
from strict_rfc3339 import validate_rfc3339
from validate_email import validate_email


ipv4_regex = get_compiled_pattern('^%(IPv4address)s$')
ipv6_regex = get_compiled_pattern('^%(IPv6address)s$')
hostname_regex = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)


rfc3339 = validate_rfc3339


email = validate_email


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