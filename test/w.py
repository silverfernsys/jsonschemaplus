import collections

def flatten(it):
    for x in it:
        if (isinstance(x, collections.Iterable) and
            not isinstance(x, str)):
            for y in flatten(x):
                yield y
        else:
            yield x

def a(x):
    for y in x:
        if y % 2 == 0:
            yield 'error'

def b(x):
    yield a(x)

def c(x):
    yield b(x)

def d(x):
    return flatten(c(x))


def main():
    print(list(flatten(c(xrange(10)))))
    print(list(d(xrange(10))))


if __name__ == '__main__':
    main() 