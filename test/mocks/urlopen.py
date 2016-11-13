from test.helpers import path
import json

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


class MockUrlOpen(object):
    class MockData(object):
        class MockString(object):
            def __init__(self, data):
                self.data = data

            def decode(self, format):
                return self.data.read()

        def __init__(self, data):
            self.data = data

        def read(self):
            return self.MockString(self.data)

    def __init__(self, components):
        self._components = list(components)

    def urlopen(self, url):
        components = self._components + urlparse(url).path.split('/')
        return self.MockData(open(path(components)))
