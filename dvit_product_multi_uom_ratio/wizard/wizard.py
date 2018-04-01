from odoo import models, fields, api


class WizTaskStockLines(models.TransientModel):
    _name = "wiz.prod.uom.line"
    wiz_id = fields.Many2one(string="prod_uom",comodel_name="wiz.prod.uom",)
    uom = fields.Char(string="Name", )
    qty = fields.Float(string="Ratio", )


class WizProdUoM(models.TransientModel):
    _name = 'wiz.prod.uom'

    line_ids = fields.One2many(string="UoMs",comodel_name="wiz.prod.uom.line",inverse_name="wiz_id",)
    ref_uom = fields.Char(string="Main UoM", )

    def create_uoms(self):
        product_id = self.env['product.template'].browse([self.env.context.get('active_id', False)])
        prod_name = product_id.name.replace(' ','')[:5]
        uom_categ_id = self.env['product.uom.categ'].create({'name':product_id.name+'_uoms'})
        ref_uom_id = self.env['product.uom'].create({
        'name': self.ref_uom,
        'uom_type': 'reference',
        'category_id': uom_categ_id.id,
        'rounding': 0.001,
        'factor': 1,
        'factor_inv': 1,
        })
        product_id.write({
        'uom_id': ref_uom_id.id,
        'uom_po_id': ref_uom_id.id,
        })
        for line in self.line_ids:
            self.env['product.uom'].create({
            'name': line.uom,
            'uom_type': line.qty > 0 and 'bigger' or 'smaller',
            'factor_inv': line.qty > 0 and line.qty or (1/abs(line.qty)),
            'factor': line.qty < 0 and abs(line.qty) or (1/abs(line.qty)),
            'category_id': uom_categ_id.id,
            'rounding': 0.001,
            })

        return True

    @api.multi
    def add_uoms(self):
        uom_ids = self.create_uoms()

        return True
