
from odoo import models, fields, api, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)

        # old_res = super(StockMove, self)._prepare_account_move_line(
        #     qty, cost, credit_account_id, debit_account_id)

        # dr_line = old_res[0][-1]
        # cr_line = old_res[1][-1]
        # pd_line = old_res[2][-1]

        # stock move generated from MO don't have picking_id nor partner_id
        # find the partner_id from procurement group_id
        if not self.picking_id:
            partner_id = self.group_id.partner_id and \
                self.env['res.partner']._find_accounting_partner(self.group_id.partner_id) or False
            res[0][-1].update({'partner_id': partner_id and partner_id.id})
            res[1][-1].update({'partner_id': partner_id and partner_id.id})
            # res[2][-1].update({'partner_id': partner_id and partner_id.id})

        return res
