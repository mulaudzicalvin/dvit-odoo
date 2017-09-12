# -*- coding: utf-8 -*-

from odoo import models, fields, api

class stock_picking_invoiced(models.Model):
    _inherit='stock.picking'
    invoice_state = fields.Selection(string="Invoice Control",
        selection=[('invoiced', 'Invoiced'), 
        ('2binvoiced', 'To Be Invoiced'),
        ('none', 'Not Applicable'), ],  default='none')
    invoice_id = fields.Many2one('account.invoice', string="Account Invoice",readonly=True )

    @api.multi
    def create_invoice(self):
        invoice_obj = self.env['account.invoice']
        i_line_obj = self.env['account.invoice.line']
        sale_journal = self.env['account.journal'].search([('type','=','sale')])[0]
        sale_journal_id = sale_journal.id
        purch_journal = self.env['account.journal'].search([('type','=','purchase')])[0]
        purch_journal_id = purch_journal.id


        for obj in self:
            # Vendor Refund
            if obj.location_dest_id.usage == 'supplier':
                global inv_id
                inv_id= invoice_obj.create({
                    'partner_id':obj.partner_id.id,
                    'picking_id': self.id,
                    'date_invoice':obj.min_date,
                    'origin':obj.name,
                    'type':'in_refund',
                    'journal_id':purch_journal_id,
                    'account_id': obj.partner_id.property_account_payable_id.id,
                 })
                for i in obj.move_lines:
                    accounts = i.product_id.product_tmpl_id.get_product_accounts()
                    price_unit = i.product_id.uom_id._compute_price(i.product_id.standard_price, i.product_uom)
                    i_line_id = i_line_obj.create({
                    'invoice_id':inv_id.id,
                    'product_id':i.product_id.id,
                    'price_unit': price_unit,
                    'name':i.name,
                    'account_id': accounts.get('stock_input') and accounts['stock_input'].id or \
                                  accounts['expense'].id,
                    'quantity':i.product_uom_qty,
                    'uom_id':i.product_uom.id,
                    })
            # Vendor Invoice
            elif obj.location_id.usage == 'supplier':
                    inv_id= invoice_obj.create({
                        'partner_id':obj.partner_id.id,
                        'picking_id': self.id,
                        'date_invoice':obj.min_date,
                        'type':'in_invoice',
                        'journal_id':purch_journal_id,
                        'account_id': obj.partner_id.property_account_payable_id.id,
                            })
                    for i in obj.move_lines:
                        accounts = i.product_id.product_tmpl_id.get_product_accounts()
                        price_unit = i.product_id.uom_id._compute_price(i.product_id.standard_price, i.product_uom)
                        i_line_id = i_line_obj.create({
                        'invoice_id':inv_id.id,
                        'product_id':i.product_id.id,
                        'price_unit': price_unit,
                        'name':i.name,
                        'account_id':accounts.get('stock_input') and accounts['stock_input'].id or accounts['expense'].id,
                        'quantity':i.product_uom_qty,
                        'uom_id':i.product_uom.id,
                        })

            # Customer Refund
            elif obj.location_id.usage == 'customer':
                inv_id= invoice_obj.create({
                    'partner_id':obj.partner_id.id,
                    'picking_id': self.id,
                    'date_invoice':obj.min_date,
                    'type':'out_refund',
                    'journal_id':sale_journal_id,
                    'account_id': obj.partner_id.property_account_receivable_id.id,
                     })
                for i in obj.move_lines:
                    accounts = i.product_id.product_tmpl_id.get_product_accounts()
                    price_unit = i.product_id.uom_id._compute_price(i.product_id.lst_price, i.product_uom)
                    i_line_id = i_line_obj.create({
                        'invoice_id':inv_id.id,
                        'product_id':i.product_id.id,
                        'price_unit':price_unit,
                        'name':i.name,
                        'account_id':accounts.get('income') and accounts['income'].id or False,
                        'quantity':i.product_uom_qty,
                        'uom_id': i.product_uom.id,
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
                for i in obj.move_lines:
                    accounts = i.product_id.product_tmpl_id.get_product_accounts()
                    price_unit = i.product_id.uom_id._compute_price(i.product_id.lst_price, i.product_uom)
                    i_line_id = i_line_obj.create({
                        'invoice_id':inv_id.id,
                        'product_id':i.product_id.id,
                        'price_unit':price_unit,
                        'name':i.name,
                        'account_id':accounts.get('income') and accounts['income'].id or False,
                        'quantity':i.product_uom_qty,
                        'uom_id': i.product_uom.id,
                        })

            else:
                break

            if inv_id and i_line_id:
                obj.write({'invoice_state':'invoiced'})

            self.invoice_id= inv_id.id

class AccountInvoice(models.Model):
    _inherit='account.invoice'
    picking_id = fields.Many2one('stock.picking','Picking invoice',readonly=True)
