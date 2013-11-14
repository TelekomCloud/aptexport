aptexport python module
=======================
aptexport is a python modules based on `python-apt` to collect packages and export the package list. Currently only json is supported.

Installation
============
`python-apt` from http://packages.debian.org/source/sid/python-apt is needed. This module is only useful on Debian based systems.

Usage
=====
There's a command line tool called `aptcacheexport`. To see a installed packages in json format, do::

  ./aptcacheexport --only-installed --pretty
