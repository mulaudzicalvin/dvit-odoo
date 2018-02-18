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
            line.order_id=sale_copy
            line.pack_parent_line_id=False
        pack_copied_lines.unlink()
        return sale_copy

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
