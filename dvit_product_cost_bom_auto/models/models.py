# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        for bom in self:
            bom_cost = 0.0
            for line in bom.bom_line_ids:
        if line.product_id.uom_id == line.product_uom:
                    bom_cost += line.product_id.standard_price * line.product_qty
            self.product_tmpl_id.standard_price = bom_cost

        return res

