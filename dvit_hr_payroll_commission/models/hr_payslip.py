# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # ---------- Fields management
    invoice_ids = fields.Many2many('account.invoice', string='Invoices')
    move_line_ids = fields.Many2many('account.move.line', string='Journal Items')

    # ---------- Utilities
    @api.multi
    def _detach_invoices_from_payslip(self):
        # for each invoice that have self.id in slip_ids set slip_ids -= self.id
        for slip in self:
            InvoiceObj = self.env['account.invoice']
            invoices = InvoiceObj.search([('slip_ids', 'in', self.ids)])
            for inv in invoices:
                inv.slip_ids -= slip

    @api.multi
    def _detach_move_lines_from_payslip(self):
        for slip in self:
            AccountMoveLineObj = self.env['account.move.line']
            amls = AccountMoveLineObj.search([('slip_ids', 'in', self.ids)])
            for aml in amls:
                aml.slip_ids -= slip

    @api.multi
    def _attach_invoices_to_payslip(self):
        # this module is computing payments not invoices, so search
        # for all user's invoices and do not attach invoices
        for slip in self:
            invoice_ids = slip.contract_id._comp_commission()
        return invoice_ids

    @api.multi
    def _attach_move_lines_to_payslip(self, invoices):
        # for each payment that dont have slip id of current employee; 
        # add self.id to payment.slip_ids
        for slip in self:
            for inv in invoices:
                for payment in inv.payment_ids:
                    if not payment.slip_ids:
                        payment.slip_ids += slip
                    else:
                        uids = []
                        for pslip in payment.slip_ids:
                            uids.append(pslip.employee_id.user_id.id)
                        if slip.employee_id.user_id.id in uids:
                            continue
                        else:
                            # commission += payment.credit
                            payment.slip_ids += slip

    @api.multi
    def compute_sheet(self):
        
        for payslip in self:
            payslip._detach_invoices_from_payslip()
            payslip._detach_move_lines_from_payslip()
            # No contract? forget about it
            if not payslip.contract_id:
                continue
            # update commission on contract
            # payslip.contract_id._comp_commission()

            invoice_ids = payslip.contract_id._comp_commission()
            payslip._attach_move_lines_to_payslip(invoice_ids)

            # update again
            # payslip.contract_id._comp_commission()

        res = super(HrPayslip, self).compute_sheet()

        return res

    @api.multi
    def cancel_sheet(self):
        for slip in self:
            slip._detach_invoices_from_payslip()
            slip._detach_move_lines_from_payslip()
            slip.contract_id._comp_commission()
        return super(HrPayslip, self).cancel_sheet()


    @api.multi
    def unlink(self):
        for slip in self:
            slip._detach_invoices_from_payslip()
            slip._detach_move_lines_from_payslip()
            slip.contract_id._comp_commission()
        return super(HrPayslip, self).unlink()