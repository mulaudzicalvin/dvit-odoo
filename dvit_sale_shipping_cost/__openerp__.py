# -*- coding: utf-8 -*-
{
    'name': "dvit_sale_shipping_cost",

    'summary': """
        Add shipping cost and information to Sale order and create journal entry
        on sale confirmation.""",

    'author': "DVIT.ME",
    'website': "http://dvit.me",

    'category': 'sale',
    'version': '8.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    #
}
