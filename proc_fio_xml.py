#! /usr/bin/env python
# vim: set ts=4 sw=4:

# according to http://www.fio.cz/docs/cz/API_Bankovnictvi.pdf
# https://www.fio.cz/ib_api/rest/last/{token}/transactions.{format}

import sys
import xml.etree.ElementTree
import re
from datetime import datetime

from fred_transproc.template import render_template_head, render_template_tail, render_template_item

# FIO date: YYYY-mm-dd+GMT
# GMT: HH:MM
re_date = re.compile("^([0-9]+-[0-9]+-[0-9]+)[+-][0-9]+:[0-9]+$")

def get_isoformat_date(fio_date):

    global re_date
    if not fio_date:
        return ""
    re_fio_date = re_date.match(fio_date)
    if not re_fio_date:
        return ""
    return datetime.strptime(re_fio_date.group(1), "%Y-%m-%d").date().isoformat()


if __name__ == '__main__':
    top = xml.etree.ElementTree.ElementTree()
    top.parse(sys.stdin)
    info = top.find("Info")
    account_number_our = info.findtext("accountId")
    account_bank_code_our = info.findtext("bankId")
    number = info.findtext("idList")

    old_date = get_isoformat_date(info.findtext("dateStart"))
    old_balance = info.findtext("openingBalance").replace(",", ".")

    date = get_isoformat_date(info.findtext("dateEnd"))
    balance = info.findtext("closingBalance").replace(",", ".")

    credit = ""
    debet = ""

    print unicode(render_template_head([account_number_our, account_bank_code_our, number, date, balance, old_date,
            old_balance, credit, debet])).encode('utf8')

    transaction_list = top.find("TransactionList")
    if transaction_list is not None:
        for item in transaction_list.findall("Transaction"):
            ident = item.findtext("column_22")
            account_number = item.findtext("column_2", "")
            account_bank_code = item.findtext("column_3", "")
            const_symbol = item.findtext("column_4", "")
            var_symbol = item.findtext("column_5", "")
            spec_symbol = item.findtext("column_6", "")
            price = item.findtext("column_1").replace("+", "").replace(",", ".")
            name = item.findtext("column_10", "")
            date = get_isoformat_date(item.findtext("column_0"))
            code = "1" # 1-normal transaction; 2-storno transaction
            memo = item.findtext("column_16", "")[:64]
            crtime = '' # time when we inserted it to our database (transproc don't fill it)

            type = "" # only for output for backend, transproc leaves this blank

            # all payments in FIO XML are realized:
            status = "1" # 1-Realized (only this should be further processed)

            print unicode(render_template_item([ident, account_number, account_bank_code,
                    const_symbol, var_symbol, spec_symbol, price, type, code, status, memo,
                    date, crtime, name])).encode('utf8')

    print unicode(render_template_tail()).encode('utf8')
