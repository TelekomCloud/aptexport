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
#import apt_pkg
import json


class AptCacheExport(object):
    """handle the availalbe/installed software packages"""
    def __init__(self, rootdir="/", cache_update=False):
        self.__cache_update = cache_update
        self.__cache = apt.Cache(rootdir=rootdir, memonly=False)
        #update the apt-cache before using it? Need to be root todo this
        if cache_update:
            self.__cache.update()
        self.__cache.open()

    def _package_version_origins_dict(self, obj):
        """convert a list of origins to a dict"""
        if isinstance(obj, list):
            l = list()
            for o in obj:
                #ignore origin '/var/lib/dpkg/status'
                if hasattr(o, 'archive') and o.archive != "now":
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

    def _package_version_dict_full(self, obj):
        """convert a apt.package.Version to a dict with full information"""
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
                'uri': obj.uri,
                'summary': obj.summary,
                'description': obj.description,
            }
        #we can not handle this object type with the encoder
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.Version' object" %
            (type(obj)))

    def _package_version_dict_minimal(self, obj):
        """convert a apt.package.Version to a dict with minimal information"""
        if isinstance(obj, apt.package.Version):
            return {
                'version': obj.version,
                'sha256': obj.sha256,
            }
        #we can not handle this object type with the encoder
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.Version' object" %
            (type(obj)))

    def _package_version_list_minimal(self, obj):
        """convert a apt.package.VersionList to a list of dicts"""
        if isinstance(obj, apt.package.VersionList):
            return [self._package_version_dict_minimal(v) for v in obj]
        #we can not handle this object type with the encoder
        raise Exception(
            "Can not encode '%s'. Not a 'apt.package.VersionList' object" %
            (type(obj)))

    def _package_dict(self, obj):
        """convert a apt.package.Package object to a dict"""
        if isinstance(obj, apt.package.Package):
            package = dict()
            package['fullname'] = obj.fullname
            #information about currently installed version
            if obj.installed:
                package['installed'] = self._package_version_dict_full(
                    obj.installed)
            else:
                package['installed'] = None
            #other available versions (minimal info)
            package['versions'] = self._package_version_list_minimal(
                obj.versions)
            #possible installation candidate (minimal info)
            if obj.candidate:
                #if there's no installed version, add full
                #description of candidate
                if package['installed']:
                    package['candidate'] = self._package_version_dict_minimal(
                        obj.candidate)
                else:
                    package['candidate'] = self._package_version_dict_full(
                        obj.candidate)
            else:
                package['candidate'] = None
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
