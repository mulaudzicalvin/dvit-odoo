# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        res.write({'code':res.code})
        return res

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        for bom in self:
            bom_cost = 0.0
            for line in bom.bom_line_ids:
                if line.product_uom == line.product_id.uom_id:
                    bom_cost += (line.product_id.standard_price * line.product_qty) / bom.product_qty
                else:
                    price = line.product_id.standard_price
                    uom = self.env['product.uom']
                    from_uom = line.product_id.uom_id.id
                    to_uom = line.product_uom.id
                    print "-------------"
                    print from_uom
                    print to_uom
                    unit_price = uom._compute_price(from_uom, price, to_uom)
                    print unit_price
                    print "-------------"
                    bom_cost += (unit_price * line.product_qty) / bom.product_qty
            bom.product_tmpl_id.standard_price = bom_cost
        return res


class ProdTempl(models.Model):
    _inherit = "product.template"
    @api.multi
    def write(self,vals):
        res = super(ProdTempl,self).write(vals)
        for prod in self:
            # get all bom lines contain this prod
            bom_line_ids = self.env['mrp.bom.line'].search([('product_id.product_tmpl_id','=',prod.id)])

            for bom_line_id in bom_line_ids:
                #trigger write on bom to update the cost.
                bom_line = self.env['mrp.bom.line'].browse(bom_line_id.id)
                bom = bom_line.bom_id
                bom.write({'position':bom_line.bom_id.position})
        return res
