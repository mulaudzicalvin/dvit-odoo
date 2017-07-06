# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    total_amount_in_words = fields.Char(string="Amount in Words", store=True)

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        res = super(AccountInvoice,self)._compute_amount()
        supported_langs = ['ar','en','fr','de','dk','ru','he','id','lt','lv','no','pl']
        lang = self.partner_id and self.partner_id.lang[:2]
        if not lang in supported_langs:
            lang = 'en'
        self.total_amount_in_words = num2words(self.amount_total,lang=lang)
        # print "-------------------------------"
        # print self.total_amount_in_words
        # print "-------------------------------"
        return res
