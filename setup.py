# -*- coding: utf-8 -*-

from os import path, getcwd
from setuptools import setup, find_packages

CWD = getcwd()
README_PATH = path.join(CWD, 'README.rst')
LICENSE_PATH = path.join(CWD, 'LICENSE')

try:
    f = open(README_PATH, 'r')
    readme = f.read()
except IOError:
    readme = ''

try:
    f = open(LICENSE_PATH, 'r')
    readme = f.read()
except IOError:
    license = 'ISC'


setup(
    name='gg',
    version='0.0.0',
    description='',
    long_description=readme,
    author='Alejandro Gómez',
    author_email='alejandroogomez@gmail.com',
    url='https://github.com/alejandrogomez/gg',
    entry_points={
        'console_scripts': [
            'gg = gg.cli:main',
    ],},
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

