#! /usr/bin/env python2
#
# Copyright (C) 2009-2019  CZ.NIC, z. s. p. o.
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

# according to http://www.csob.cz/cz/Produktovy-katalog/Elektronicke-bankovnictvi/CSOB-BusinessBanking-24/Stranky/Prirucky-a-navody-CSOB-BusinessBanking-24.aspx

import sys
import xml.etree.ElementTree
from datetime import datetime

from fred_transproc.template import render_template_head, render_template_tail, render_template_item


if __name__ == '__main__':
    top = xml.etree.ElementTree.ElementTree()
    top.parse(sys.stdin)
    finsta03 = top.find("FINSTA03")
    account_number_our, account_bank_code_our = finsta03.findtext("S25_CISLO_UCTU").split('/')
    number = finsta03.findtext("S28_CISLO_VYPISU")

    old_date = datetime.strptime(finsta03.findtext("S60_DATUM"), "%d.%m.%Y").date().isoformat()
    old_balance = finsta03.findtext("S60_CASTKA").replace(",", ".")
    old_balance_sign = finsta03.findtext("S60_CD_INDIK").replace("C", "").replace("D", "-")

    date = datetime.strptime(finsta03.findtext("S62_DATUM"), "%d.%m.%Y").date().isoformat()
    balance = finsta03.findtext("S62_CASTKA").replace(",", ".")
    balance_sign = finsta03.findtext("S62_CD_INDIK").replace("C", "").replace("D", "-")

    credit = finsta03.findtext("SUMA_KREDIT", "").replace(",", ".").replace("=", "")
    debet = finsta03.findtext("SUMA_DEBIT", "").replace(",", ".").replace("=", "")

    old_balance = old_balance_sign + old_balance
    balance = balance_sign + balance
    credit = credit
    debet = debet

    print unicode(render_template_head([account_number_our, account_bank_code_our, number, date, balance, old_date,
            old_balance, credit, debet])).encode('utf8')

    finsta05 = finsta03.findall("FINSTA05")
    for item in finsta05:
        ident = item.findtext("S28_POR_CISLO")
        account_number = item.findtext("PART_ACCNO", "")
        account_bank_code = item.findtext("PART_BANK_ID", "")
        const_symbol = item.findtext("S86_KONSTSYM", "")
        var_symbol = item.findtext("S86_VARSYMOUR", "")
        spec_symbol = item.findtext("S86_SPECSYMOUR", "")
        price = item.findtext("S61_CASTKA").replace("+", "").replace(",", ".")
        name = item.findtext("PART_ACC_ID")
        date = datetime.strptime(item.findtext("DPROCD"), "%d.%m.%Y").date().isoformat()
        code = item.findtext("S61_CD_INDIK")
        memo = item.findtext("PART_ID1_1")[:64]
        crtime = ''

        # code can be D - debet, C - credit, DR - storno deposit and CR - storno credit
        # (we already know difference between C and D by sign of price - so to <code> tag
        #  we save only whether it is normal (1) or storno(2) transaction):
        if code in ("D", "C"):
            code = "1"
        elif code in ("DR", "CR"):
            code = "2"

        type = "1"  # not decided (not processed)

        # all payments in CSOB XML are realized:
        status = "1"

        print unicode(render_template_item([ident, account_number, account_bank_code,
                const_symbol, var_symbol, spec_symbol, price, type, code, status, memo,
                date, crtime, name])).encode('utf8')

    print unicode(render_template_tail()).encode('utf8')
