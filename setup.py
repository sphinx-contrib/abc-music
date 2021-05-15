#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
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
# -----------------------------------------------------------------------------
from setuptools import find_namespace_packages, setup


setup(
    name='abc-sphinx-extensions',
    version=0.1,
    license='GPL',
    # license_file='LICENCE',
    description='Sphinx extensions for creating tunebooks with abcfiles',
    # long_description=open('README.rst', 'r').read(),
    install_requires=[
        'sphinx>=2.1',
    ],
    packages=find_namespace_packages(include=['abc_sphinx.*'])
)
