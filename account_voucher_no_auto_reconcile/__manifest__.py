# -*- coding: utf-8 -*-
{
    'name': "Account Voucher no auto reconcile",

    'summary': """ Account voucher / payment no auto line match nor reconcilation.""",

    'description': """
Account Voucher / Payment no line auto match nor reconcilation.
================================================================
This module will add a new button "Manual reconcilation" in the account voucher
to reset all auto reconciled lines.
    """,
    'author': "DVIT.me",
    'website': "http://www.dvit.me",
    'category': 'Accounting',
    'version': '10.0.0.1',
    'depends': ['account_voucher'],
    'data': ['views.xml'],
    'installable': False,
    'auto_install': False,
    'application': False,
}
