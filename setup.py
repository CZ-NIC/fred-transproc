#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Installation fred transproc.
"""
# Start block --fred-distutils-dir
# add path for freddist if is required and set as argument
import re
import os
import sys

setup = None
try:
    from freddist.core import setup
except ImportError:
    # path to freddist module (use if freddist is not installed)
    explicit_dir_name = None
    pythonpath = os.environ.get("PYTHONPATH", "")
    for argv in sys.argv:
        match = re.match("--fred-distutils-dir=(\S+)", argv)
        if match:
            explicit_dir_name = True
            distpath = match.group(1)
            if distpath not in pythonpath:
                os.environ["PYTHONPATH"] = os.path.pathsep.join(
                                                        (pythonpath, distpath))
            if distpath not in sys.path:
                sys.path.insert(0, distpath)
            break
    if not explicit_dir_name:
        distpath = os.path.dirname(__file__)
        if distpath:
            if distpath not in pythonpath:
                os.environ["PYTHONPATH"] = os.path.pathsep.join(
                                                        (pythonpath, distpath))
            if distpath not in sys.path:
                sys.path.insert(0, distpath)
# End of block --fred-distutils-dir

if setup is None:
    try:
        from freddist.core import setup
    except ImportError, msg:
        print >> sys.stderr, 'ImportError:', msg
        raise SystemExit, 'You required fred-distutils package or define path '\
        'with option --fred-distutils-dir=PATH'


PACKAGE_VERSION = '1.0.0'
PROJECT_NAME = 'fred-transproc'
PACKAGE_NAME = 'fred_transproc'


def main():
    "Run freddist setup"
    setup(
        # Distribution meta-data
        name = PROJECT_NAME,
        author = 'Jan Kryl',
        author_email = 'developers@nic.cz',
        url = 'http://fred.nic.cz/',
        version = PACKAGE_VERSION,
        license = 'GNU GPL',
        platforms = ['posix'],
        description = 'FRED TransProc',
        long_description = 'Component of FRED (Fast Registry for Enum and '
                           'Domains)',
    
        scripts = ['transproc'], 
        packages = [PACKAGE_NAME], 
        package_dir = {PACKAGE_NAME: '.'}, 
        data_files = (
            ('APPCONFDIR', ['transproc.conf']), 
            ('DOCDIR', ['backend.xml', 'example_csob.xml', 'example_ebanka.csv',
                         'example_raiffeisenbank.txt', 'ChangeLog', 'README']),
        )
    )

if __name__ == '__main__':
    main()
