from jsonschemaplus.validators import Draft4Validator as jsp_validator
from jsonschema import Draft4Validator as js_validator
from test.helpers import path, paths
from test.mocks import MockRequestResponse, MockUrlOpen
from tabulate import tabulate
from termcolor import colored
from os.path import dirname, abspath
from copy import deepcopy
from timeit import timeit
import json
import operator
import sys


if sys.version_info > (3,):
    from functools import reduce


try:
    import mock
except:
    from unittest import mock


current_dir = dirname(abspath(__file__))


def min_index(values):
    index, _ = min(enumerate(values), key=operator.itemgetter(1))
    return index


def max_index(values):
    index, _ = max(enumerate(values), key=operator.itemgetter(1))
    return index


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def project_name(cls):
    return cls.__module__.split('.')[0]


def fqn(obj):
    return obj.__class__.__module__ + '.' + obj.__class__.__name__


HEADER_COLOR = None
SUCESS_COLOR = 'green'
FAIL_COLOR = 'red'
TBL_FMT = 'simple' # 'plain'


def color_text(text, color=None):
        return colored(text, color=color, attrs=['bold'])


@mock.patch('jsonschemaplus.resolver.get')
@mock.patch('jsonschema.validators.urlopen')
def is_valid(paths, comparisons, mock_urlopen, mock_get):
    m = MockRequestResponse((current_dir, '..', 'test', 'data',
        'JSON-Schema-Test-Suite', 'draft4', 'refRemote'))
    mock_get.side_effect = lambda url: m.json(url)

    u = MockUrlOpen((current_dir, '..', 'test', 'data',
        'JSON-Schema-Test-Suite', 'draft4', 'refRemote'))
    mock_urlopen.side_effect = lambda url: u.urlopen(url)

    headers = ['filename', color_text(project_name(comparisons[0][0]))]
    headers.extend([project_name(x[0]) for x in comparisons[1:]])
    headers.append('min_index')
    results = []
    for path in paths:
        result = [path.split('/')[-1]]
        for comparison in comparisons:
            with open(path, 'r') as file:
                time_acc = 0.0
                for data in json.loads(file.read()):
                    validator = comparison[0](data['schema'])
                    func = getattr(validator, comparison[1])
                    for test in data['tests']:
                        wrapped_func = wrapper(func, test['data'])
                        time_acc += timeit(wrapped_func, number=1000)
                result.append(time_acc)
        result.append(min_index(result[1:]))
        results.append(result)

    def sum_with_index(index):
        return lambda x, y: x + y[index]

    total = [color_text('Total')]
    for i in range(len(comparisons)):
        total.append(reduce(sum_with_index(i + 1), results, 0))
    total.append(min_index(total[1:]))
    results.append(total)

    def mapper(item):
        mapped = [item[0]]
        min_item = item[-1]
        for index, x in enumerate(item[1:-1]):
            if index == min_item:
                if index == 0:
                    x_str = color_text(str(x), color='green')
                else:
                    x_str = color_text(str(x), color='red')
            else:
                x_str = str(x)
            mapped.append(x_str)
        return mapped

    highlighted_results = map(mapper, results)

    return tabulate(highlighted_results, headers=headers, tablefmt=TBL_FMT)


def run_benchmark(path_components, benchmark, comparisons):
    if type(path_components) == tuple:
        if path_components[-1].startswith('*.'):
            p = paths(path_components)
        else:
            p = [path(path_components)]
    elif type(path_components) == list:
        p = []
        for c in path_components:
            if c[-1].startswith('*.'):
                p.extend(paths(c))
            else:
                p.append(path(c))
    else:
        raise ValueError('path_components must either be a list or a tuple')

    results = benchmark(p, comparisons)
    print(results)


def main():
    path = [
        (current_dir, '..', 'test', 'data', 'JSON-Schema-Test-Suite', 'draft4', 'optional', '*.json'),
        (current_dir, '..', 'test', 'data', 'JSON-Schema-Test-Suite', 'draft4', '*.json'),
        (current_dir, '..', 'test', 'data', 'simple', 'draft4', '*.json'),
        (current_dir, '..', 'test', 'data', 'complex', 'draft4', '*.json'),
    ]
    run_benchmark(path, is_valid, [(jsp_validator, 'is_valid'), (js_validator, 'is_valid')])


if __name__ == '__main__':
    main()
