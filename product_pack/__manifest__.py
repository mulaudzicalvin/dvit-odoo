# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'DVIT Product Pack',
    'version': '10.0.2.1',
    'category': 'Product',
    'sequence': 1,
    'summary': 'Product bundles and packages',
    'description': """
Product Pack
============
Based on INGADHOC's product_pack, Improved and fixed some features.
currently this module is doing the following:
- allow configuring a product as a package or bundle that contains multiple products
- adding a package to sale order, will add its components to the sale order if it's a detailed package
- we can select one of four package types for sale orders:
    - Detailed - component prices: show component prices and the pack price is zero
    - ... ToDo: complete the description...

DVIT Improvments:
- The package product is always a service - enforced.
- Non fixed price packages have their sale price calculated automatically and enforced.
- Package lines on Pack tab on product form have price & Subtotal price on each line plus package total - lst_price
- updating a component product sale price will update all packages' sale prices that contain this component
- On sale order if we remove a line that's part of a package - the package price will be updated
- On sale order every line have the original product price as reference
- Package line discounts is useless - so removed
- Non-detailed packages now creates warehouse moves and pickings for its components
- Packages are now supported on the Point of Sale using product_pack_pos module
    """,
    'author':  'NaN·tic, ADHOC, DVIT.ME',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pack_view.xml',
        'views/sale_view.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
