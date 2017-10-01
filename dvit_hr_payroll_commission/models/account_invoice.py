# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    slip_ids = fields.Many2many('hr.payslip', string='Commission Payslips')

    @api.multi
    def invoice_validate(self):
    	res = super(AccountInvoice, self).invoice_validate()
        emp_id = self.env['hr.employee'].search([('user_id','=',self.user_id.id)])[0]
        contracts = self.env['hr.contract'].search([('employee_id','=',emp_id.id)])
        for contract in contracts:
        	contract._comp_commission()
        return res

