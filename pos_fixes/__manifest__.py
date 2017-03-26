{
    'name': 'POS Fixes',
    'summary': 'Point of Sale Fixes',
    'description': """
    This module **does not** deppend on IngAdhoc's product_pack anymore.

    Fixes included:

    - Fix POS invoices payments by reconciling them automatically on POS session closing to get them paid.

    - Complete the anglo-saxon journal entries missing in POS.

    - Support & Process sales of product packs by IngAdhoc's product_pack.

    - prevent barcode on payment screen by preventing payments greater than order amount * 100 .

     """,
    'version': '10.0.0.1',
    'category': 'Point of Sale',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'LGPL-3',
    'price': '20.0'
    'depends': [
<<<<<<< HEAD:pos_fixes/__manifest__.py
=======
        # 'account_anglo_saxon',
>>>>>>> 70c491072c316faf3ae086a9263da7c55d3b6fc5:pos_fixes/__manifest__.py
        'account',
        'account_voucher',
        'point_of_sale',
    ],
    'data': ['views.xml'],
<<<<<<< HEAD:pos_fixes/__manifest__.py
    'demo': [],
    'installable': False,
    'auto_install': False,
=======
    'conflicts': ['pos_anglo_saxon',
                  'pos_invoice_reconcile'],
    'installable': True,
    'auto_install': True,
>>>>>>> 70c491072c316faf3ae086a9263da7c55d3b6fc5:pos_fixes/__manifest__.py
    'application': False,

}
