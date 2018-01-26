# -*- coding: utf-8 -*-

{
    "name": "MRP BoM extra costs",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "price": 15.0,
    "currency": 'EUR',
    'summary': 'Allow adding indirect overhead costs on BoM as a percent of its costs.',
    'description': """
Allow adding indirect overhead costs on BoM as a percent of its costs.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['dvit_product_cost_bom_auto'],
    "data": ["views/views.xml", ],
    "installable": True,
}
