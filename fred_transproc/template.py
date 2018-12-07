#
# Copyright (C) 2007-2012  CZ.NIC, z. s. p. o.
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

from xml.sax.saxutils import escape
import types

_template_head = '''<?xml version="1.0" encoding="UTF-8"?>
<statements>
  <statement>
    <account_number>%s</account_number>
    <account_bank_code>%s</account_bank_code>
    <number>%s</number>
    <date>%s</date>
    <balance>%s</balance>
    <old_date>%s</old_date>
    <old_balance>%s</old_balance>
    <credit>%s</credit>
    <debet>%s</debet>
    <items>'''

_template_tail = '''    </items>
  </statement>
</statements>'''

_template_item = '''      <item>
        <ident>%s</ident>
        <account_number>%s</account_number>
        <account_bank_code>%s</account_bank_code>
        <const_symbol>%s</const_symbol>
        <var_symbol>%s</var_symbol>
        <spec_symbol>%s</spec_symbol>
        <price>%s</price>
        <type>%s</type>
        <code>%s</code>
        <status>%s</status>
        <memo>%s</memo>
        <date>%s</date>
        <crtime>%s</crtime>
        <name>%s</name>
      </item>'''


def _escape_data_list(data_list):
    return tuple(escape(item if isinstance(item, types.StringTypes) else str(item)) for item in data_list)


def render_template_head(data_list):
    return _template_head % _escape_data_list(data_list)

def render_template_tail():
    return _template_tail

def render_template_item(data_list):
    return _template_item % _escape_data_list(data_list)
