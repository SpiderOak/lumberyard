# -*- coding: utf-8 -*-
"""
setup.py

setup file for lumberyard
"""
from distutils.core import setup

_name = "lumberyard"
_description = "HTTP access to $NAME"
_version = "0.1.0"
_author = "Doug Fort"
_author_email = "dougfort@spideroak.com"
_url = "https://spideroak.com"
_packages = ["lumberyard", ]
_classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries",
]
with open("README.txt") as input_file:
    _long_description = input_file.read()

setup(
    name=_name,
    description=_description,
    long_description=_long_description,
    author=_author,
    author_email=_author_email,
    url=_url,
    packages=_packages,
    version=_version,
    classifiers=_classifiers,
)
