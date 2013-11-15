# -*- coding: utf-8 -*-
#
# Copyright 2013 Thomas Bechtold <thomasbechtold@jpberlin.de>
# Copyright 2013 Thomas Bechtold <t.bechtold@telekom.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import os
import sys
#use aptexport module from local dir
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from aptexport import AptCacheExport

import unittest
import json
import StringIO


class JsonExportTests(unittest.TestCase):
    def test_json_export(self):
        """write json to file and reread the file and load into json"""
        #first dump the cache as json to file
        ace = AptCacheExport()
        f = StringIO.StringIO()
        ace.as_json(f, True, True)
        #now load json output from file
        f.seek(0)
        with open('/tmp/json-test', "w") as x:
            x.write("".join(f.readlines()))
        f.seek(0)
        json.loads("".join(f.readlines()))
        f.close()
        return
