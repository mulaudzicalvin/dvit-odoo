# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    shipping_company = fields.Boolean(string="Shipping Company?")

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    shipping_service = fields.Boolean(string="Shipping Service?")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    shipping_company = fields.Many2one('res.partner', 'Shipping Company')
    shipping_service = fields.Many2one('product.template', 'Shipping Service')
    shipping_qty = fields.Integer('Shipped Qty')
    shipping_entry = fields.Many2one('account.move','Shipping Journal Entry')

    @api.multi
    def action_cancel(self, context=None):
        res = super(SaleOrder,self).action_cancel(context=context)
        # if self.shipping_entry:
        journal_allow_cancel = self.shipping_entry.journal_id.update_posted
        self.shipping_entry.journal_id.write({'update_posted':True})
        self.shipping_entry.button_cancel()
        self.shipping_entry.unlink()
        self.shipping_entry.journal_id.write({'update_posted':journal_allow_cancel})
        return res

    @api.multi
    def action_button_confirm(self, context=None):
        super(SaleOrder,self).action_button_confirm(context=context)
        self._create_shipping_cost_entry(self.shipping_company, self.shipping_service, self.shipping_qty)

    def _create_shipping_cost_entry(self, company, service, qty):
        # service = self.shipping_service
        # company = self.shipping_company
        # qty = self.shipping_qty

        AM = self.env['account.move']
        AML = self.env['account.move.line']
        JID = self.env['account.journal'].search([['type','=','purchase']])[0]
        period = self.env['account.period'].find()

        move = AM.create({
            'name': 'shipping for ' + self.name,
            'ref': 'shipping for ' + self.name,
            'date': self.create_date,
            'journal_id': JID.id,
            'period_id': period.id,
            })

        dr_line = AML.create({
        'name': 'shipping for ' + self.name,
        'journal_id': move.journal_id.id,
        'move_id': move.id,
        'account_id': service.property_account_expense.id,
        'debit': service.standard_price * qty,
        'period_id': period.id,
            })

        cr_line = AML.create({
        'name': 'shipping for ' + self.name,
        'journal_id': move.journal_id.id,
        'move_id': move.id,
        'account_id': company.property_account_payable.id,
        'partner_id': company.id,
        'credit': service.standard_price * qty,
        'period_id': period.id,
            })

        self.write({'shipping_entry':move.id,})

        return True
