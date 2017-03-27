from odoo import models, fields, api
from odoo.tools.float_utils import float_round as round


class PosOrder(models.Model):
    _inherit = "pos.order"

    '''This code will complete the anglo-saxon STJ entries
        in COGS / Stock accounts per order'''

    def create_picking(self):
        account_move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        for order in self:

            ao_lines = order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu']) #and \
            for ao_line in ao_lines:
                print('------------POSFIX --- ' + str(ao_line.id) + str(ao_line.name) + ' -----------')
            o_lines = ao_lines.filtered(lambda l: l.product_id.categ_id.property_valuation == 'real_time')
            for o_line in o_lines:
                print('------------POSFIX --- ' + str(o_line.id) + str(o_line.name) + ' -----------')
            if o_lines:
                company_id = order.company_id.id
                session = order.session_id
                move = self._create_account_move(session.start_at,
                                                     order.name,
                                                     int(session.config_id.journal_id.id),
                                                     company_id,
                                                     )
                print ('------------ POSFIX --move-name - ' + str(move.name) + ' ------------')

                move_id = move.id
                print ('------------ POSFIX --move-id - ' + str(move_id) + ' ------------')

                # move.write({'narration':'POSFIX'})
                amount_total = order.amount_total

                for o_line in o_lines :
                    print ('------------ POSFIX --- ' + str(o_line.name) + ' ------------')
                    amount = 0
                    # if o_line.product_id.categ_id.property_valuation == 'real_time':
                    stkacc = o_line.product_id.categ_id.property_stock_account_output_categ_id and \
                        o_line.product_id.categ_id.property_stock_account_output_categ_id
                        # cost of goods account cogacc
                    cogacc = o_line.product_id.property_account_expense_id and \
                        o_line.product_id.property_account_expense_id
                    if not cogacc:
                        cogacc = o_line.product_id.categ_id.property_account_expense_categ_id and \
                            o_line.product_id.categ_id.property_account_expense_categ_id

                    amount = o_line.qty * o_line.product_id.standard_price
                    line_vals = {
                        'name': o_line.product_id.name + 'POSFIX',
                        'move_id': move_id,
                        'journal_id': move.journal_id.id,
                        'date': move.date,
                        'product_id': o_line.product_id.id,
                        'partner_id': order.partner_id and order.partner_id.id or False,
                        'quantity': o_line.qty,
                        'ref': o_line.name
                    }

                    if amount_total > 0:
                            # create move.lines to credit stock and
                            # debit cogs
                        caml = {
                            'account_id': stkacc.id,
                            'credit': amount,
                            'debit': 0.0,
                        }
                        caml.update(line_vals)
                        daml = {
                            'account_id': cogacc.id,
                            'credit': 0.0,
                            'debit': amount,
                        }
                        daml.update(line_vals)
                        move_line_obj.create( caml)
                        move_line_obj.create( daml)

                    if amount_total < 0:
                        # create move.lines to credit cogs and
                        # debit stock
                        caml = {
                            'account_id': cogacc.id,
                            'credit': -amount,
                            'debit': 0.0,
                        }
                        caml.update(line_vals)
                        daml = {
                            'account_id': stkacc.id,
                            'credit': 0.0,
                            'debit': -amount,
                        }
                        daml.update(line_vals)
                        move_line_obj.create( caml)
                        move_line_obj.create( daml)

            else:
                print('---------- NOLINIESPOSFIX ---------')

        super(PosOrder, self).create_picking()
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
