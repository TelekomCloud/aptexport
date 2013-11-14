# -*- coding: utf-8 -*-
#
# Copyright 2013 Thomas Bechtold <thomasbechtold@jpberlin.de>
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
import argparse
import apt
import apt_pkg
import json


class AptCacheExport(object):
    """handle the availalbe/installed software packages"""
    def __init__(self):
        self.__cache = apt.Cache(rootdir="/", memonly=False)
        #self.cache.update()
        self.__cache.open()

    def _package_version_origins_dict(self, obj):
        """convert a list of origins to a dict"""
        if isinstance(obj, list):
            return [
                {
                    'archive': o.archive,
                    'codename': o.codename,
                    'component': o.component,
                    'label': o.label,
                    'origin': o.origin,
                    'site': o.site,
                    'trusted': o.trusted,
                } for o in obj]
        #we can not handle this object type with the encoder
        raise Exception("Can not encode '%s'. Not a 'list' object with origins" % (type(obj)))

    def _package_version_dict(self, obj):
        """convert a apt.package.Version to a dict"""
        if isinstance(obj, apt.package.Version):
            return {
                'policy_priority': obj.policy_priority,
                'version': obj.version,
                'installed_size': obj.installed_size,
                'uri': obj.uri,
                'sha256': obj.sha256,
                'size': obj.size,
                'installed_size': obj.installed_size,
                'source_name': obj.source_name,
                'source_version': obj.source_version,
                'origins': self._package_version_origins_dict(obj.origins),
                'section': obj.section,
                'architecture': obj.architecture,
                'uris': obj.uris,
                'summary': obj.summary,
                'description': obj.description,
            }
        #we can not handle this object type with the encoder
        raise Exception("Can not encode '%s'. Not a 'apt.package.Version' object" % (type(obj)))

    def _package_version_list_list(self, obj):
        """convert a apt.package.VersionList to a list of dicts"""
        if isinstance(obj, apt.package.VersionList):
            return [self._package_version_dict(v) for v in obj]
        #we can not handle this object type with the encoder
        raise Exception("Can not encode '%s'. Not a 'apt.package.VersionList' object" % (type(obj)))

    def _package_dict(self, obj):
        """convert a apt.package.Package object to a dict"""
        if isinstance(obj, apt.package.Package):
            package = dict()
            package['name'] = obj.name
            package['shortname'] = obj.shortname
            package['has_config_files'] = obj.has_config_files
            package['is_installed'] = obj.is_installed
            package['is_upgradable'] = obj.is_upgradable
            if obj.installed:
                package['installed'] = self._package_version_dict(obj.installed)
            #package['installed_files'] = obj.installed_files
            package['versions'] = self._package_version_list_list(obj.versions)
            if obj.candidate:
                package['candiate'] = self._package_version_dict(obj.candidate)
            return package
        raise Exception("Can not encode '%s'. Not a 'apt.package.Package' object" % (type(obj)))

    def _get_packages(self, only_installed):
        """iterate over the packages"""
        for pkg in self.__cache:
            if only_installed and not pkg.is_installed:
                continue
            yield self._package_dict(pkg)

    def as_json(self, out, only_installed, pretty):
        """write to a file-like object"""
        for package in self._get_packages(only_installed=only_installed):
            if pretty:
                out.write(json.dumps(package, indent=2))
            else:
                out.write(json.dumps(package))
