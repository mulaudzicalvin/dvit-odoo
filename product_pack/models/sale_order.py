# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    def copy(self, default=None):
        sale_copy = super(sale_order, self).copy(default)
        # we unlink pack lines that should not be copied
        pack_copied_lines = sale_copy.order_line.filtered(
                lambda l: l.pack_parent_line_id.order_id == self)
        for line in pack_copied_lines:
            line.pack_parent_line_id=False
        pack_copied_lines.unlink()

        for line in sale_copy.order_line.filtered(
            lambda l: l.pack_child_line_ids and
            l.product_id.pack_price_type == 'totalice_price' and
            not l.pack_parent_line_id):
            line.price_unit = line.env['product.pricelist'].price_get(
                line.product_id.id, line.product_uom_qty,
                line.order_id.partner_id.id)[line.order_id.pricelist_id.id]

        return sale_copy

    def write(self, vals):
        old_lines = self.order_line
        res = super(sale_order, self).write(vals)

        if old_lines:
            for order in self:
                ### we will recalculate all lines that have childs and totalice_price and depth is 0
                for line in order.order_line.filtered(lambda l: l.pack_child_line_ids and
                l.product_id.pack_price_type == 'totalice_price' and not l.pack_parent_line_id):
                    line.update_pack_line_total()
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
