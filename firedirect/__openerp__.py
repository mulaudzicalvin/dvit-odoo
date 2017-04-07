# -*- coding: utf-8 -*-
{
    'name': "firedirect",

    'summary': """
        Area to manage courses for fire-direct
        """,

    'description': """
        Area to manage courses for fire-direct
    """,

    'author': "Bahr Solutions",
    'website': "http://www.bahrsolutions.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','email_template','board','hr','web_instcalendar'],

    # always loaded
    'data': [
        'security/firedirect_security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
        'status.xml',
        'reports.xml',
        'report/company.xml',
        'report/instructor.xml',
        'report/form.xml',
        'report/daily.xml',
        'email.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}