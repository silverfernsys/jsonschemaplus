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


def project_name(cls):
    return cls.__module__.split('.')[0]


def fqn(obj):
    return obj.__class__.__module__ + '.' + obj.__class__.__name__


HEADER_COLOR = None
SUCESS_COLOR = 'green'
FAIL_COLOR = 'red'
TBL_FMT = 'simple' # 'plain', 'rst'


def color_text(text, color=None):
        return colored(text, color=color, attrs=['bold'])


def total_time(data, comparison, wrapper):
    time_acc = 0.0
    for d in data:
        validator = comparison[0](d['schema'])
        func = getattr(validator, comparison[1])
        for test in d['tests']:
            wrapped_func = wrapper(func, test['data'])
            time_acc += timeit(wrapped_func, number=1000)
    return time_acc


@mock.patch('jsonschemaplus.resolver.get')
@mock.patch('jsonschema.validators.urlopen')
def run_benchmark(name, paths, comparisons, mock_urlopen, mock_get):
    m = MockRequestResponse((current_dir, '..', 'test', 'data',
        'JSON-Schema-Test-Suite', 'draft4', 'refRemote'))
    mock_get.side_effect = lambda url: m.json(url)

    u = MockUrlOpen((current_dir, '..', 'test', 'data',
        'JSON-Schema-Test-Suite', 'draft4', 'refRemote'))
    mock_urlopen.side_effect = lambda url: u.urlopen(url)

    headers = ['filename', color_text(project_name(comparisons[0][0]))]
    headers.extend([project_name(x[0]) for x in comparisons[1:]])
    results = []
    for path in paths:
        result = [path.split('/')[-1]]
        for comparison in comparisons:
            wrapper = comparison[2]
            with open(path, 'r') as file:
                result.append(total_time(json.loads(file.read()), comparison, wrapper))
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
    tab = tabulate(highlighted_results, headers=headers, tablefmt=TBL_FMT)
    title = color_text(name).center(tab.find('\n'), ' ')
    return title + '\n' + tab


def expand_paths(path_components):
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
    return p


def benchmark(name, file_paths, comparisons):
    return run_benchmark(name, file_paths, comparisons)


def is_valid(path):
    def wrapper(func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped

    return benchmark('is_valid', path, [(jsp_validator, 'is_valid', wrapper),
        (js_validator, 'is_valid', wrapper)])


def errors(path):
    def list_errors_wrapper(func, *args, **kwargs):
        def wrapped():
            return list(func(*args, **kwargs))
        return wrapped

    return benchmark('list validation errors', path, [(jsp_validator, 'errors', list_errors_wrapper),
        (js_validator, 'iter_errors', list_errors_wrapper)])


def main():
    path = expand_paths([
        (current_dir, '..', 'test', 'data', 'JSON-Schema-Test-Suite', 'draft4', 'optional', '*.json'),
        (current_dir, '..', 'test', 'data', 'JSON-Schema-Test-Suite', 'draft4', '*.json'),
        (current_dir, '..', 'test', 'data', 'simple', 'draft4', '*.json'),
        (current_dir, '..', 'test', 'data', 'complex', 'draft4', '*.json'),
    ])
    
    benchmarks = {'is_valid': is_valid, 'errors': errors}
    commands = sys.argv[1:]

    keys = benchmarks.keys()
    unknown_command = False
    for command in commands:
        if command not in keys:
            unknown_command = True
            print('Unknown command: %s' % color_text(command))
    
    if not len(commands) or unknown_command:
        print('Possible commands are %s' % ', '.join([color_text(k) for k in keys]))
        sys.exit(1)

    results = ''
    for index, command in enumerate(commands):
        if index > 0:
            results += '\n'
        results += benchmarks[command](path)

    print(results)


if __name__ == '__main__':
    main()
