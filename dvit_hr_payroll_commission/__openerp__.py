# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payroll Commisions',
    'summary': 'Payroll Commisions',
    'category': 'Human Resources',
    'author': ["DVIT.ME","Open Net Sarl"],
    'depends': [
        'hr_payroll_account',
    ],
    'version': '8.0.3.0',
    'auto_install': False,
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'data': [
        'views/hr_contract_view.xml',
        'views/hr_payroll_view.xml',
        'data/hr.salary.rule.xml',
    ],
    'installable': True
}
