
from odoo import models, fields, api, _
import datetime
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    tgl_modify = fields.Boolean('Modified', default=False)

    # @api.model
    def f_tgl_modify(self):
        for production in self:
            production.tgl_modify = not self.tgl_modify

    def f_update_order(self):
        for production in self:
            if production.state in ['planned','progress','done']:
                raise UserError(_('You can not update in progress or done orders.'))
                # continue
            # we need to create a temp bom from current config and process it, then delete it
            bom = self.env['mrp.bom']
            bom_line = self.env['mrp.bom.line']
            bom_id = bom.create({
                'active': False, #this is 
                'product_tmpl_id': production.product_tmpl_id.id,
                'product_qty': production.product_qty,
                'product_uom_id': production.product_uom_id.id,
                'routing_id': production.routing_id.id,
                })
            for line in production.move_raw_ids:
                bom_line.create({
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'product_uom_id': line.product_uom.id,
                    'bom_id': bom_id.id,
                    })
            # trigger write on BoM to update product cost if dvit_product_cost_bom_auto is installed
            bom_id.code = 'Auto generated for ' + str(production.name) +' '+ str(fields.Datetime.now())
            #########
            # delete current moves - this is not working if we have some confirmed moves
            for move in production.move_raw_ids:
                move.do_unreserve()
                move.write({'state':'draft'})
                move.action_cancel()
                move.unlink()
            for move in production.move_finished_ids:
                move.action_cancel()
                move.unlink()

            old_bom = production.bom_id
            production.bom_id = bom_id

            # delete old bom_id if auto generated
            if old_bom.code and 'Auto generated' in old_bom.code and str(production.name) in old_bom.code and not old_bom.active:
                old_bom.unlink()

            # then recreate the moves again
            production._generate_moves()
            production.tgl_modify = not self.tgl_modify

    # def button_mark_done(self):
    #     for production in self:
    #         res = super(MrpProduction, self).button_mark_done() 
    #         production.bom_id.unlink()
    #     return res
    