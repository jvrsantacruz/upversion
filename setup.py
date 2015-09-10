# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
README = open(os.path.join(here, 'README.md')).read()
REQUIREMENTS = open(os.path.join(here, 'requirements.txt')).readlines()

setup(
    name='upversion',
    version='0.0.1',
    description='Release python packages with ease',
    author='Javier Santacruz',
    author_email='jsl@taric.es',
    install_requires=REQUIREMENTS,
    long_description=README,
    py_modules=['upversion'],
    packages=find_packages(),
    classifiers=[
        "Internal :: Do not upload"
    ],
    entry_points="""
    [console_scripts]
    upversion=upversion:cli
    """
)
