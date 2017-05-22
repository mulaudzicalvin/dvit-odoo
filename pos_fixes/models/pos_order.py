from openerp import models, fields, api
from openerp.tools.float_utils import float_round as round


class pos_order(models.Model):
    _inherit = "pos.order"

    '''This code will complete the anglo-saxon STJ entries
        in COGS / Stock accounts per order, plz
        keep in mind that this module depends on the product_pack
        created by IngAdhoc to process packs also'''

    def create_picking(self, cr, uid, ids, context=None):
        super(pos_order, self).create_picking(cr,
                                              uid, ids,
                                              context=context)

        pos_order_obj = self.pool.get('pos.order')
        account_move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        company_id = self.pool.get('res.users').browse(cr, uid,
                                                       uid, context=context).company_id.id

        for order in self.browse(cr, uid, ids, context=context):
            session = order.session_id
            # if move_id is None:
            # Create an entry for the sale
            move_id = pos_order_obj._create_account_move(cr,
                                                         uid,
                                                         session.start_at,
                                                         session.name,
                                                         session.config_id.journal_id.id,
                                                         company_id,
                                                         context=context)

            move = account_move_obj.browse(cr, uid,
                                           move_id, context=context)

            amount_total = order.amount_total

            for o_line in order.lines:
                amount = 0

                if o_line.product_id.type != 'service' and \
                        o_line.product_id.valuation == 'real_time':
                    stkacc = o_line.product_id.property_stock_account_output and \
                        o_line.product_id.property_stock_account_output
                    if not stkacc:
                        stkacc = o_line.product_id.categ_id.property_stock_account_output_categ and \
                            o_line.product_id.categ_id.property_stock_account_output_categ

                    # cost of goods account cogacc
                    cogacc = o_line.product_id.property_account_expense and \
                        o_line.product_id.property_account_expense
                    if not cogacc:
                        cogacc = o_line.product_id.categ_id.property_account_expense_categ and \
                            o_line.product_id.categ_id.property_account_expense_categ
                    amount = o_line.qty * o_line.product_id.standard_price
                    line_vals = {
                        'period_id': move.period_id.id,
                        'name': o_line.product_id.name,
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
                        move_line_obj.create(cr, uid, caml)
                        move_line_obj.create(cr, uid, daml)

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
                        move_line_obj.create(cr, uid, caml)
                        move_line_obj.create(cr, uid, daml)

                '''Due to the Pack nature we need to process it separately'''
                if hasattr(o_line.product_id, 'pack'):
                    if o_line.product_id.pack:
                        for pack_line in o_line.product_id.pack_line_ids:
                            if pack_line.product_id.type != 'service' and \
                                    pack_line.product_id.valuation == 'real_time':
                                stkacc = pack_line.product_id.property_stock_account_output and \
                                    pack_line.product_id.property_stock_account_output
                                if not stkacc:
                                    stkacc = pack_line.product_id.categ_id.property_stock_account_output_categ and \
                                        pack_line.product_id.categ_id.property_stock_account_output_categ
                                cogacc = pack_line.product_id.property_account_expense and \
                                    pack_line.product_id.property_account_expense
                                if not cogacc:
                                    cogacc = pack_line.product_id.categ_id.property_account_expense_categ and \
                                        pack_line.product_id.categ_id.property_account_expense_categ
                                amount = o_line.qty * pack_line.quantity * pack_line.product_id.standard_price #TODO covert UoS/UoM
                                if cogacc and stkacc:
                                    line_vals = {
                                        'period_id': move.period_id.id,
                                        'name': pack_line.product_id.name,
                                        'move_id': move_id,
                                        'journal_id': move.journal_id.id,
                                        'date': move.date,
                                        'product_id': pack_line.product_id.id,
                                        'partner_id': order.partner_id and order.partner_id.id or False,
                                        'quantity': pack_line.quantity * o_line.qty,
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
                                        move_line_obj.create(
                                            cr, uid, caml)
                                        move_line_obj.create(
                                            cr, uid, daml)

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
                                        move_line_obj.create(
                                            cr, uid, caml)
                                        move_line_obj.create(
                                            cr, uid, daml)

        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
