# -*- coding: utf-8 -*-

{
    "name": "Product Multi UoM with conversion ratio",
    "version": "10.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "price": 125.0,
    "currency": 'EUR',
    'summary': 'Allow creating different multi UoMs per product like 1 box = 5 kg and 1 kg = 7 meter.',
    'description': """
    Allow creating different multi UoMs per product like 1 box = 5 kg and 1 kg = 7 meter.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['product'],
    "data": ["wizard/views.xml"],
	 "images": [
        'static/description/banner.png'
    ],
    "installable": True,
}
