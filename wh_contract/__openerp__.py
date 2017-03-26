# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Contract',
    'version': '8.0.0.1',
    'category': 'Productivity',
    'sequence': 60,
    'summary': 'Links stock operations with contracts.',
    'description': """
    Links stock operations with contracts.
    """,
    'author': 'dvit.me',
    'depends': ['account', 'account_analytic_analysis', 'stock'],
    'data': [
        'templates.xml',
    ],
    'installable': True,
    'application': False,
    'website': 'https://dvit.me',
    'auto_install': False,
}
