# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    def copy(self, default=None):
        sale_copy = super(sale_order, self).copy(default)
        # we unlink pack lines that should not be copied
        pack_copied_lines = sale_copy.order_line.filtered(
                lambda l: l.pack_parent_line_id.order_id == self)
        for line in pack_copied_lines:
            line.pack_parent_line_id=False
        pack_copied_lines.unlink()

        for line in sale_copy.order_line.filtered(
            lambda l: l.pack_child_line_ids and
            l.product_id.pack_price_type == 'totalice_price' and
            not l.pack_parent_line_id):
            line.price_unit = line.env['product.pricelist'].price_get(
                line.product_id.id, line.product_uom_qty,
                line.order_id.partner_id.id)[line.order_id.pricelist_id.id]
            # line.price_subtotal = line.price_unit * line.product_uom_qty


        return sale_copy



    def write(self, vals):
        old_lines = self.order_line
        res = super(sale_order, self).write(vals)

        if old_lines:
            for order in self:
                ### we will recalculate all lines that have childs and totalice_price and depth is 0
                for line in order.order_line.filtered(lambda l: l.pack_child_line_ids and
                l.product_id.pack_price_type == 'totalice_price' and l.pack_depth == 0):
                    print '>>>>>> totalice_price line w depth 0: ', line.product_id.name
                    # line.price_unit = 0.0
                    line.update_pack_line_total()
                    

            ######################## detailed recalculation below code is headache, so canceld ############

        # # for line in self.order_line:
        # #     print '>>>>>> before write line:', line.id, ',', line.product_id.name, ',', line.product_uom_qty
        # #
        # #     print '>>>>> old line: ', line
        # #         [act,   id, {vals}]
        # # l_val:  [4,   1993,   False] >>
        # # l_val:  [1,   2001,   {u'pack_depth': 33}]
        # # l_val:  [2,   2001,   False]
        # # l_val:  [0,   False,  {u'product_uom': 1, u'sequence': 11, u'price_unit': 10, u'line_no': False, u'is_optional': False, u'pack_child_line_ids': [], u'procurement_ids': [], u'qty_delivered': 0, u'qty_delivered_updateable': True, u'customer_lead': 0, u'analytic_tag_ids': [], u'state': u'draft', u'name': u'AProd1', u'duplicate': False, u'tax_id': [], u'product_uom_qty': 1, u'discount': 0, u'layout_category_id': False, u'pack_parent_line_id': False, u'invoice_status': u'no', u'product_id': 103, u'pack_depth': 0, u'alt_product_id': False, u'route_id': False}]
        # #   l_val[0] = action {4: none, 0: create - id=False, 1: write, 2: unlink}
        #
        # old_line_ids = [l.id for l in self.order_line]
        # deleted_line_parents = []
        #
        # for l_val in vals['order_line']:
        #     # if action = unlink & self.line.pack_parent_line_id
        #     if l_val[0]==2 and self.order_line.browse(l_val[1]).pack_parent_line_id:
        #         line_2_delete = self.order_line.browse(l_val[1])
        #         deleted_line_parents.append(self.order_line.browse(l_val[1]).pack_parent_line_id)
        #         # print '>>>>> Line2Del , its parent: ', line_2_delete.product_id.name, ', ', line_2_delete.pack_parent_line_id.product_id.name
        #         # deleted_line_parent.update_pack_total()
        #
        # res = super(sale_order, self).write(vals)
        #
        # order_line_ids = [l.id for l in self.order_line]
        # added_line_ids = [l.id for l in self.order_line if l.id not in old_line_ids]
        # deleted_line_ids = [l for l in old_line_ids if l not in order_line_ids]
        #
        # # for l in new_lines:
        # #     print '>>>> new lines: ', l.product_id.name
        #
        # # for l_val in vals['order_line']:
        # #     # print ">>>>>> l_val: ", l_val
        # #
        # #     # if action = create & have data and data dict have pack_parent_line_id
        # #     # also check if old_lines have lines - do not run on 1st time creation
        # #     if l_val[0]==0 and l_val[2].get('pack_parent_line_id') and old_line_ids:
        # #         new_parent = self.env['sale.order.line'].browse(l_val[2].get('pack_parent_line_id'))
        # #         print '>>>>> created line with parent: ', l_val
        # #         # self.update_pack_total(new_parent=new_parent)
        # #
        # #     # if action = write & have data & data dict have pack_parent_line_id
        # #     if l_val[0]==1 and l_val[2] and l_val[2].get('pack_parent_line_id'):
        # #         line_id = l_val[1]
        # #         # get old pack_parent_line_id
        # #         old_parent = self.order_line.filtered(lambda l: l.id == line_id).pack_parent_line_id
        # #         new_parent = self.env['sale.order.line'].browse(l_val[2].get('pack_parent_line_id'))
        # #         print '>>>>> write old, new parents: ', old_parent.product_id.name, ',', new_parent.product_id.name

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
