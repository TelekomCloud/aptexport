# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.rst"), "r") as f:
    long_desc = "".join(f.readlines())

setup(
    name="aptexport",
    version="0.1",
    packages=find_packages(),
    scripts=['tools/aptcacheexport'],
    package_data={
        '': ['README.rst', 'LICENSE'],
    },
    install_requires=[
        'python-apt',
        'setuptools',
    ],
    author="Thomas Bechtold",
    author_email="thomasbechtold@jpberlin.de",
    description="export apt package catalog",
    long_description=long_desc,
    license="GPL-3",
    keywords="apt dpkg debian ubuntu",
    url="https://github.com/toabctl/aptexport",

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
)
