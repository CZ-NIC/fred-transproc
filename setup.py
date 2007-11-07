#!/usr/bin/env python
# vim: set ts=4 sw=4:
#
import sys, os.path, string, commands
from distutils import core
from distutils import log

core.DEBUG = False


try:
	core.setup(name="transproc", version="0.1.0",
			description="Component of FRED (Fast Registry for Enum and Domains)",
			author   = "Jan Kryl",
			author_email="jan.kryl@nic.cz",
			license  = "GNU GPL",
			scripts  = [ "transproc" ],
			data_files = [
				("libexec/transproc",
					[ "proc_ebanka.py" ]
				),
				]
			)

except Exception, e:
	log.error("Error: %s", e)

