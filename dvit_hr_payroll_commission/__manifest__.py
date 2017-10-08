# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# © 2017 Mohamed M. Hagag (DVIT.ME)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'DVIT Payroll Commisions',
    'summary': 'Payroll Commisions',
    'summary': "Calculate commissions for employees and add it to payslips.",
    'category': 'Human Resources',
    'author': ["DVIT.ME", "Open Net Sarl"],
    'license': 'AGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['hr_payroll_account'],
    'version': '10.0.3.0',
    'website': 'http://dvit.me',
    'data': [
        'views/hr_contract_view.xml',
        'views/hr_payroll_view.xml',
        'data/hr.salary.rule.xml',
    ],
    'installable': True,
    'auto_install': False,
}
