#! /usr/bin/env python
# vim: set ts=4 sw=4:

import sys
import csv
from datetime import datetime
# from datetime import date
# import datetime

from template import template_head
from template import template_tail
from template import template_item

def error(msg):
    sys.stderr.write('Invalid format: ' + msg + '\n')
    sys.exit(1)

if __name__ == '__main__':
    reader = csv.reader(sys.stdin, delimiter=";")
    first_time = True
    for row in reader:
        if len(row) != 16:
            error("Bad number of columns")
        if first_time:
            first_time = False
            own_account_number = row[8].strip()
            own_account_bank_code = row[9].strip()
            own_account = "%s/%s" % (own_account_number, own_account_bank_code)
            number = ""
            date = ""
            balance = ""
            old_date = ""
            old_balance = ""
            credit = ""
            debet = ""
            print template_head % (own_account, number, date, balance,
                    old_date, old_balance, credit, debet)
        ident = row[15].strip()
        account_number = row[6].strip()
        bank_code = row[7].strip()
        const_symbol = row[11].strip()
        var_symbol = row[10].strip()
        spec_symbol = ""
        price = row[4].strip().replace(',', '.').replace(' ', '')
        code = row[13].strip()
        memo = row[12].strip()[:64]
        date = datetime.strptime(row[0].strip(), "%d.%m.%Y")
        crtime = datetime.strptime(row[5].strip(), "%d.%m.%Y %H:%M:%S")
        name = row[14].strip()
        print template_item % (ident, account_number, bank_code,  const_symbol,
                var_symbol, spec_symbol, price, code, memo, date.date().isoformat(),
                crtime.isoformat(" "), name)
    print template_tail

