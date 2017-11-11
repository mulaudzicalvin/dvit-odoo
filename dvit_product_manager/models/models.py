# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    product_manager = fields.Many2one('res.users', string='Product Manager')
