# -*- coding: utf-8 -*-

from openerp import models, fields, api

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    contract = fields.Many2one(string="Contract", comodel_name="account.analytic.account")


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    stock_picking_ids = fields.One2many(comodel_name="stock.picking", inverse_name="contract",
                                        string="Stock Operations", required=False, )
    
