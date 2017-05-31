# -*- coding: utf-8 -*-
{
    'name': "Report Modification",

    'summary': """Report modification""",

    'description': """
    Report modification
    """"""""""""
    """,

    'author': "DVIT.ME",
    'website': "http://dvit.me",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reportt.xml',
        'invoice_report.xml'
    ],
}
