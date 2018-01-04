from odoo import models, fields

class saleOrder(models.Model):
    _inherit = 'sale.order'

    print_type = fields.Selection(
        string="Print type",
        selection=[
                ('catalogue', 'Catalogue'),
                ('proposal', 'Proposal'),
            ],
        default='proposal',
    )


class productTemplate(models.Model):
    _inherit = 'product.template'

    desc_catalog = fields.Text(string="Catalogue Description", )
    desc_proposal = fields.Text(string="Proposal Description", )
