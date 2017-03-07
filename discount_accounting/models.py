# # -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from openerp import models, fields, api


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):
        cr = self.env.cr
        uid = self.env.user.id
        context = self._context
        move = self.move_id
        journal_id = move.journal_id
        update_posted_orig = journal_id.update_posted
        journal_id.update_posted = True
        move.button_cancel()
        inv_id = self.id
        # sales_journal_id = self.journal_id.id
        account_defaults = self.pool.get("discount.account_config").browse(cr, uid, 1)
        sale_account = journal_id.default_debit_account_id
        line_id_vals = []
        record_disount = 0
        for ol in self.invoice_line:
            record_disount += (ol.discount / 100) * ol.price_unit * ol.quantity
        if self.type == "out_invoice":
            sale_account = self.journal_id.default_credit_account_id.id
            line_id_vals += self.env['account.move.line'].create(
                {"name": "sale discount",
                "account_id": sale_account,
                "credit": record_disount,
                "date": self.date_due,
                "journal_id": self.journal_id.id,
                "partner_id": self.partner_id.id,
                "period_id": self.period_id.id,
                "move_id": move.id},context = context)
            line_id_vals += self.env['account.move.line'].create({
                "name": "discount",
                "account_id": account_defaults.sale_discount_account.id,
                "debit": record_disount,
                "date": self.date_due,
                "journal_id": self.journal_id.id,
                "partner_id": self.partner_id.id,
                "period_id": self.period_id.id,
                "move_id": move.id}
                ,context = context)
        elif self.type == "out_refund":
            sale_account = self.journal_id.default_debit_account_id.id
            line_id_vals = self.env['account.move.line'].create(
                {"name": "sale discount refund",
                "account_id": sale_account,
                "debit": record_disount,
                "date": self.date_due,
                "journal_id": self.journal_id.id,
                "partner_id": self.partner_id.id,
                "period_id": self.period_id.id,
                "move_id": move.id},
                context = context)
            line_id_vals += self.env['account.move.line'].create({
                "name": "discount",
                "account_id": account_defaults.sale_discount_account.id,
                "credit": record_disount,
                "date": self.date_due,
                "journal_id": self.journal_id.id,
                "partner_id": self.partner_id.id,
                "period_id": self.period_id.id,
                "move_id": move.id},
                context = context)
            journal_id.update_posted = update_posted_orig
        super(account_invoice, self).invoice_validate()
        move.button_validate()

class account_config_settings(models.Model):
    _inherit = "account.config.settings"

    @api.multi
    def open_discount_accounting_form(self):
        discount_from = self.env.ref('discount_accounting.view_discount_account_config_installer', False)
        return {
            'name': 'Discount Accounting Config',
            'type': 'ir.actions.act_window',
            'res_model': 'discount.account_config',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'views': [(discount_from.id, 'form')],
            'view_id': 'discount_from.id',
            'flags': {},
            'res_id': 1,
            'id': 1,
        }
class discount_accounting_config(models.Model):

    _name = 'discount.account_config'

    sale_discount_account = fields.Many2one(
        'account.account',
        string="Default Discount Account",
        domain="[('type', '!=', 'view')]",)

    @api.multi
    def save(self):
        return {'type': 'ir.actions.act_window_close'}

#
# from openerp import models, fields, api
#
#
# class account_invoice(models.Model):
# 	_inherit = "account.invoice"
#
# 	@api.multi
# 	def invoice_validate(self):
# 		cr = self.env.cr
# 		uid = self.env.user.id
# 		context = self._context
# 		move = self.env['account.move'].create({"journal_id": self.journal_id.id,
# 			"name": self.move_id.name,
# 			"ref": self.move_id.ref,
# 			"partner_id": self.partner_id.id})
# 		super(account_invoice, self).invoice_validate()
# 		sales_journal_id = 0
# 		inv = self.id
# 		sales_journal_id = self.journal_id.id
# 		account_defaults = self.pool.get("discount.account_config").browse(cr, uid, 1)
# 		sale_account = 0
# 		line_id_vals = []
# 		record_disount = 0
# 		for ol in self.invoice_line:
# 			record_disount += (ol.discount / 100) * ol.price_unit * ol.quantity
# 		if self.type == "out_invoice":
# 			sale_account = self.journal_id.default_debit_account_id.id
# 			line_id_vals = self.env['account.move.line'].create({"name": "discount sale",
# 				"account_id": sale_account,
# 				"credit": record_disount,
# 				"date": self.date_due,
# 				"journal_id": self.journal_id.id,
# 				"partner_id": self.partner_id.id,
# 				"period_id": self.period_id.id,
# 				"move_id": move.id},context = context) + self.env['account.move.line'].create({
# 				"name": "discount",
# 				"account_id": account_defaults.sale_discount_account.id,
# 				"debit": record_disount,
# 				"date": self.date_due,
# 				"journal_id": self.journal_id.id,
# 				"partner_id": self.partner_id.id,
# 				"period_id": self.period_id.id,
# 				"move_id": move.id},context = context)
# 		elif self.type == "out_refund":
# 			sale_account = self.journal_id.default_debit_account_id.id
# 			line_id_vals = self.env['account.move.line'].create({"name": "discount sale",
# 				"account_id": sale_account,
# 				"debit": record_disount,
# 				"date": self.date_due,
# 				"journal_id": self.journal_id.id,
# 				"partner_id": self.partner_id.id,
# 				"period_id": self.period_id.id,
# 				"move_id": move.id},context = context) + self.env['account.move.line'].create({
# 				"name": "discount",
# 				"account_id": account_defaults.sale_discount_account.id,
# 				"credit": record_disount,
# 				"date": self.date_due,
# 				"journal_id": self.journal_id.id,
# 				"partner_id": self.partner_id.id,
# 				"period_id": self.period_id.id,
# 				"move_id": move.id},context = context)
# 		move.post()
#
# class account_config_settings(models.Model):
# 	_inherit = "account.config.settings"
#
# 	@api.multi
# 	def open_discount_accounting_form(self):
# 		discount_from = self.env.ref('discount_accounting.view_discount_account_config_installer', False)
# 		return {
# 			'name': 'Discount Accounting Config',
# 			'type': 'ir.actions.act_window',
# 			'res_model': 'discount.account_config',
# 			'view_type': 'form',
# 			'view_mode': 'form',
# 			'target': 'new',
# 			'views': [(discount_from.id, 'form')],
# 			'view_id': 'discount_from.id',
# 			'flags': {},
# 			'res_id': 1,
# 			'id': 1,
# 		}
# class discount_accounting_config(models.Model):
#
# 	_name = 'discount.account_config'
#
# 	sale_discount_account = fields.Many2one(
# 		'account.account',
# 		string="Default Discount Account",
# 		domain="[('type', '!=', 'view')]",)
#
# 	@api.multi
# 	def save(self):
# 		return {'type': 'ir.actions.act_window_close'}
