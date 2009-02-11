#! /usr/bin/env python
# vim: set ts=4 sw=4:

# according to http://www.csob.cz/bankcz/cz/Produktovy-katalog/Elektronicke-bankovnictvi/CSOB-BusinessBanking-24/Prirucky-a-navody-CSOB-BusinessBanking-24.htm

import sys
import xml.etree.ElementTree
import datetime

template_head = '''<statements>
  <statement>
    <account_number>%s</account_number>
    <number>%s</number>
    <date>%s</date>
    <balance>%s</balance>
    <old_date>%s</old_date>
    <oldBalance>%s</oldBalance>
    <credit>%s</credit>
    <debet>%s</debet>
    <items>'''

template_tail = '''    </items>
  </statement>
</statements>'''

template_item = '''      <item>
        <account_number>%s</account_number>
        <account_bank_code>%s</account_bank_code>
        <const_symbol>%s</const_symbol>
        <var_symbol>%s</var_symbol>
        <spec_symbol>%s</spec_symbol>
        <price>%s</price>
        <code>%s</code>
        <memo>%s</memo>
        <date>%s</date>
      </item>'''

def date_to_iso(date):
    """DD.MM.YYYY to YYYY-MM-DD"""
    return date[6:10] + "-" + date[3:5] + "-" + date[0:2]

if __name__ == '__main__':
    top = xml.etree.ElementTree.ElementTree()
    top.parse(sys.stdin)
    finsta03 = top.find("FINSTA03")
    account_number = finsta03.findtext("S25_CISLO_UCTU")
    number = finsta03.findtext("S28_CISLO_VYPISU")

    old_date = date_to_iso(finsta03.findtext("S60_DATUM"))
    old_balance = finsta03.findtext("S60_CASTKA").replace(",", ".")
    old_balance_sign = finsta03.findtext("S60_CD_INDIK").replace("C", "").replace("D", "-")

    date = date_to_iso(finsta03.findtext("S62_DATUM"))
    balance = finsta03.findtext("S62_CASTKA").replace(",", ".")
    balance_sign = finsta03.findtext("S62_CD_INDIK").replace("C", "").replace("D", "-")

    credit = finsta03.findtext("SUMA_KREDIT", "").replace(",", ".").replace("=", "")
    debet = finsta03.findtext("SUMA_DEBIT", "").replace(",", ".").replace("=", "")

    old_balance = old_balance_sign + old_balance
    balance = balance_sign + balance
    credit = credit
    debet = debet

    print template_head % (account_number, number, date, balance, old_date,
            old_balance, credit, debet)

    finsta05 = finsta03.findall("FINSTA05")
    for item in finsta05:
        account_number = item.findtext("PART_ACCNO", "")
        account_bank_code = item.findtext("PART_BANK_ID", "")
        const_symbol = item.findtext("S86_KONSTSYM", "")
        var_symbol = item.findtext("S86_VARSYMOUR", "")
        spec_symbol = item.findtext("S86_SPECSYMOUR", "")
        price = item.findtext("S61_CASTKA").replace("+", "")
        memo = item.findtext("PART_ACC_ID")
        date = date_to_iso(item.findtext("DPROCD"))
        code = item.findtext("S61_CD_INDIK")
        if code == "D":
            code = 1
        elif code == "C":
            code = 2
        elif code == "DR":
            code = 3
        elif code == "CR":
            code = 4

        print template_item % (account_number, account_bank_code, const_symbol,
                var_symbol, spec_symbol, price, code, memo, date)

    print template_tail


