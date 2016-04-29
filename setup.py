#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

from setuptools import setup
from codecs import open  # Use codecs' open for a consistent encoding


about = __import__('rolca_core.__about__')


# Automate publishing to pypi
if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(about.__version__))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('rolca_core.egg-info')
    sys.exit()


# Get the long description from the README file
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=about.__title__,

    version=about.__version__,

    description=about.__summary__,
    long_description=long_description,

    url=about.__url__,

    author=about.__author__,
    author_email=about.__email__,

    license=about.__license__,

    packages=['rolca_core'],

    include_package_data=True,  # use MANIFEST.in

    install_requires=[
        'Django>=1.9,<1.10a1',
        'djangorestframework>=3.0',
        'Pillow>=3.0.0',
        'psycopg2>=2.5.0',
    ],
    extras_require={
        'docs': [
            'sphinx'
        ],
        'test': [
            'check-manifest',
            'mock',
            'readme'
        ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    test_suite="test_project.runtests.runtests",
)
