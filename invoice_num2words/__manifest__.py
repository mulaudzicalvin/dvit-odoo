{
    'name': 'Invoice Number to words',
    'version': '0.1',
    'category': 'Accounting',
        'sequence': 1,
    'summary': "Show invoice Total in words. ",
    'description':"Show invoice Total in words. ",
    'author': 'DVIT',
    'website': 'http://www.dvit.me',

    "external_dependencies": {
    'python': ['num2words']
        },

    'depends': ['account'],
    'data': [
        'views/report_invoice.xml',
        'templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
