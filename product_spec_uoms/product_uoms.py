# -*- coding: utf-8 -*-

from openerp import models, fields, api

class product_template(models.Model):
    _inherit = 'product.template'
    uom_ids = fields.One2many(comodel_name="product.uom", inverse_name="product_id",
                                string="Product UoMs", required=False, )
    special_uoms = fields.Boolean(string="Special UoMs")
    


class product_uom(models.Model):
    _inherit = 'product.uom'
    # generate_id = fields.Many2one(comodel_name="product.generato", string="", required=False,)
    product_id = fields.Many2one(comodel_name="product.template",
                                string="Product Id", required=False, )
