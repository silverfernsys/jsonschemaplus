#! /usr/bin/python
from jsonschemaplus.validators import Draft4Validator as validator
from jsonschemaplus.errors import ValidationError
from jsonschemaplus.schemas.metaschema import metaschema
from jsonschemaplus.schemas.hyperschema import hyperschema
from os.path import join, dirname, abspath
import json


def path(*args):
    return join(dirname(abspath(__file__)), *args)


def paths(*args):
    return glob.glob(join(dirname(abspath(__file__)), *args))


def validate_type():
    data = json.loads(open(path('data', 'draft4', 'type.json')).read())
    for d in data:
        v = validator(d['schema'])
        for test in d['tests']:
            try:
                v.validate(test['data'])
                assert test['valid'] == True
            except ValidationError as e:
                assert test['valid'] == False


def validate_ref():
    data = json.loads(open(path('data', 'draft4', 'ref.json')).read())
    for d in data:
        v = validator(d['schema'])
        for test in d['tests']:
            try:
                v.validate(test['data'])
                assert test['valid'] == True
            except ValidationError as e:
                assert test['valid'] == False


def resolve_metaschema():
    v = validator(metaschema)


def resolve_hyperschema():
    v = validator(hyperschema)


def main():
    # validate_ref()
    validate_type()
    resolve_metaschema()
    resolve_hyperschema()


if __name__ == '__main__':
    main()
