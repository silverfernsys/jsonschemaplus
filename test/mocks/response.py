from test.helpers import path
import json as json_


try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


class MockRequestResponse(object):
    def __init__(self, components, url=None):
        self._components = list(components)

        if url != None:
            self.json(url)
        else:
            self._data = None
    
    def json(self, url=None):
        if url != None:
            components = self._components + urlparse(url).path.split('/')
            with open(path(components)) as file:
                self._data = json_.loads(file.read())
        return self._data
