======
README
======

This is a README file for transproc python script and other related scripts.
The purpose of this script is to connect to data source (IMAP, HTTP...), download
new data and process them. Processing is done by dedicated scripts,
where each script handles one transcript format. It is possible to specify
mapping between the transcript processor and data source by several attributes
(like email attribute FROM). Based on these attributes, data is processed by
appropriate processor.

There is a configuration file for transproc, see example transproc.conf
in repository. The configuration file is searched in /etc/fred directory
by default. It is possible to specify its location in command line.
