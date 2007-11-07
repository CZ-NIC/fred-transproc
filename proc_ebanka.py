#!/usr/bin/env python
#
# vim: set ts=4 sw=4:

import sys

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
    <items>
'''

template_tail = '''    </items>
  </statement>
</statements>
'''

template_item = '''      <item>
        <account_number>%s</account_number>
        <account_bank_code>%s</account_bank_code>
        <const_symbol>%s</const_symbol>
        <var_symbol>%s</var_symbol>
        <spec_symbol>%s</spec_symbol>
        <price>%s</price>
        <memo>%s</memo>
        <date>%s</date>
      </item>
'''

def error(msg):
	sys.stderr.write('Invalid format: ' + msg + '\n')
	sys.exit(1)

def getfield(str, i, delim = ' '):
	list = [ field for field in str.split(delim) if field ]
	if len(list) < i:
		error('Required field %d is not present in string "%s"' % (i, str))
	return list[i - 1]


if __name__ == '__main__':
	input = sys.stdin.read()
	input = input.replace('\r', '').strip() # delete \r characters
	sections = [ section.strip() for section in input.split('\n\n') if section ]
	if len(sections) != 3:
		error('Transcript has %d sections and should have 3' % len(sections))
	# header 1
	lines = [ line.strip() for line in sections[0].split('\n') ]
	if lines[0] != 'eBanka':
		error('Transcript does not start with "eBanka" word')
	var_number = getfield(lines[1], 4)
	tmp_date = getfield(lines[2], 2).split('.')
	var_date = tmp_date[2] + '-' + tmp_date[1] + '-' + tmp_date[0]
	# header 2
	lines = [ line.strip() for line in sections[1].split('\n') ]
	var_account_id = getfield(lines[1], 3)
	# header 3 + body
	subsections = [ section.strip() for section in sections[2].split('=' * 86) if section ]
	if len(subsections) not in [2, 5]:
		error('Transcript has %d subsections and should have 3 or 5' %
				len(subsections))
	# header 3
	lines = [ line.strip() for line in subsections[1].split('\n') ]
	var_oldBalance = getfield(lines[0], 2, '  ').replace(' ', '')
	var_credit     = getfield(lines[1], 3, '  ').replace(' ', '')
	var_debet      = getfield(lines[2], 3, '  ').replace(' ', '')
	var_balance    = getfield(lines[4], 2, '  ').replace(' ', '')
	# print what we have so far
	print template_head % (var_account_id, var_number, var_date, var_balance,
			var_date, var_oldBalance, var_credit, var_debet)
	# body
	if len(subsections) > 2:
		transfers = [ transfer for transfer in subsections[4].split('-' * 86) if transfer ]
		for transfer in transfers:
			lines = [ line for line in transfer.split('\n') if line ][:3]
			if len(lines) != 3:
				error('Bad number of lines of transaction item')
			item_spec_symbol = lines[0][44:55].strip()
			item_price = lines[0][55:76].strip().replace(' ','')
			item_memo = lines[1][11:33].strip()
			item_var_symbol = lines[1][44:55].strip()
			(item_account_number, item_account_bank_code) = lines[2][11:33].strip().split('/')
			item_const_symbol = lines[2][44:55].strip()
			print template_item % (item_account_number, item_account_bank_code,
					item_const_symbol, item_var_symbol, item_spec_symbol,
					item_price, item_memo, var_date)

	print template_tail
	sys.exit(0)
