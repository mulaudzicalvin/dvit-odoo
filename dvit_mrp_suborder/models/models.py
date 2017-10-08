# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    subproduction_ids = fields.Many2many(
        string="Suborders",
        comodel_name="mrp.production",
        relation="rel_mrp_subproduction",
        column1="parent_id",
        column2="child_id",
    )
