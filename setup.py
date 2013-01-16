#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Installation fred transproc.
"""
import re

from freddist.command.install import install
from freddist.core import setup


PROJECT_NAME = 'fred-transproc'


class TransprocInstall(install):
    user_options = install.user_options + [
        ('backendcmd=', None, 'Command for backend CLI admin tool.'),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.backendcmd = None

    def update_config(self, filename):
        """
        Update config path variable.
        """
        content = open(filename).read()
        if self.backendcmd:
            pattern = re.compile(r'^backendcmd.*$', re.MULTILINE)
            content = pattern.sub("backendcmd = %s" % self.backendcmd, content)

        pattern = re.compile(r'^procdir.*$', re.MULTILINE)
        content = pattern.sub("procdir = %s" % self.expand_filename('$libexec/%s' % PROJECT_NAME), content)

        pattern = re.compile(r'^logfile.*$', re.MULTILINE)
        content = pattern.sub("logfile = %s" % self.expand_filename('$localstate/log/%s.log' % PROJECT_NAME), content)

        open(filename, 'w').write(content)
        self.announce("File '%s' was updated" % filename)

    def update_transproc_path_to_config(self, filename):
        """
        Update transproc script path variable.
        """
        content = open(filename).read()
        pattern = re.compile(r'^configfile.*$', re.MULTILINE)
        content = pattern.sub("configfile = '%s'" % self.expand_filename('$sysconf/fred/transproc.conf'), content)

        open(filename, 'w').write(content)
        self.announce("File '%s' was updated" % filename)


def main():
    data_files = [
        ('$sysconf/fred', ['transproc.conf']),
        ('$doc', ['backend.xml', 'ChangeLog', 'README']),
        ('$libexec/%s' % PROJECT_NAME, ['proc_csob_xml.py', 'proc_ebanka_csv.py', 'proc_ebanka.py', 'proc_fio_xml.py']),
    ]
    setup(name=PROJECT_NAME,
          author='Jan Kryl',
          author_email='developers@nic.cz',
          url='http://fred.nic.cz/',
          license='GNU GPL',
          platforms=['posix'],
          description='FRED TransProc',
          long_description='Component of FRED (Fast Registry for Enum and Domains)',
          packages=['fred_transproc'],
          scripts=['transproc'],
          data_files=data_files,
          modify_files={'$sysconf/fred/transproc.conf': 'update_config',
                        '$scripts/transproc': 'update_transproc_path_to_config'},
          cmdclass={'install': TransprocInstall})


if __name__ == '__main__':
    main()
