# -*- coding: utf-8 -*-
{
    'name': "Product Generator",

    'summary': """
        This module allow you to create a product with Uom quiclu and simple """,

    'description': """

    """,

    'author': "DVIT",
    'website': "https://www.dvit.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','sale'],

    # always loaded
    'data': [
        'product_generator_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}