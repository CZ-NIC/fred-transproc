#!/usr/bin/python
# -*- coding: utf-8 -*-
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
