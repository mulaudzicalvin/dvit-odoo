
from odoo import models, fields, api,_
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    last_purchase_price = fields.Float(string="Last purchase price")

class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    @api.multi
    def action_invoice_open(self):
        for inv in self:
            for line in inv.invoice_line_ids:
                #TODO: what about currency ?!!
                unit_price = line.price_unit
                company_currency = inv.company_id.currency_id
                if inv.currency_id != company_currency:
                    unit_price = inv.currency_id.with_context(
                    date=inv._get_currency_rate_date()).compute(
                    abs(unit_price), inv.company_id.currency_id)
                line.product_id.product_tmpl_id.last_purchase_price = unit_price
            res = super(AccountInvoice,self).action_invoice_open()
        return res

class PriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    base = fields.Selection(selection_add=[('last_purchase_price','Last purchase price')])
