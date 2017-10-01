# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class HrContract(models.Model):
    _inherit = 'hr.contract'
    commission = fields.Float(string='Commission',
                              compute='_comp_commission', store=True)
    comm_rate = fields.Float(string='Commissions Rate',
                             digits=dp.get_precision('Payroll Rate'), store=True)
    comm_type = fields.Selection(string='Commission Type', 
        selection=[('all','All Sales'),('team','Team Sales'),('own','Own sales')],
        default='own',
        help='Sales = His sales only; Team = His team sales only; All = On all sales')

    @api.multi
    @api.depends('employee_id','employee_id.payslip_count')
    @api.onchange('comm_type','employee_id','employee_id.payslip_count')
    def _comp_commission(self):
        for contract in self:
            # ToDo: Fix performance by:
                # calling this function from invoice validate
                # this function shoud get all invoices that has payment_ids which
                # don't have slips or have slip_ids ***not*** related to employee
            invoice_ids = []
            comm_type = contract.comm_type
            contract.commission = 0
            account_invoice_obj = self.env['account.invoice']

            if comm_type == 'own':
                own_invoices = account_invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('user_id', '=', contract.employee_id.user_id.id),
                    ('type', '=', 'out_invoice'),
                ])
                for inv in own_invoices:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for pslip in payment.slip_ids:
                                uids.append(pslip.employee_id.user_id.id)
                        if contract.employee_id.user_id.id not in uids:
                            invoice_ids.append(inv)

            elif comm_type == 'team':
                team_obj = self.env['crm.case.section']
                team_ids = team_obj.search(['|',
                    ('user_id','=',contract.employee_id.user_id.id),
                    ('member_ids','child_of', contract.employee_id.user_id.id)])
                # print "------ team_ids= "+ str(team_ids) + " --------"
                team_invoices = account_invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('type', '=', 'out_invoice'),
                    ('section_id', 'in', [t.id for t in team_ids]),
                    ('date_invoice', '>=', contract.date_start),
                    ])

                for inv in team_invoices:
                    # if inv.section_id in team_ids:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for pslip in payment.slip_ids:
                                uids.append(pslip.employee_id.user_id.id)
                        if contract.employee_id.user_id.id in uids:
                            continue
                        else:
                            invoice_ids.append(inv)

            else: #comm_type = all
                all_invoices = account_invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('type', '=', 'out_invoice'),
                    ('date_invoice', '>=', contract.date_start),
                    ])
                for inv in all_invoices:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for pslip in payment.slip_ids:
                                uids.append(pslip.employee_id.user_id.id)
                        if contract.employee_id.user_id.id in uids:
                            continue
                        else:
                            invoice_ids.append(inv)

            commission = 0
            for inv in invoice_ids:
                for payment in inv.payment_ids:
                    if not payment.slip_ids:
                        commission += payment.credit
                    else:
                        uids = []
                        for pslip in payment.slip_ids:
                            uids.append(pslip.employee_id.user_id.id)
                        if contract.employee_id.user_id.id in uids:
                            continue
                        else:
                            commission += payment.credit

            contract.commission = commission
            return invoice_ids

