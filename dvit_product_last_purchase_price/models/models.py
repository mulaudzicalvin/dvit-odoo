
from odoo import models, fields, api,_
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class dvit_purchase_price(models.Model):
    # _name = 'dvit_purchase_price.dvit_purchase_price'
    _inherit = ['product.template']
    last_purchase_price = fields.Float(string="Last purchase price")

class account_invoice(models.Model):
    _inherit = ['account.invoice']

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
            raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        products=self.env['product.product']
        for line in self.invoice_line_ids:
            product=products.browse(line.product_id.id)
            product.product_tmpl_id.last_purchase_price=line.price_unit
        return to_open_invoices.invoice_validate()

class PriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    base = fields.Selection(selection_add=[('last_purchase_price','Last purchase price')])
