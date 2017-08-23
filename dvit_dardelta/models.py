from openerp import models, fields, api

class mothida(models.Model):
      _inherit="sale.order"
      presale = fields.Many2one(comodel_name="res.users", string="Pre sale",)
      approved_by = fields.Many2one(comodel_name="res.users", string="Approved by",)
