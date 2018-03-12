# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-BroadTech IT Solutions (<http://www.broadtech-innovations.com/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
##############################################################################


{
    'name' : 'dvit account partner ledger currency',
    'version' : '0.1',
    'summary': 'dvit account partner ledger currency',
    'sequence': 1,
    'description': "Merge 2 modules - partner_ledger_filter and partner_ledger_currency",
    'category': 'Accounting',
    'author': 'DVIT.ME',
    'website': 'http://www.dvit.me/',
    'depends' : ['account'],
    'data': [
        'views/report_generalledger.xml',
        'views/report_partnerledger.xml',
        'wizard/account_report_general_ledger_view.xml'
        ],

    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': False,
    'auto_install': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
