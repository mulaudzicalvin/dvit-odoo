# -*- coding: utf-8 -*-
{
    'name': "Report Modification",

    'summary': """Report modification""",

    'description': """
    Report modification
    """"""""""""
    contain all data
    """,

    'author': "magdy",
    'website': "http://www.udemy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'School management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reportt.xml',
        'invoice_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}