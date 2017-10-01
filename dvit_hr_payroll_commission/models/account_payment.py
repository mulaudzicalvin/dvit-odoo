# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    slip_ids = fields.Many2many('hr.payslip', string='Commission Payslips')

    
