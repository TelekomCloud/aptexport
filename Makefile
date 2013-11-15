#!/usr/bin/make

all: pep8

pep8:
	/usr/bin/pep8 `find . -path ./build -prune -o -name '*.py' -print` tools/aptcacheexport
