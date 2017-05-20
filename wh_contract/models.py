# -*- coding: utf-8 -*-

from openerp import models, fields, api

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    contract_id = fields.Many2one('account.analytic.account','Contract')


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    stock_picking_ids = fields.One2many('stock.picking', 'contract_id',
                                        string="Stock Operations", copy=True )
    
