#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='energy-meter-mercury206',
    version='0.1.0',
    description='Get readings from energy meter Mercury 206 with Python over serial interface',
    long_description=readme + '\n\n' + history,
    author='Sergey Panfilov',
    author_email='sergray@gmail.com',
    url='https://github.com/sergray/energy-meter-mercury206',
    packages=[
        'mercury206',
    ],
    entry_points={
        'console_scripts': [
            'mercury206_config = mercury206.scripts:sample_config',
            'mercury206_readings = mercury206.scripts:display_readings',
            'mercury206_vcp = mercury206.scripts:instant_vcp',
        ]
    },
    package_dir={'mercury206': 'mercury206'},
    include_package_data=True,
    install_requires=[
        'minimalmodbus',
        'pyserial',
    ],
    license="BSD",
    zip_safe=False,
    keywords='energy-meter-mercury206',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)