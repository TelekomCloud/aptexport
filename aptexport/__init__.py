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

import apt
import hashlib

class Package(object):
    def __init__(self, pkg):
        #handle only packages of type 'apt.package.Package'
        if not isinstance(pkg, apt.package.Package):
            raise Exception("pkg type not 'apt.package.Package'")
        self.__pkg = pkg
        #get the version to get information from
        if hasattr(self.__pkg, "installed") and self.__pkg.installed:
            self.__pkg_version = pkg.installed
        elif hasattr(self.__pkg, "candidate") and self.__pkg.candidate:
            self.__pkg_version = pkg.candidate
        elif hasattr(self.__pkg, "versions") and self.__pkg.versions and \
                len(self.__pkg.versions) > 0:
            self.__pkg_version = self.__pkg.versions[0]
        else:
            raise Exception("Can not get a version for pkg '{0}'".format(
                pkg.fullname))

    def __repr__(self):
        return "<%(name)s, %(version)s>" % self.as_dict()

    def as_dict(self):
        """get package information as dict"""
        p = dict()
        p["name"] = self.__pkg.name
        p["uri"] = self.__pkg_version.uri
        p["version"] = self.__pkg_version.version
        p["summary"] = self.__pkg_version.summary
        p["sha256"] = self.__pkg_version.sha256
        # fake a checksum value, since we can't find a real one
        if p["sha256"] is None:
            p["sha256"] = hashlib.sha256( p["name"] + "-" + p["version"] ).hexdigest()
        p["provider"] = "apt"
        p["architecture"] = self.__pkg_version.architecture
        return p


class PackageListApt(object):
    """create list with all/only installed deb packages"""
    def __init__(self, rootdir="/", cache_update=False):
        self.__cache_update = cache_update
        self.__cache = apt.Cache(rootdir=rootdir, memonly=False)
        #update the apt-cache before using it? Need to be root todo this
        if cache_update:
            self.__cache.update()
        self.__cache.open()

    def package_list_apt(self, only_installed):
        """iterate over the packages"""
        for pkg in self.__cache:
            if only_installed and not pkg.is_installed:
                continue
            yield (Package(pkg).as_dict())
