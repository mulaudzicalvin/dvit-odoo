# -*- coding: utf-8 -*-
{
    'name': 'Discount Accounting',
    'summary': 'Discount Accounting',
    'description': """
Sale & Purchase discount accounting entries
=============================================
This module made to process sale & discount accounting entries 
correctly so that it appears in Sale & purchase discount accounts.

Install the module and set the sale & purchase discount accounts 
which should be of type income for sale discounts and expense 
for purchase discounts.

After that if make a discount on SO or PO lines (Odoo's built-in discount)
it will process the discount entries like below:
TBD

Notes: 
------
- Purchase discount entries is not implemented yet, should be here soon.
- This module depends on account_cancel to be able to modify journal entries and add discount items to it using cancel, modify, post approach - better workaround suggestions is more than appreciated.
 """,
'version': '8.0.1.0',
    'category': 'Productivity',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': ['sale','account','account_cancel'],
    'data': [
        'security/ir.model.access.csv',
        'templates.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,

}
