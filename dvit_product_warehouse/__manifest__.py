

{
    'name': 'Product warehouse',
    'summary': 'Force product/category warehouse on sale, purchase and manufacturing orders',
    'version': '10.0.1.0',
    "author": 'DVIT.ME',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    "price": 199.0,
    "currency": 'EUR',
    'website': "http://www.dvit.me",
    'depends': ['sale_stock',
                'purchase',
                # 'mrp',
                ],
    'data': [
        'view/templates.xml'
    ],
    'installable': True,
}
