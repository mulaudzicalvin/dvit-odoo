
from odoo import models, fields, api
from odoo.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class pos_session(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def action_pos_session_closing_control(self):
        po_obj = self.env['pos.order']
        aml_obj = self.env['account.move.line']

        # Call regular function
        res = super(pos_session, self).action_pos_session_close()

        # Get All Pos Order invoiced during the current Sessions
        po_ids = po_obj.search([
            ('session_id', 'in', self.ids),
            ('invoice_id', '!=', False),
        ])
        for po in po_ids:
            # We're searching only account Invoices that has been payed
            # In Point Of Sale
            #if not po.invoice_id.forbid_payment:
            #    continue

            # Search all move Line to reconcile in Sale Journal
            aml_sale_ids = []
            aml_sale_total = 0
            # did't find line_id and replaced it with line_ids
            for aml in po.invoice_id.move_id.line_ids:
                if (aml.partner_id.id == po.partner_id.commercial_partner_id.id and
                        aml.account_id.internal_type == 'receivable'):
                    aml_sale_ids.append(aml.id)
                    aml_sale_total += aml.debit - aml.credit

            aml_payment_ids = []
            aml_payment_total = 0
            # Search all move Line to reconcile in Payment Journals
            abs_ids = list(set([x.statement_id.id for x in po.statement_ids]))
            aml_ids = aml_obj.search([
                ('statement_id', 'in', abs_ids),
                ('partner_id', '=', po.partner_id.commercial_partner_id.id),
                # did't find reconcile_id and replaced it with full_reconcile_id
                ('full_reconcile_id', '=', False)])
            for aml in aml_obj.browse(
                    aml_ids._ids):
                # type -> user_type_id
                if (aml.account_id.internal_type == 'receivable'):
                    aml_payment_ids.append(aml.id)
                    aml_payment_total += aml.debit - aml.credit

            # Try to reconcile
            if aml_payment_total != - aml_sale_total:
                # Unable to reconcile
                _logger.warning(
                    "Unable to reconcile the payment of %s #%s."
                    "(partner : %s)" % (
                        po.name, po.id, po.partner_id.name))
            else:
                # TypeError: reconcile() takes at most 3 arguments (6 given) [FIXED]
                aml_all_ids = aml_payment_ids + aml_sale_ids
                aml_obj.browse(aml_all_ids).reconcile()
        return res