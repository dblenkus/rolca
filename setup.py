from os import path
import setuptools

# Get long description from README.
with open('README.rst') as fh:
    long_description = fh.read()

# Get package metadata from 'rolca.__about__.py' file.
base_dir = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(base_dir, 'src', 'rolca', '__about__.py')) as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about['__title__'],
    use_scm_version=True,
    description=about['__summary__'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    # Exclude tests from built/installed package.
    packages=setuptools.find_packages(
        'src', exclude=['tests', 'tests.*', '*.tests', '*.tests.*']
    ),
    package_data={
        'rolca.core': [
            'locale/sl/LC_MESSAGES/django.*',
        ],
    },
    package_dir={'': 'src'},
    python_requires='>=3.8, <3.12',
    install_requires=[
        'boto3~=1.26.0',
        'channels~=4.0.0',
        'channels_redis~=4.1.0',
        'Django==4.2',
        'djangorestframework~=3.14.0',
        'django-filter~=23.1',
        'Pillow~=9.5.0',
        'psycopg2-binary~=2.9.6',
    ],
    extras_require={
        'docs': [
            'sphinx>=6.2.0',
            'sphinx_rtd_theme',
        ],
        'package': [
            'twine',
            'wheel',
        ],
        'test': [
            'black',
            'check-manifest',
            'docutils',
            'flake8~=6.0.0',
            'isort~=5.12.0',
            'mock>=5.0.2',
            'pydocstyle~=6.3.0',
            'pytest-cov>=4.0.0',
            'pytest-django>=4.5.2',
            'pytest-pythonpath~=0.7.4',
            'readme_renderer',
            'setuptools_scm',
            'twine',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
