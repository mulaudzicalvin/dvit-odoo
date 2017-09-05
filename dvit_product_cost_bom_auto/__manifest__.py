# -*- coding: utf-8 -*-
{
    'name': "Product cost from BoM auto",

    'summary': """
        Auto set product cost from BoM on update.
        """,

    'description': """

1- Auto update BoM cost from its components on write

2- Auto update BoM's Product cost price from the BoM cost on write

3- Auto update cost of all BoMs that include a product on updating that product's cost manually or through purchase orders in case of avg price.
    """,

    'author': "DVIT.ME",
    'website': "http://www.dvit.me",

    'category': 'Uncategorized',
    'version': '10.0.0.4',

    'depends': ['mrp'],

    'data': [],

    'demo': [],
}
