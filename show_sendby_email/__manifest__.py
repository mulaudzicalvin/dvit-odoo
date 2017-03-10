# -*- coding: utf-8 -*-
{
    'name': "show_sendby_email",

    'summary': """
        always show send email buttons in invoices """,

    'description': """
         This module makes the ( print & Send by email  ) buttons avilabe even after registering an invoice payment .
         """,

    'author': "Dvit",
    'website': "https://www.dvit.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account','base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}