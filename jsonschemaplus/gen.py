from collections import Iterable


class ParserIterator(Iterable):
    def __init__(self, iterator, lookahead=None):
        self._iterator = self._flatten(iterator)
        self._lookahead = lookahead

    def __iter__(self):
        return self

    def lookahead(self):
        try:
            self._lookahead = self.next()
            return self._lookahead
        except StopIteration:
            return None

    def __next__(self):
        return self.next()

    def next(self):
        if self._lookahead != None:
            value, self._lookahead = self._lookahead, None
            return value
        else:
            try:
                return next(self._iterator)
            except StopIteration as e:
                raise e

    def _flatten(self, it):
        for i in it:
            if (isinstance(i, Iterable) and
                not isinstance(i, str)):
                for y in self._flatten(i):
                    yield y
            else:
                yield i
