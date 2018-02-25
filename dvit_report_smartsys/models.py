from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_optional = fields.Boolean(string="Optional", copy=True)

    @api.constrains('is_optional')
    def _onchange_optional(self):
        for line in self.pack_child_line_ids:
            line.is_optional = self.is_optional

    @api.multi
    def update_pack_line_total(self):
        for line in self:
            if line.is_optional:
                continue
            line.price_unit = line.get_line_total()
            if line.pack_parent_line_id:
                line.price_unit = 0.0

    def get_line_total(self):
        total = 0.0
        for child in self.pack_child_line_ids:
            if child.is_optional:
                continue
            child.pack_depth = child.pack_parent_line_id.pack_depth +1
            child.price_unit = 0.0
            total += child.get_line_total()
        if not self.pack_child_line_ids:
            if self.is_optional:
                return 0.0
            total += self.product_uom_qty * self.product_id.list_price
            self.price_unit = 0.0

        return total

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_type = fields.Selection(
        string="Print type",
        selection=[
                ('catalogue', 'Catalogue'),
                ('proposal', 'Proposal'),
            ],
        default='proposal',
    )

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line.filtered(lambda l: not l.is_optional) :
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('order_line.total_line')
    def _total_all(self):
        for order in self:
            tot_all = 0.0
            for line in order.order_line.filtered(lambda l: not l.is_optional):
                tot_all += line.total_line
            order.total_b4_disc = tot_all

class productTemplate(models.Model):
    _inherit = 'product.template'

    desc_catalog = fields.Text(string="Catalogue Description", )
    desc_proposal = fields.Text(string="Proposal Description", )
