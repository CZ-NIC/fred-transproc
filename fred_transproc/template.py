template_head = '''<?xml version="1.0" encoding="UTF-8"?>
<statements>
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
        <ident>%s</ident>
        <account_number>%s</account_number>
        <account_bank_code>%s</account_bank_code>
        <const_symbol>%s</const_symbol>
        <var_symbol>%s</var_symbol>
        <spec_symbol>%s</spec_symbol>
        <price>%s</price>
        <type>%s</type>
        <code>%s</code>
        <memo>%s</memo>
        <date>%s</date>
        <crtime>%s</crtime>
        <name>%s</name>
      </item>'''
