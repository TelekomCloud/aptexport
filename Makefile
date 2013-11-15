#!/usr/bin/make

all: pep8 flake8 tests

FILE_LIST:=$(shell find . -path ./build -prune -o -name '*.py' -print) tools/aptcacheexport

pep8:
	pep8 $(FILE_LIST)

flake8:
	flake8 $(FILE_LIST)

tests:
	nosetests

.PHONY : pep8 flake8 tests
