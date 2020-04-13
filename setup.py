#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from os.path import dirname
from os.path import join

from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


project_name = 'track-analyzer'
module_name = project_name
regex_found_badges = re.compile('^.. start-badges.*^.. end-badges', re.M | re.S)
dependencies = [
    'pandas==0.25.2',
    'matplotlib==3.1.1',
    'geopy==1.20.0',
    'networkx==2.4',
    'numpy==1.17.3',
    'shapely==1.7.0',
    'pymongo==3.10.1',
    'gpxpy==1.3.5',
    'osmnx==0.10',
    'seaborn==0.9.0'
]

setup(
    name=module_name,
    version='0.1.0-SNAPSHOT',
    author='Antonio Boutaour',
    author_email='tboutaour@gmail.com',
    long_description='TrackAnalizer: TFG',
    url='',
    python_requires='>=3.7',
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages('src', exclude=['tests', 'tests.*']),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS',
    ],
    tests_require=["nose"] + dependencies,
    install_requires=dependencies
)
