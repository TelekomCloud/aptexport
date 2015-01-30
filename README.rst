Mothballed
==========

This project is currently unmaintained. The core developers have moved to other projects. The system works very well and has a solid core.

If the status changes, please update this section.

aptexport python module
=======================
.. image:: https://travis-ci.org/TelekomCloud/aptexport.png?branch=master
   :target: https://travis-ci.org/TelekomCloud/aptexport

aptexport is a python modules based on `python-apt` to collect packages and export the package list. Currently only json is supported.

Installation
============
`python-apt` from http://packages.debian.org/source/sid/python-apt is needed. This module is only useful on Debian based systems.

Usage
=====
There's a command line tool called `aptcacheexport`. To see a installed packages in json format, do::

  ./aptcacheexport --only-installed --pretty

Exported format
===============
The exported format looks like::

   {
     "node":     "<nodename>",
     "packages": [
     {
     "name":         "<packagename>",
     "uri":          "<uri>",
     "version":      "<version>",
     "summary":      "<summary>",
     "sha256":       "<sha256>",
     "provider":     "[apt|pip|gem|...]",
     "architecture": "<i386|amd64>",
     ]
     }
   }

Here's an example of the exported format::

  {
    "node": "localhost.localdomain",
    "packages": [
    {
      "name": "accountsservice",
      "uri": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.15-2ubuntu9_amd64.deb",
      "summary": "query and manipulate user account information",
      "version": "0.6.15-2ubuntu9",
      "architecture": "amd64",
      "sha256": "5d8e40ce35ea30f621573d40b17dcd21e3b974f2dd5e096c6c10701af8cdc5d0",
      "provider": "apt",
      },
      ...
      ]
  }

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
