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

import apt
#import apt_pkg
import json


class AptCacheExport(object):
    """handle the availalbe/installed software packages"""
    def __init__(self, cache_update=False):
        self.__cache_update = cache_update
        self.__cache = apt.Cache(rootdir="/", memonly=False)
        #update the apt-cache before using it? Need to be root todo this
        if self.__cache_update:
            self.cache.update()
        self.__cache.open()

    def _package_version_origins_dict(self, obj):
        """convert a list of origins to a dict"""
        if isinstance(obj, list):
            l = list()
            for o in obj:
                d = dict()
                if hasattr(o, 'archive'):
                    d['archive'] = o.archive
                if hasattr(o, 'codename'):
                    d['codename'] = o.codename
                if hasattr(o, 'component'):
                    d['component'] = o.component
                if hasattr(o, 'label'):
                    d['label'] = o.label
                if hasattr(o, 'origin'):
                    d['origin'] = o.origin
                if hasattr(o, 'site'):
                    d['site'] = o.site
                if hasattr(o, 'trusted'):
                    d['trusted'] = o.trusted
                l.append(d)
            return l
        #we can not handle this object type with the encoder
        raise Exception(
            "Can not encode '%s'. Not a 'list' object with origins" %
            (type(obj)))

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
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.Version' object" %
            (type(obj)))

    def _package_version_list_list(self, obj):
        """convert a apt.package.VersionList to a list of dicts"""
        if isinstance(obj, apt.package.VersionList):
            return [self._package_version_dict(v) for v in obj]
        #we can not handle this object type with the encoder
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.VersionList' object" %
            (type(obj)))

    def _package_dict(self, obj):
        """convert a apt.package.Package object to a dict"""
        if isinstance(obj, apt.package.Package):
            package = dict()
            package['fullname'] = obj.fullname
            package['name'] = obj.name
            package['shortname'] = obj.shortname
            if hasattr(obj, "has_config_files"):
                package['has_config_files'] = obj.has_config_files
            package['is_installed'] = obj.is_installed
            package['is_upgradable'] = obj.is_upgradable
            if obj.installed:
                package['installed'] = self._package_version_dict(
                    obj.installed)
            #package['installed_files'] = obj.installed_files
            package['versions'] = self._package_version_list_list(obj.versions)
            if obj.candidate:
                package['candiate'] = self._package_version_dict(obj.candidate)
            return package
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.Package' object" %
            (type(obj)))

    def _get_packages(self, only_installed):
        """iterate over the packages"""
        for pkg in self.__cache:
            if only_installed and not pkg.is_installed:
                continue
            yield self._package_dict(pkg)

    def as_json(self, out, only_installed, pretty):
        """write to a file-like object"""
        out.write('[\n')
        if pretty:
            out.write(",".join(map(lambda x: json.dumps(x, indent=2),
                                   self._get_packages(
                                       only_installed=only_installed))))
        else:
            out.write(",".join(map(lambda x: json.dumps(x),
                                   self._get_packages(
                                       only_installed=only_installed))))
        out.write(']\n')
