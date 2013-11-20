# -*- coding: utf-8 -*-
# Copyright 2013 Thomas Bechtold <thomasbechtold@jpberlin.de>
# Copyright 2013 Deutsche Telekom AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
import tempfile
import shutil


class JsonExportTests(unittest.TestCase):
    def __setup_apt_directory_tree(self):
        """setup directory structure for apt"""
        os.makedirs(os.path.abspath(self.rootdir + "/etc/apt"))
        #create sources.list
        repository_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "repository")
        with open(os.path.abspath(self.rootdir + "/etc/apt/sources.list"),
                  "w") as s:
            s.write("""
deb [arch=amd64] file://%(repo_path)s codename1 main
deb [arch=amd64] file://%(repo_path)s codename2 component1 component2
#deb-src file://%(repo_path)s codename1 main component1 component2
#deb-src file://%(repo_path)s codename2
            """ % {'repo_path': repository_path})
        #create empty apt.conf
        os.makedirs(os.path.abspath(self.rootdir + "/etc/apt/apt.conf.d"))
        with open(os.path.abspath(self.rootdir + "/etc/apt/apt.conf"),
                  "w") as s:
            s.write("")

    def setUp(self):
        self.rootdir = tempfile.mkdtemp(prefix='aptexport-tests_')
        self.__setup_apt_directory_tree()
        self.ace = AptCacheExport(rootdir=self.rootdir, cache_update=True)
        #stringIO used to write json
        self.f = StringIO.StringIO()

    def tearDown(self):
        if self.rootdir:
            if self.rootdir.startswith("/tmp"):
                shutil.rmtree(self.rootdir)
            else:
                sys.stdout.write(
                    "don't delete temp dir '%s' for safety" % (self.rootdir))
        self.f.close()

    def test_export_import(self):
        """write json to file and reread the file and load into json"""
        #first dump the cache as json to file
        self.ace.as_json(self.f, False, True)
        #now load json output from file
        self.f.seek(0)
        json.loads("".join(self.f.readlines()))

    def test_only_installed_packages(self):
        """test expects that the testpackages
        'aptexport-unittest-dummy1-bin1' and
        'aptexport-unittest-dummy1-bin2' are not installed"""
        #check only installed packages
        self.ace.as_json(self.f, True, True)
        self.f.seek(0)
        jsondata = json.loads("".join(self.f.readlines()))
        #expect 0 packages installed!
        self.assertEqual(len(jsondata), 0)

    def test_all_packages(self):
        """test if packages from repositories are listed"""
        #check all packages (not only installed)
        self.ace.as_json(self.f, False, True)
        self.f.seek(0)
        jsondata = json.loads("".join(self.f.readlines()))
        #expect 2 packages available
        self.assertEqual(len(jsondata), 2,
                         "2 packages expected in the test repository")

    def test_aptexport_dummy_package(self):
        """test a single package and the available fields"""
        #check all packages (not only installed)
        self.ace.as_json(self.f, False, True)
        self.f.seek(0)
        jsondata = json.loads("\n".join(self.f.readlines()))
        #first package should be 'aptexport-unittest-dummy1-bin1:amd64'
        p = jsondata[0]
        self.assertEqual(p['fullname'], 'aptexport-unittest-dummy1-bin1:amd64')
        self.assertEqual(p['installed'], None)
        #not all versions of python-apt have this key
        if hasattr(p, "has_config_files"):
            self.assertEqual(p['has_config_files'], False)
        #expected 2 versions for this package
        self.assertEqual(len(p['versions']), 2)
        self.assertEqual(p['versions'][0]['version'], '0.2-1')
        self.assertEqual(p['versions'][1]['version'], '0.1-1')
        #check some fields of one of the versions
        self.assertIsNot(p['versions'][0]['sha256'], None or "")
        #installation candidate
        self.assertFalse(p['candidate'] is None)
        self.assertEqual(p['candidate']['version'], '0.2-1')
