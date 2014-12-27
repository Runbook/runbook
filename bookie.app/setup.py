#!/usr/bin/env python

PROJECT = 'bookie'

VERSION = '0.0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Runbook scaffold generator',
    long_description=long_description,

    author='Reda NOUSHI',
    author_email='reda_noushi@yahoo.com',

    url='https://github.com/noushi/bookie',
    download_url='https://github.com/noushi/bookie/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: GNU Affero GPL 3',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'bookie = bookie.main:main'
        ],
        'bookie': [
            'simple = bookie.simple:Simple',
            'reaction = bookie.reaction:Reaction',
        ],
    },

    zip_safe=False,
)
