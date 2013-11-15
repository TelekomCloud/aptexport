#!/usr/bin/make

all: pep8 flake8

FILE_LIST:=$(shell find . -path ./build -prune -o -name '*.py' -print) tools/aptcacheexport

pep8:
	/usr/bin/pep8 $(FILE_LIST)

flake8:
	/usr/bin/flake8 $(FILE_LIST)
