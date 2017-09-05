# -*- coding: utf-8 -*-

from odoo import models, fields, api

class stock_picking_invoiced(models.Model):
    _inherit='stock.picking'
    invoice_state = fields.Selection(string="Invoice Control",
        selection=[('invoiced', 'Invoiced'), 
        ('2binvoiced', 'To Be Invoiced'),
        ('none', 'Not Applicable'), ],  default='none')
    invoice_ids = fields.One2many('account.invoice', 'picking_id', 'Related invoices', readonly=True)
    account_invoice_id = fields.Many2one('account.invoice', string="Account Invoice",readonly=True )

    @api.multi
    def create_invoice(self):
        partner = self.env['res.partner']
        invoice_obj = self.env['account.invoice']
        invoice = self.env['account.invoice']

        i_line_obj = self.env['account.invoice.line']
        sale_journal = self.env['account.journal'].search([('type','=','sale')])[0]
        sale_journal_id = sale_journal.id
        sale_account_id = sale_journal.default_debit_account_id.id if sale_journal.default_debit_account_id \
            else sale_journal.default_credit_account_id.id
        purch_journal = self.env['account.journal'].search([('type','=','purchase')])[0]
        purch_journal_id = purch_journal.id
        purch_account_id = purch_journal.default_debit_account_id.id if purch_journal.default_debit_account_id \
            else purch_journal.default_credit_account_id.id


        for obj in self:
            if obj.location_dest_id.usage == 'supplier':
                global inv_id
                inv_id= invoice_obj.create({
                            'partner_id':obj.partner_id.id,
                            'picking_id': self.id,
                            'date_invoice':obj.min_date,
                            'origin':obj.name,
                            'type':'in_invoice',
                            'journal_id':purch_journal_id,
                            'account_id': obj.partner_id.property_account_payable_id.id,

                 })
                # obj.invoice_ids += inv_id
                for i in obj.move_lines:
                    quan= -i.product_uom_qty
                    i_line_id = i_line_obj.create({
                            'invoice_id':inv_id.id,
                            'product_id':i.product_id.id,
                            'price_unit':i.product_id.standard_price,
                            'name':i.name,
                            'account_id':i.product_id.property_account_expense_id.id,
                            'quantity':quan,

                        })

            elif obj.location_id.usage == 'supplier':
                    inv_id= invoice_obj.create({
                                'partner_id':obj.partner_id.id,
                                'picking_id': self.id,
                                'date_invoice':obj.min_date,
                                'type':'in_invoice',
                                'journal_id':purch_journal_id,
                                'account_id': obj.partner_id.property_account_payable_id.id,
                            })
                    # obj.invoice_ids += inv_id
                    for i in obj.move_lines:
                         i_line_id = i_line_obj.create({
                                    'invoice_id':inv_id.id,
                                    'product_id':i.product_id.id,
                                    'price_unit':i.product_id.standard_price,
                                    'name':i.name,
                                    'account_id':i.product_id.property_account_expense_id.id,
                                    'quantity':i.product_uom_qty,

                                })


            elif obj.location_id.usage == 'customer':
                inv_id= invoice_obj.create({
                            'partner_id':obj.partner_id.id,
                            'picking_id': self.id,
                            'date_invoice':obj.min_date,
                            'type':'out_invoice',
                            'journal_id':sale_journal_id,
                            'account_id': obj.partner_id.property_account_receivable_id.id,
                        })
                # obj.invoice_ids += inv_id
                for i in obj.move_lines:
                     quan= -i.product_uom_qty
                     i_line_id = i_line_obj.create({
                                'invoice_id':inv_id.id,
                                'product_id':i.product_id.id,
                                'price_unit':i.product_id.lst_price,
                                'name':i.name,
                                'account_id':i.product_id.property_account_income_id.id,
                                'quantity':quan,

                            })


            elif obj.location_dest_id.usage == 'customer':
                inv_id= invoice_obj.create({
                            'partner_id':obj.partner_id.id,
                            'picking_id': self.id,
                            'date_invoice':obj.min_date,
                            'type':'out_invoice',
                            'journal_id':sale_journal_id,
                            'account_id': obj.partner_id.property_account_receivable_id.id,
                        })
                # obj.invoice_ids += inv_id
                for i in obj.move_lines:
                     i_line_id = i_line_obj.create({
                                'invoice_id':inv_id.id,
                                'product_id':i.product_id.id,
                                'price_unit':i.product_id.lst_price,
                                'name':i.name,
                                'account_id':i.product_id.property_account_income_id.id,
                                'quantity':i.product_uom_qty,

                            })

            else:
                break


            if inv_id and i_line_id:
                obj.write({'invoice_state':'invoiced'})

            self.account_invoice_id= inv_id.id

class AccountInvoice(models.Model):
    _inherit='account.invoice'
    picking_id = fields.Many2one('stock.picking','Picking invoice',readonly=True)
