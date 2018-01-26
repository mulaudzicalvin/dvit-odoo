# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location', readonly="1")

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations')

    @api.multi
    def tgl_restrict(self):
        self.restrict_locations = not self.restrict_locations
        model_data = self.env['ir.model.data']
        res_groups = self.env['res.groups']
        restrict_group = model_data.search([('name', '=', 'stock_restrictions_group')]).res_id
        current_group=res_groups.browse(restrict_group)
        if self.restrict_locations:
            current_group=res_groups.browse(restrict_group)
            current_group.write({'users':  [(4, self.id)]})
            self.groups_id =[(4, restrict_group)]
        else:
            current_group.write({'users':  [(3, self.id)]})

# Removed as we use rules to restrict access
# class stock_move(models.Model):
#     _inherit = 'stock.move'
#
#     @api.one
#     @api.constrains('state', 'location_id', 'location_dest_id')
#     def check_user_location_rights(self):
#         if self.state == 'draft':
#             return True
#         user_locations = self.env.user.stock_location_ids
#         if self.env.user.restrict_locations:
#             message = _(
#                 'Invalid Location. You cannot process this move since you do '
#                 'not control the location "%s". '
#                 'Please contact your Adminstrator.')
#             if self.location_id not in user_locations:
#                 raise Warning(message % self.location_id.name)
#             elif self.location_dest_id not in user_locations:
#                 raise Warning(message % self.location_dest_id.name)
