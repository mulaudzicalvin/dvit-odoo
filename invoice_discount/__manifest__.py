{
    'name': 'Invoice Discount',
    'version': '1.0',
    'category': 'Accounting',
        'sequence': 1,
    'summary': "Show Discount Total and Total before Discount on Invoices. ",
    'description':"Show Discount Total and Total before Discount on Invoices.",
    'author': 'DVIT',
    'website': 'http://dvit.me',
    'website': 'http://www.dvit.me',
    'depends': ['account_voucher'],
    'data': [
        'discount_view.xml',
        'views/report_discount.xml',
    ],
    'installable': False,
    'auto_install': False,
}


