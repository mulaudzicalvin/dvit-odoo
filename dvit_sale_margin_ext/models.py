from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    purchase_price = fields.Float('Cost Price', digits_compute= dp.get_precision('Product Price'), store=True)

class sale_order(models.Model):
    _inherit = "sale.order"
    total_cost = fields.Float("Total Cost", compute='_get_total_cost', store=True)

    @api.one
    @api.depends('order_line')
    def _get_total_cost(self):
        for order in self:
            for line in order.order_line:
                order.total_cost += line.purchase_price * line.product_uom_qty
