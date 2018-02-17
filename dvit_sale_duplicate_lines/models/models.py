# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    duplicate = fields.Boolean("duplicate")


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    @api.constrains('order_line','amount_total')
    @api.onchange('order_line')
    def _check_duplicate(self):
        for i in self.order_line:
            i.duplicate = False
            for j in self.order_line:
                if i.product_id.id == j.product_id.id and i != j:
                    i.duplicate=True
