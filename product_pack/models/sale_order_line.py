# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import  float_compare



class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # Fields for sale order pack
    pack_total = fields.Float(
        string='Pack total',
        compute='_get_pack_total'
        )
    pack_total_price = fields.Float(
        string='Pack Unit Price',
        )
    pack_line_ids = fields.One2many(
        'sale.order.line.pack.line',
        'order_line_id',
        'Pack Lines'
        )
    pack_type = fields.Selection(
        related='product_id.pack_price_type',
        readonly=True
        )

    # Fields for common packs
    pack_depth = fields.Integer(
        'Depth',
        help='Depth of the product if it is part of a pack.'
    )
    pack_parent_line_id = fields.Many2one(
        'sale.order.line',
        'Pack',
        help='The pack that contains this product.',
        ondelete="cascade",
        # copy=False,
    )
    pack_child_line_ids = fields.One2many(
        'sale.order.line',
        'pack_parent_line_id',
        'Lines in pack'
    )

    @api.one
    @api.constrains('product_id', 'price_unit', 'product_uom_qty')
    def expand_pack_line(self):
        detailed_packs = ['components_price', 'totalice_price', 'fixed_price']
        if (
                self.state == 'draft' and
                self.product_id.pack and
                self.pack_type in detailed_packs):
            for subline in self.product_id.pack_line_ids:
                vals = subline.get_sale_order_line_vals(
                    self, self.order_id)
                vals['sequence'] = self.sequence
                existing_subline = self.search([
                    ('product_id', '=', subline.product_id.id),
                    ('pack_parent_line_id', '=', self.id),
                    ], limit=1)
                # if subline already exists we update, if not we create
                if existing_subline:
                    existing_subline.write(vals)
                else:
                    self.create(vals)

    @api.multi
    def button_save_data(self):
        return True

    @api.multi
    def action_pack_detail(self):
        view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'product_pack.view_order_line_form2')
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': self.id,
            'context': self.env.context
        }
        return view

    @api.one
    @api.depends(
        'pack_line_ids',
        'pack_line_ids.price_subtotal',
    )
    def _get_pack_total(self):
        pack_total = 0.0
        if self.pack_line_ids:
            pack_total = sum(x.price_subtotal for x in self.pack_line_ids)
        self.pack_total = pack_total

    @api.one
    @api.onchange('pack_total')
    def _onchange_pack_line_ids(self):

        self.price_unit = self.pack_total

    @api.constrains('product_id')
    def expand_none_detailed_pack(self):
        if self.product_id.pack_price_type in [
            'totalice_price',
            'none_detailed_totaliced_price',
            'none_detailed_assited_price']:
            # remove previus existing lines
            self.pack_line_ids.unlink()


            # create a sale pack line for each product pack line
            for pack_line in self.product_id.pack_line_ids:
                price_unit = pack_line.product_id.lst_price
                quantity = pack_line.quantity
                vals = {
                    'order_line_id': self.id,
                    'product_id': pack_line.product_id.id,
                    'product_uom_qty': quantity,
                    'price_unit': price_unit,
                    'discount': pack_line.discount,
                    'price_subtotal': price_unit * quantity,
                    }
                self.pack_line_ids.create(vals)

    # @api.multi
    # def get_sale_order_line_price(self, pack_line):
    #     self.ensure_one()
    #     # if self.product_id.pack_price_type == 'totalice_price':
    #     for subline in pack_line.product_id.pack_line_ids:
    #         price += self.get_sale_order_line_price(subline)
    #
    #     price = 0.0
    #     subproduct = pack_line.product_id
    #     order = self.order_id
    #     qty = pack_line.quantity * self.product_uom_qty
    #     pricelist = order.pricelist_id.id
    #     price = self.env['product.pricelist'].price_get(subproduct.id, quantity, order.partner_id.id)[pricelist]
    #
    #     return price

    @api.constrains('product_id')
    def totalice_price(self):
        if self.product_id.pack_price_type in [
            'totalice_price',
            'none_detailed_totaliced_price',
            'none_detailed_assited_price']:

            order = self.order_id
            pricelist = order.pricelist_id.id
            self.product_id.product_tmpl_id.set_pack_price()

            self.pack_total_price = self.env['product.pricelist'].price_get(
                self.product_id.id, self.product_uom_qty,
                self.order_id.partner_id.id)[pricelist]

    def remove_line_price_from_root_pack(self, amount, qty):
        for line in self:
            if line.pack_parent_line_id:
                line.pack_parent_line_id.remove_line_price_from_root_pack(amount,qty)
            if not line.pack_parent_line_id and line.product_id.pack_price_type == 'totalice_price':
                line.price_unit -= (qty * amount) / line.product_uom_qty
                line.total_line -= qty * amount
                line.price_subtotal -= qty * amount * ( 1 - (line.discount / 100))

    @api.multi
    def unlink(self):
        for line in self:
            if line.filtered(lambda x: x.state in ('sale', 'done')):
                raise UserError(_('You can not remove a sale order line.\n\Discard changes and try setting the quantity to 0.'))
            line.pack_parent_line_id and line.pack_parent_line_id.remove_line_price_from_root_pack(line.pack_total_price, line.product_uom_qty)
        return super(sale_order_line, self).unlink()
