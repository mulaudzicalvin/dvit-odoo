# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Restaurant Plus',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'sequence': 60,
    'summary': 'Restaurant Plus',
    'description': """
    This is a merge of point of sale 8 and 9 and pos_restaurant 8 and 9.
    """,
    'author': 'dvit.me',
    'depends': ['sale_stock', 'point_of_sale', 'pos_restaurant'],
    'data': [
        "views/templates.xml", 
        "data/report_paperformat.xml",
        "point_of_sale_report.xml",
        "point_of_sale_view.xml",
        "res_users_view.xml",
    ],
    'qweb':[
        'static/src/xml/multiprint.xml',
        'static/src/xml/splitbill.xml',
        'static/src/xml/printbill.xml',
        'static/src/xml/notes.xml',
        'static/src/xml/floors.xml',
        'static/src/xml/pos.xml'
    ],
    'installable': True,
    'application': True,
    'website': 'https://dvit.me',
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
