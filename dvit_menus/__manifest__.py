# -*- coding: utf-8 -*-
{
    'name': 'DVIT Menus',
    'summary': 'DVIT Menus',
    'description': """
    This module changes odoo menu style.
     """,
    'version': '10.0.1.1',
    'category': 'Theme',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': ['web_lang'],
    'conflicts': [],
    'data': ["static/src/xml/main.xml",
    'security/ir.model.access.csv',],  
    'demo': [],
    'installable': False,
    'auto_install': False,
    'application': False,

}