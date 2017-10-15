{
    'name': 'POS Fixes',
    'summary': 'Point of Sale Fixes: complete stock account moves, mark pos invoices as paid and reconcile them.',
    'description': """
    Fixes included:

    - Fix POS invoices payments by reconciling them automatically on POS session closing to get them paid.

    - Complete the Gr/Ir anglo-saxon journal entries missing in POS.

    - Now supports IngAdhoc's Product packs 1- create anglo-saxon for packs.

    ToDo:

    - Improve performance by reconciling invoices per order close not in session close .

     """,
     "license": "AGPL-3",
     "price": 35.0,
     "currency": 'EUR',
    'version': '10.0.2.0',
    'category': 'Point of Sale',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
        'point_of_sale',
        'purchase',
        ],
    'data': ['views.xml'],
    'installable': True,
    'auto_install': True,
    'application': False,

}
