from openerp import models, fields, api

class SaleOrder(models.Model):
      _inherit="sale.order"
      presale = fields.Many2one('res.users', string="Pre-sale", store=True)
      approved_by = fields.Many2one('res.users', string='approved by', store=True)

      approve_phone = fields.Char(string="Phone", required=False, store=True)
      approve_email = fields.Char(string="email", required=False, store=True)
      approve_mobile = fields.Char(string="mobile", required=False, store=True)
      approve_name = fields.Char(string="name", required=False, store=True)
      approve_fax = fields.Char(string="Fax", store=True)

      presale_phone = fields.Char(string="Presale phone", required=False, store=True)
      presale_mobile = fields.Char(string="Presale mobile", required=False, store=True)
      presale_fax = fields.Char(string="Presale Fax", required=False, store=True)
      presale_name = fields.Char(string="Presale name", required=False, store=True)
      presale_email = fields.Char(string="Presale email", required=False, store=True)

      sale_phone = fields.Char(string="sales person phone", required=False, store=True)
      sale_mobile = fields.Char(string="sales person mobile", required=False, store=True)
      sale_fax = fields.Char(string="sales person Fax", required=False, store=True)
      sale_name = fields.Char(string="sales person name", required=False, store=True)
      sale_email = fields.Char(string="sales person email", required=False, store=True)

      @api.onchange('approved_by')
      def _onchange_employee_id(self):
        self.approve_phone = self.approved_by.partner_id.phone
        self.approve_email = self.approved_by.partner_id.email
        self.approve_mobile = self.approved_by.partner_id.mobile
        self.approve_name = self.approved_by.partner_id.name
        self.approve_fax = self.approved_by.partner_id.fax
      @api.onchange('presale')
      def _onchange_id(self):
        self.presale_phone = self.presale.partner_id.phone
        self.presale_mobile = self.presale.partner_id.mobile
        self.presale_fax = self.presale.partner_id.fax
        self.presale_name = self.presale.partner_id.name
        self.presale_email = self.presale.partner_id.email

      @api.onchange('user_id')
      def _onchange_user_id(self):
        self.sale_phone = self.user_id.partner_id.phone
        self.sale_mobile = self.user_id.partner_id.mobile
        self.sale_fax = self.user_id.partner_id.fax
        self.sale_name = self.user_id.partner_id.name
        self.sale_email = self.user_id.partner_id.email

