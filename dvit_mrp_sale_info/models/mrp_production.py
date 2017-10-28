# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_id = fields.Many2one(
        'sale.order', string='Sale order', readonly=True, store=True,
        compute='get_sale_info')
    partner_id = fields.Many2one(related='sale_id.partner_id',
                                 string='Customer', store=True)

    @api.depends('move_raw_ids.state','move_finished_ids.state',
    'move_raw_ids','move_finished_ids')
    def get_sale_info(self):
        for prod in self:
            if not prod.move_finished_ids:
                continue
            prod.update({
            'sale_id': prod.move_finished_ids[0].move_dest_id.picking_id.sale_id,
            })
