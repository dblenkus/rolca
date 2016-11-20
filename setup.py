#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open  # Use codecs' open for a consistent encoding
from os import path
from setuptools import find_packages, setup

base_dir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get package metadata from 'rolca.__about__.py' file
about = {}
with open(path.join(base_dir, 'rolca', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],

    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,

    url=about['__url__'],

    author=about['__author__'],
    author_email=about['__email__'],

    license=about['__license__'],

    # exclude tests from built/installed package
    packages=find_packages(exclude=['test_project', 'tests.*', '*.tests', '*.tests.*']),
    package_data={
        'rolca.core': [
            'static/rolca_core/*',
            'static/rolca_core/css/*',
            'static/uploader/*',
            'static/uploader/css/*',
            'templates/*.html',
            'templates/uploader/*.html',
        ]
    },

    install_requires=[
        'Django>=1.10,<1.11a1',
        'djangorestframework>=3.4.0',
        'Pillow>=3.0.0',
        'psycopg2>=2.5.0',
    ],
    extras_require={
        'docs': [
            'sphinx>=1.3.2',
            'sphinx_rtd_theme',
        ],
        'package': [
            'twine',
            'wheel',
        ],
        'test': [
            'check-manifest',
            'coverage>=4.2',
            'mock>=1.3.0',
            'pycodestyle>=2.1.0',
            'pydocstyle>=1.0.0',
            'pylint>=1.6.4',
            'readme_renderer'
        ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
