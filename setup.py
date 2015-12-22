#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from setuptools import setup


version = __import__('rolca_core').VERSION

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
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('rolca_core.egg-info')
    sys.exit()

setup(
    name='rolca-core',
    version=version,
    url='https://github.com/dblenkus/rolca-core',
    author='Domen Blenkuš',
    author_email='domen@blenkus.com',
    description='Open source platform for organising photography salons.',
    long_description=open('README.rst', 'r').read(),
    license='Apache License (2.0)',
    packages=['rolca_core'],
    include_package_data=True,  # use MANIFEST.in
    install_requires=[
        'Django>=1.9,<1.10a1',
        'djangorestframework>=3.0',
        'Pillow>=3.0.0',
        'psycopg2>=2.5.0',
    ],
    extras_require={
        'docs':  ['sphinx'],
        'test': ['check-manifest', 'mock', 'readme'],
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
