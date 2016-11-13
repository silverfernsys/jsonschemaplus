try:
	from response import MockRequestResponse
except:
	from test.mocks.response import MockRequestResponse


try:
	from urlopen import MockUrlOpen
except:
	from test.mocks.urlopen import MockUrlOpen