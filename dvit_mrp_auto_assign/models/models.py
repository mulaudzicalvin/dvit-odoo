# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        if production.product_id.product_tmpl_id.product_manager:
          production.user_id = production.product_id.product_tmpl_id.product_manager
        return production
