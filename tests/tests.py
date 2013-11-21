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
from aptexport import PackageListApt

import unittest
import tempfile
import shutil
import subprocess


class BaseTests(unittest.TestCase):
    """basic test class"""
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
        """run before every testcase"""
        self.rootdir = tempfile.mkdtemp(prefix='aptexport-tests_')
        self.__setup_apt_directory_tree()
        self.pla = PackageListApt(rootdir=self.rootdir, cache_update=True)

    def tearDown(self):
        """run after every testcase"""
        if self.rootdir:
            if self.rootdir.startswith("/tmp"):
                shutil.rmtree(self.rootdir)
            else:
                sys.stdout.write(
                    "don't delete temp dir '%s' for safety" % (self.rootdir))


class PackageTests(BaseTests):
    def test_package_keys(self):
        """test that the requested keys are available for every package"""
        for p in self.pla.package_list_apt(False):
            expected_keys = set(["name", "uri", "version", "summary", "sha256",
                                 "provider", "architecture"])
            available_keys = set(p.keys())
            self.assertEqual(
                len(available_keys.symmetric_difference(expected_keys)), 0)


class PackageListTests(BaseTests):
    def test_package_dummies_in_all(self):
        """test that the 2 package dummies are available in all package list"""
        name_list_all = map(lambda x: x["name"],
                            self.pla.package_list_apt(False))
        self.assertIn("aptexport-unittest-dummy1-bin1", name_list_all)
        self.assertIn("aptexport-unittest-dummy1-bin2", name_list_all)

    def test_package_dummies_in_installed(self):
        """test that the 2 package dummies are not available in installed
        package list"""
        name_list_installed = map(lambda x: x["name"],
                                  self.pla.package_list_apt(True))
        self.assertNotIn("aptexport-unittest-dummy1-bin1", name_list_installed)
        self.assertNotIn("aptexport-unittest-dummy1-bin2", name_list_installed)


class ToolsTests(unittest.TestCase):

    def setUp(self):
        tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "../tools")
        self.aptcacheexport_path = os.path.join(tools_dir, "aptcacheexport")
        if not os.path.exists(self.aptcacheexport_path):
            raise Exception("'%s' not found" % self.aptcacheexport_path)

    def test_aptcacheexport_help(self):
        """just run the help and check return value to be sure that there's no
        syntax error"""
        #if return code is != 0, check_output raises a CalledProcessError
        subprocess.check_output([self.aptcacheexport_path, "-h"])
        #now check with an invalid parameter and expect an exception
        self.assertRaises(subprocess.CalledProcessError,
                          subprocess.check_output,
                          (self.aptcacheexport_path,
                           "--invalid-parameter-foo-bar"))
