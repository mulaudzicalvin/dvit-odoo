# -*- coding: utf-8 -*-
{
    'name': "DarDelta Report new",

    'summary': """
        Report modification""",

    'description': """
        Report modification
    """,

    'author': "DVIT.ME",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','hr'],

    # always loaded
    'data': [
        'report.xml',
        'template.xml',

    ],
}
