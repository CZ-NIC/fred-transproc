CHANGELOG
=========

1.7.1 (2019-11-20)
------------------

* Update spec file for F31 and Centos/RHEL 8

1.7.0 (2019-03-20)
------------------

* License GNU GPLv3+
* Fix rpm build

1.6.1 (2019-02-05)
------------------

* Change severity of console logger (INFO -> ERROR)

1.6.0 (2019-01-15)
------------------

* Add CSOB CEB processor (SOAP + REST)

1.5.0 (2018-10-26)
------------------

* Generalize backend command configuration

  * backend_payment_cmd
  * backend_statement_cmd (see command placeholders in example configuration)

* Use setuptools for packaging
* COPR build
* Removed obsolete processor proc_ebanka.py

1.4.0 (2018-02-14)
------------------

* Add support for dynamic date interval in url for http sources

  * url placeholders {START_DATE} {END_DATE}
  * see example transproc.conf for usage

1.3.0 (2017-03-02)
------------------

* Configuration file documentation
* Fedora packaging

1.2.1 (2013-06-12)
------------------

* Parser for FIO updated to new format

1.2.0 (2013-01-07)
------------------

* Parser for FIO xml data files

1.1.2 (2012-09-10)
------------------

* Whitespace normalization and PEP8-ification
* Update due to distutils changes (setup.cfg)

1.1.1 (2012-06-09)
------------------

* fix - escape function for output xml data (xml entities issue)

1.1.0 (2012-05-14)
------------------

* add support for IMAP SSL

1.0.13 (2012-03-19)
-------------------

* setup.py fix - config file path

1.0.12 (2012-03-15)
-------------------

* config option for change of maximal input read iterations of backend processing command
* ebanka csv processor now picks only realized payments for further processing

1.0.11 (2010-09-11)
-------------------

* config fix - imapfolder parameter - preserve default value of select(...) - INBOX

1.0.10 (2010-08-13)
-------------------

* payments in foreign currency are now included in output xml (with price set to 0)

1.0.9 (2010-06-22)
------------------

* imapfolder config option for IMAP data source
* default log path using installation prefix now

1.0.5 (2010-04-01)
------------------

* Added support for logging
* BugFix: When emtpy csv comes to proc_csob_xml processor,
  it will not generate invalid XML but rather empty string
* Transproc now don't send empty output XML from processor
  to backend (due to bugfix above)

1.0.2 (2010-03-12)
------------------

* Setup.py enhanced
* Some minor bugfixes like exception handling while connecting to HTTP, typos...

1.0.0 (2010-02-19)
------------------

* Support for IMAP + HTTP data sources
* Support for data source types options
* Configurable source data recoding from different charset
* Configurable filter by subject for IMAP source
* Processed mail marking improved
* Import command takes parameter for original statement file and its mimetype (defined in configuration)
* Output xml changes:

  * xml header added
  * oldBalance element renamed to old_balance
  * account_bank_code added to statement xml (account_number splitted)
  * ident should be same if there is more sources for one account (it was set to empty string in proc_ebanka for now)
  * status element added

* proc_ebanka is now not supported because of ``ident`` element problem

1.0.0 (2009-02-11)
------------------

* Parser for CSOB xml files

1.0.0 (2007-11-07)
------------------

* Old ``get_transcripts.py`` script imported and renamed to transproc
* Parser for ebanka transcript completed
* New setup.py installer
