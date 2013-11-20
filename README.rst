aptexport python module
=======================
.. image:: https://travis-ci.org/TelekomCloud/aptexport.png
   :target: https://travis-ci.org/TelekomCloud/aptexport

aptexport is a python modules based on `python-apt` to collect packages and export the package list. Currently only json is supported.

Installation
============
`python-apt` from http://packages.debian.org/source/sid/python-apt is needed. This module is only useful on Debian based systems.

Usage
=====
There's a command line tool called `aptcacheexport`. To see a installed packages in json format, do::

  ./aptcacheexport --only-installed --pretty

Tests
=====
To execute the whole testsuite (including pep8 and flake8), do::

  make

To run a single testcase (in this example case `test_aptexport_dummy_package` from class `JsonExportTests`) with nose, do::

  nosetests -s tests/tests.py:JsonExportTests.test_aptexport_dummy_package

There's also a testserver under the `tests/` directory. To use the testserver, do::

  ./tests/testserver &
  ./tools/aptcacheexport -p -i -s http://127.0.0.1:8000/

The testserver has a timeout and stops automatically. If the server gets a POST request, the data from that request is loaded by json.
