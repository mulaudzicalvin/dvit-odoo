# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import Warning
import math


class product_product(models.Model):
    _inherit = 'product.product'

    pack_line_ids = fields.One2many(
        'product.pack.line',
        'parent_product_id',
        'Pack Products',
        help='List of products that are part of this pack.'
        )
    used_pack_line_ids = fields.One2many(
        'product.pack.line',
        'product_id',
        'On Packs',
        help='List of packs where product is used.'
        )

    @api.one
    @api.constrains('pack_line_ids')
    def check_recursion(self):
        """
        Check recursion on packs
        """
        pack_lines = self.pack_line_ids
        while pack_lines:
            if self in pack_lines.mapped('product_id'):
                raise Warning(_(
                    'Error! You cannot create recursive packs.\n'
                    'Product id: %s') % self.id)
            pack_lines = pack_lines.mapped('product_id.pack_line_ids')


class product_template(models.Model):
    _inherit = 'product.template'

    # TODO rename a pack_type
    pack_price_type = fields.Selection([
        ('components_price', 'Detailed - Components Prices'),
        ('totalice_price', 'Detailed - Totaliced Price'),
        ('fixed_price', 'Detailed - Fixed Price'),
        ('none_detailed_assited_price', 'None Detailed - Assisted Price'),
        ('none_detailed_totaliced_price', 'None Detailed - Totaliced Price'),
    ],
        'Pack Type',
        help="* Detailed - Components Prices: Detail lines with prices on "
        "sales order.\n"
        "* Detailed - Totaliced Price: Detail lines on sales order totalicing "
        "lines prices on pack (don't show component prices).\n"
        "* Detailed - Fixed Price: Detail lines on sales order and use product"
        " pack price (ignore line prices).\n"
        "* None Detailed - Totaliced Price: Do not detail lines on sales order.\n"
        "* None Detailed - Assisted Price: Do not detail lines on sales "
        "order. Assist to get pack price using pack lines."
        )
    pack = fields.Boolean(
        'Pack?',
        help='Is a Product Pack?',
        )
    pack_line_ids = fields.One2many(
        related='product_variant_ids.pack_line_ids'
        )
    used_pack_line_ids = fields.One2many(
        related='product_variant_ids.used_pack_line_ids'
        )

    @api.constrains(
        'product_variant_ids', 'pack_price_type')
    def check_relations(self):
        """
        Check assited packs dont have packs a childs
        """
        # check assited price has no packs child of them
        if self.pack_price_type == 'none_detailed_assited_price':
            child_packs = self.mapped(
                'pack_line_ids.product_id').filtered('pack')
            if child_packs:
                raise Warning(_(
                    'A "None Detailed - Assisted Price Pack" can not have a '
                    'pack as a child!'))

        # TODO we also should check this
        # check if we are configuring a pack for a product that is partof a
        # assited pack
        # if self.pack:
        #     for product in self.product_variant_ids
        #     parent_assited_packs = self.env['product.pack.line'].search([
        #         ('product_id', '=', self.id),
        #         ('parent_product_id.pack_price_type', '=',
        #             'none_detailed_assited_price'),
        #         ])
        #     print 'parent_assited_packs', parent_assited_packs
        #     if parent_assited_packs:
        #         raise Warning(_(
        #             'You can not set this product as pack because it is part'
        #             ' of a "None Detailed - Assisted Price Pack"'))

    @api.one
    @api.constrains('company_id', 'product_variant_ids', 'used_pack_line_ids')
    def check_pack_line_company(self):
        """
        Check packs are related to packs of same company
        """
        for line in self.pack_line_ids:
            if line.product_id.company_id != self.company_id:
                raise Warning(_(
                    'Pack lines products company must be the same as the\
                    parent product company'))
        for line in self.used_pack_line_ids:
            if line.parent_product_id.company_id != self.company_id:
                raise Warning(_(
                    'Pack lines products company must be the same as the\
                    parent product company'))

    @api.multi
    def write(self, vals):
        """
        We remove from prod.prod to avoid error
        """
        if vals.get('pack_line_ids', False):
            self.product_variant_ids.write(
                {'pack_line_ids': vals.pop('pack_line_ids')})

        for prod in self:
        # set type to service if it's a pack
            if not 'pack' in vals:
                vals['pack'] = prod.pack
            if vals['pack'] == True:
                vals['type'] = 'service'
        return super(product_template, self).write(vals)

    @api.model
    def _price_get(self, products, ptype='list_price'):
        res = super(product_template, self)._price_get(
            products, ptype=ptype)
        for product in products:
            if (
                    product.pack and
                    product.pack_price_type in [
                        'totalice_price',
                        'none_detailed_assited_price',
                        'none_detailed_totaliced_price']):
                pack_price = 0.0
                for pack_line in product.pack_line_ids:
                    product_line_price = pack_line.product_id.price_get()[
                            pack_line.product_id.id] * (
                                1 - (pack_line.discount or 0.0) / 100.0)
                    product_line_price
                    pack_price += (product_line_price * pack_line.quantity)
                res[product.id] = pack_price
        return res

    @api.onchange('pack_line_ids','pack_price_type','type','pack','list_price')
    def set_pack_price(self):
        # This should work only in case of totalice or assited packs
        for prod in self:
            for pline in prod.pack_line_ids.filtered(lambda l: l.product_id.pack):
                pline.product_id.product_tmpl_id.set_pack_price()
            if prod.pack and prod.pack_price_type in [
                'totalice_price',
                'none_detailed_totaliced_price',
                'none_detailed_assited_price']:
                prod.list_price = sum(l.product_id.list_price * l.quantity for l in prod.pack_line_ids)

            if prod.pack and prod.type != 'service':
                prod.type = 'service'

    @api.constrains('list_price')
    def set_parent_pack_price(self):
        for prod in self:
            if not prod.pack: # if it's a pack > generates recursion
                for pack in prod.used_pack_line_ids:
                    pack.parent_product_id.product_tmpl_id.set_pack_price()
            #TODO: update parent pack product if exist - generates recursion error
            # working from Sale order line now
