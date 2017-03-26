# -*- coding: utf-8 -*-
{
    'name': 'Contract to Sale Order to Tasks',
    'summary': 'Contract info on sale order & tasks',
    'description': """
    This module had been made to:-

    - Automatically add the customer name from the contract to new sale orders.
    - Add the description of Sale Order to generated task name.

     """,
    'version': '8.0.1.0',
    'category': 'Productivity',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': ['project','account_analytic_analysis','sale'],
    'conflicts': [],
    'data': ['templates.xml'],
    'installable': True,
    'auto_install': False,
    'application': False, 
}
