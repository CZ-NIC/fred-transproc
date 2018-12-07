#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2018  CZ.NIC, z. s. p. o.
#
# This file is part of FRED.
#
# FRED is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FRED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FRED.  If not, see <https://www.gnu.org/licenses/>.

"""
Installation fred transproc.
"""
from setuptools import setup

PROJECT_NAME = 'fred-transproc'
DATA_FILES = [
    ('libexec/%s' % PROJECT_NAME, ['proc_csob_xml.py', 'proc_ebanka_csv.py', 'proc_fio_xml.py']),
]

setup(name=PROJECT_NAME,
      version='1.5.0',
      author='Jan Kryl',
      author_email='developers@nic.cz',
      url='http://fred.nic.cz/',
      license='GNU GPL',
      platforms=['posix'],
      description='FRED TransProc',
      long_description='Component of FRED (Free Registry for ENUM and Domains)',
      packages=['fred_transproc'],
      scripts=['transproc'],
      data_files=DATA_FILES)
