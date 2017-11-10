# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    purchase_ids = fields.One2many(
        string="Purchase Orders",
        comodel_name="purchase.order",
        inverse_name="production_id"
    )

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    production_id = fields.Many2one(
        string="Manufacturing Orders",
        comodel_name="mrp.production",
    )
