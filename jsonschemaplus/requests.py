try:
    from urllib2 import urlopen
except ImportError:
	from urllib.request import urlopen

import json


def get(url):
	response = urlopen(url)
	data = response.read().decode('utf-8')
	return json.loads(data)
    