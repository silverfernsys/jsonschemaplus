# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from sys import version_info

import jsonschemaplus

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jsonschemaplus',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=jsonschemaplus.__version__,

    description='JSON Schema validation for Python',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/silverfernsys/jsonschemaplus',

    # Author details
    author='Silver Fern Systems',
    author_email='dev@silverfern.io',

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='validation validator schema json jsonschema',

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['rfc3986', 'rfc3987', 'strict-rfc3339'],

    if version_info < (3, 4):
        install_requires.append('enum34')
        
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    if version_info > (3,):
        test_extras = ['coverage', 'codecov', 'pytest']
    else:
        test_extras = ['coverage', 'codecov', 'mock', 'pytest']

    extras_require={
        'test': test_extras,
        'docs': ['mkdocs'],
        'benchmark': ['jsonschema', 'tabulate', 'termcolor']
    },
)
