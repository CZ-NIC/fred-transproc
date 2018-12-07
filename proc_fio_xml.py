#! /usr/bin/env python
#
# Copyright (C) 2012-2018  CZ.NIC, z. s. p. o.
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

# according to http://www.fio.cz/docs/cz/API_Bankovnictvi.pdf
# https://www.fio.cz/ib_api/rest/periods/{token}/2012-01-01/2013-12-31/transactions.xml

import sys
import xml.etree.ElementTree
import re
from datetime import datetime

from fred_transproc.template import render_template_head, render_template_tail, render_template_item

# FIO date: YYYY-mm-dd+GMT
# GMT: HH:MM
re_date = re.compile("^([0-9]+-[0-9]+-[0-9]+)[+-][0-9]+:[0-9]+$")
re_xml_tag = re.compile("^({[^}]*})?(.*)$")

def get_isoformat_date(fio_date):

    global re_date
    if not fio_date:
        return ""
    re_fio_date = re_date.match(fio_date)
    if not re_fio_date:
        return ""
    return datetime.strptime(re_fio_date.group(1), "%Y-%m-%d").date().isoformat()


def parse_tag(tag):

    global re_xml_tag
    r_tag = re_xml_tag.match(tag)
    if r_tag is not None:
        return {'ns':r_tag.group(1), 'tag':r_tag.group(2)}
    return {'ns':'', 'tag':tag}


if __name__ == '__main__':
    top = xml.etree.ElementTree.ElementTree()
    root = top.parse(sys.stdin)

    tag = parse_tag(root.tag)
    if tag['tag']!="AccountStatement":
        sys.exit(1)
    nsFio = tag['ns']
    if nsFio is None:
        nsFio = ""
    info = root.find(nsFio+"Info")
    if info is None:
        sys.exit(1)

    info_data = {'accountId':"",
                 'bankId':"",
                 'idList':"",
                 'dateStart':"",
                 'openingBalance':"",
                 'dateEnd':"", 
                 'closingBalance':"",
                 'credit':"",
                 'debet':""}

    for item in info:
        tag = parse_tag(item.tag)['tag']
        if tag in ('dateStart', 'dateEnd'):
            info_data[tag] = get_isoformat_date(item.text)
        elif tag in info_data:
            info_data[tag] = item.text

    print unicode(render_template_head([info_data['accountId'], info_data['bankId'], info_data['idList'],
                                        info_data['dateEnd'], info_data['closingBalance'],
                                        info_data['dateStart'], info_data['openingBalance'],
                                        info_data['credit'], info_data['debet']])).encode('utf8')

    transaction_list = root.find(nsFio+"TransactionList")
    if transaction_list is not None:
        tag_ident             = nsFio + "column_22"
        tag_account_number    = nsFio + "column_2"
        tag_account_bank_code = nsFio + "column_3"
        tag_const_symbol      = nsFio + "column_4"
        tag_var_symbol        = nsFio + "column_5"
        tag_spec_symbol       = nsFio + "column_6"
        tag_currency          = nsFio + "column_14"
        tag_price             = nsFio + "column_1"
        tag_name              = nsFio + "column_10"
        tag_date              = nsFio + "column_0"
        tag_memo              = nsFio + "column_16"
        for tr in transaction_list:
            if parse_tag(tr.tag)['tag']!="Transaction":
                continue
            ident = tr.findtext(tag_ident)
            account_number = tr.findtext(tag_account_number, "")
            account_bank_code = tr.findtext(tag_account_bank_code, "")
            const_symbol = tr.findtext(tag_const_symbol, "")
            var_symbol = tr.findtext(tag_var_symbol, "")
            spec_symbol = tr.findtext(tag_spec_symbol, "")
            currency = tr.findtext(tag_currency, "")
            if currency.upper()=="CZK":
                price = tr.findtext(tag_price, "0").replace("+", "").replace(",", ".")
            else:
                price = "0"
            name = tr.findtext(tag_name, "")
            date = get_isoformat_date(tr.findtext(tag_date))
            code = "1" # 1-normal transaction; 2-storno transaction
            memo = tr.findtext(tag_memo, "")[:64]
            crtime = '' # time when we inserted it to our database (transproc don't fill it)

            type = "1"  # not decided (not processed)

            # all payments in FIO XML are realized:
            status = "1" # 1-Realized (only this should be further processed)

            print unicode(render_template_item([ident, account_number, account_bank_code,
                    const_symbol, var_symbol, spec_symbol, price, type, code, status, memo,
                    date, crtime, name])).encode('utf8')

    print unicode(render_template_tail()).encode('utf8')
