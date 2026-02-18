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
    package_data={'rolca.core': ['locale/sl/LC_MESSAGES/django.*',],},
    package_dir={'': 'src'},
    python_requires='>=3.12, <3.15',
    install_requires=[
        'boto3~=1.42.50',
        'channels~=4.3.2',
        'channels_redis~=4.3.0',
        'Django~=6.0.2',
        'djangorestframework~=3.16.1',
        'django-filter~=25.2',
        'Pillow~=12.1.1',
        'psycopg2-binary~=2.9.11',
    ],
    extras_require={
        'docs': ['sphinx>=8.2.3', 'sphinx_rtd_theme>=3.0.2',],
        'package': ['twine', 'wheel',],
        'test': [
            'black',
            'check-manifest',
            'docutils',
            'flake8~=7.3.0',
            'isort~=5.13.2',
            'mock>=1.3.0',
            'pydocstyle~=6.3.0',
            'pytest-cov>=7.0.0',
            'pytest-django>=4.12.0',
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
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
