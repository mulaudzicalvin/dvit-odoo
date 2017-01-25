# -*- coding: utf-8 -*-

from openerp import models, fields, api

class product_generator(models.Model):
    _name = 'product.generator'
    #
    # name = fields.Char()
    # product_name = fields.Char(string="Product Name", required=True, )
    # product_uom = fields.Char(string="Product Uom", required=True, )
    # product_uom_category = fields.Char(string="Product Uom Category", required=True, )
    # # uom_ids = fields.One2many(comodel_name="product.uom", inverse_name="generate_id", string="", required=False, )
    # @api.multi
    # def generate_product(self):
    #     product_obj=self.env['product.product']
    #     uom_obj=self.env['product.uom']
    #     uom_categ_obj=self.env['product.uom.categ']
    #
    #     uom_categ_id=uom_categ_obj.create({
    #         'name': self.product_uom_category,
    #     })
    #     uom_id=uom_obj.create({
    #         'name': self.product_uom,
    #         'category_id': uom_categ_id.id,
    #         'active': True,
    #         'uom_type': 'reference',
    #     })
    #     product_id=product_obj.create({
    #         'name': self.product_name,
    #         'uom_id': uom_id.id,
    #         'uos_id': uom_id.id,
    #         'uom_po_id': uom_id.id,
    #
    #     })
    #     return True
class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    uom_ids = fields.One2many(comodel_name="product.uom", inverse_name="product_id", string="Product Uom", required=False, )

class Product_Uom(models.Model):
    _inherit = 'product.uom'
    # generate_id = fields.Many2one(comodel_name="product.generato", string="", required=False,)
    product_id = fields.Many2one(comodel_name="product.template", string="Product Id", required=False, )
