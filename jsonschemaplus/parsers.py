try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


def url(value):
	components = urlparse(value)
	url = components.scheme + '://' + components.netloc + components.path
	path = '#' + components.fragment
	return (url, path)