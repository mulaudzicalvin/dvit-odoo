# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResPartner(models.Model):
	_inherit = 'res.partner'
	shipping_company = fields.Boolean(string="Shipping Company?")

class ProductTemplate(models.Model):
	_inherit = 'product.template'
	shipping_service = fields.Boolean(string="Shipping Service?")

class SaleOrder(models.Model):
	_inherit = 'sale.order'
	shipping_company = fields.One2Many(res.partner, string="Delivery Company")
	shipping_service = fields.One2Many(product.template, string='Delivery Service')

	def wkf_confirm(self):
		res = super(SaleOrder,self).wkf_confirm()
		self._create_shipping_cost_entry(shipping_company,shipping_service)

	def _create_shipping_cost_entry(company, service):
		AM = self.env['account.move']
		AML = self.env['account.move.line']
		move = AM.create(cr, uid, .....)
		dr_line = AML.create(cr, uid, move.id, service.expense_account.id, ....)
		cr_line = AML.create(cr, uid, move.id, company.property_account_payaple.id, ....)

