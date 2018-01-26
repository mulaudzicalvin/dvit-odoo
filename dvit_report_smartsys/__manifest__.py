{
    'name': 'DVIT SMARTSYS Report ',
    'summary': 'SMARTSYS Report',
    'version': '10.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': "DVIT.ME",
    'website': 'http://dvit.me/',
    "price": 500.0,
    "currency": 'EUR',
    'depends': [
        'product_pack',
        'sales_report_product_image',
        'sale_report_hide_price',
        'dvit_sale_discount',
        ],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
