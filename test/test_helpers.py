import sys, unittest
from jsonschemaplus.helpers import (email, hostname, ipv4, ipv6, rfc3339, uri, array, boolean, integer,
    null, number, object_, string, valid, maximum, minimum, max_items, min_items,
    max_length, min_length, max_properties, min_properties, multiple_of, enum, unique)


class TestErrors(unittest.TestCase):
    def test_email(self):
        self.assertTrue(email('test@example.com'))
        self.assertFalse(email('randomstring'))

    def test_hostname(self):
        # build string with length > 253 and ends in a '.'
        h = ''
        for i in range(256):
            h += str(chr(i%128))
        h += '.'

        self.assertFalse(hostname(h))

        # build a string of integers > 253
        h = ''
        for i in range(256):
            h += str(i%10)

        self.assertFalse(hostname(h))

        h = 'valid.hostname'
        self.assertTrue(hostname(h))

    def test_ipv4(self):
        self.assertTrue(ipv4('10.0.1.1'))
        self.assertFalse(ipv4('10.1'))

    def test_ipv6(self):
        self.assertTrue(ipv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334'))
        self.assertFalse(ipv6('2001:0db8:85a3:0000:0000:8a2e:0370'))

    def test_rfc3339(self):
        self.assertTrue(rfc3339('1985-04-12T23:20:50.52Z'))
        self.assertFalse(rfc3339('18:50:0'))

    def test_uri(self):
        self.assertTrue(uri('abc://username:password@example.com:123/path/data?key=value&key2=value2#fragid1'))
        self.assertFalse(uri('username:password@example.com:123/path/'))

    def test_array(self):
        self.assertTrue(array([1, 2, 3, 4]))
        self.assertFalse(array('array'))

    def test_boolean(self):
        self.assertTrue(boolean(False))
        self.assertFalse(boolean('True'))

    def test_integer(self):
        self.assertTrue(integer(4))
        self.assertTrue(integer(98249283749234923498293171823948729348710298301928331))
        self.assertFalse(integer('1'))

    def test_null(self):
        self.assertTrue(null(None))
        self.assertFalse(null('null'))

    def test_number(self):
        self.assertTrue(number(123.91))
        self.assertFalse(number('123.91'))

    def test_object(self):
        self.assertTrue(object_({'a': 1, 'b': 2}))
        self.assertFalse(object_('array'))

    def test_string(self):
        self.assertTrue(string('randomstring'))
        self.assertFalse(string(1234))

    def test_valid(self):
        self.assertTrue(valid(['a', 'b']))
        self.assertFalse(valid(object()))

    def test_maximum(self):
        self.assertTrue(maximum(10, 100, False))
        self.assertTrue(maximum('10', 2, True))
        self.assertFalse(maximum(100, 100, True))
        self.assertFalse(maximum(101, 100, True))

    def test_minimum(self):
        self.assertTrue(minimum(101, 100, False))
        self.assertTrue(minimum('2', 10, True))
        self.assertFalse(minimum(100, 100, True))
        self.assertFalse(minimum(99, 100, True))

    def test_max_items(self):
        self.assertTrue(max_items([1, 2, 3, 4, 5, 6], 10))
        self.assertFalse(max_items([1, 2, 3, 4, 5, 6], 3))
        self.assertTrue(max_items('array', 1))

    def test_min_items(self):
        self.assertTrue(min_items([1, 2, 3, 4, 5, 6], 5))
        self.assertFalse(min_items([1, 2, 3, 4, 5, 6], 20))
        self.assertTrue(min_items('array', 10))

    def test_max_length(self):
        self.assertTrue(max_length('aaaaa', 10))
        self.assertFalse(max_length('aaaa', 3))
        self.assertTrue(max_length(23, 10))

    def test_min_length(self):
        self.assertTrue(min_length('asdfqwer', 5))
        self.assertFalse(min_length('zxcv', 20))
        self.assertTrue(min_length({'a': 2}, 10))

    def test_max_properties(self):
        self.assertTrue(max_properties({'a': 2}, 5))
        self.assertFalse(max_properties({'a': 2, 'b': 3, 'c': 4}, 2))
        self.assertTrue(max_properties('qwer', 3))

    def test_min_properties(self):
        self.assertTrue(min_properties({'a': 2, 'b': 3, 'c': 4}, 2))
        self.assertFalse(min_properties({'a': 2, 'b': 3, 'c': 4}, 20))
        self.assertTrue(min_properties([1, 2, 3, 4], 10))

    def test_multiple_of(self):
        self.assertTrue(multiple_of(8, 2))
        self.assertFalse(multiple_of(5, 20))
        self.assertTrue(multiple_of('15', 10))

    def test_enum(self):
        self.assertTrue(enum(3, [1, 2, 3, 4]))
        self.assertFalse(enum(20, [1, 2, 3, 4]))

    def test_unique(self):
        self.assertTrue(unique([1, 2, 3, 4]))
        self.assertFalse(unique([1, 2, 3, 4, 3]))


if __name__ == '__main__':
	unittest.main()