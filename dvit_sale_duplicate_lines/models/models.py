# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    duplicate = fields.Boolean("duplicate")

    @api.depends('product_id')
    def update_line_duplicate(self):
        for i in self.order_id.order_line:
            if i.product_id.id == self.product_id.id :
                i.duplicate = False


    @api.multi
    def unlink(self):
        if self.filtered(lambda x: x.state in ('sale', 'done')):
            raise UserError(
                _('You can not remove a sale order line.\nDiscard changes and try setting the quantity to 0.'))
        for l in self:
            l.update_line_duplicate()
        return super(SaleOrderLine, self).unlink()

class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    @api.constrains('order_line')
    @api.depends('order_line')
    def _check_duplicate(self):
        for i in self.order_line:
            for j in self.order_line:
                if i.product_id.id==j.product_id.id and i!=j:
                    i.duplicate=True
