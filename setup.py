#!/usr/bin/env python

from setuptools import setup

description = 'Create json logging output for python' + \
              'nosetests unittest framework',

setup(
    name='nosetests-json-extended-parallel',
    version='1.0',
    author='Rui Li',
    author_email='rui.li.spam@gmail.com',
    description=description,
    url='https://github.com/ruivapps/nosetests-json-extended-parallel',
    download_url='https://github.com/ruivapps/nosetests-json-extended-parallel/tarball/1.0',
    packages=['nosetests_json_extended_parallel'],
    zip_safe=False,
    entry_points={
        'nose.plugins.0.10': [
            'nosetests_json_extended_parallel = ' +
            'nosetests_json_extended_parallel.plugin:JsonExtendedPlugin'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing'
    ],
    long_description=open('README.rst', 'r').read()
)
