
from odoo import api, fields, models

class ProductTmpl(models.Model):
    _inherit = 'product.template'

    warehouse_id = fields.Many2one(
        string="Default warehouse",
        comodel_name="stock.warehouse",
        help="Will be forced in sale, purchase and manufacture orders.",
        )

    @api.depends('categ_id')
    def _set_wh(self):
        for prod in self:
            product.write({'warehouse_id': categ_id.warehouse_id and categ_id.warehouse_id.id,})

class ProductCat(models.Model):
    _inherit = 'product.category'

    warehouse_id = fields.Many2one(
        string="Default warehouse",
        comodel_name="stock.warehouse",
        help="Will be forced in sale, purchase and manufacture orders of products in this category.",
        )

    @api.depends('parent_id')
    def _set_wh(self):
        warehouse_id = parent_id.warehouse_id

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_procurement_group_by_line(self, line):
        vals = super(SaleOrder, self)._prepare_procurement_group_by_line(line)
        wh_id = line.product_id.product_tmpl_id.warehouse_id and \
        line.product_id.product_tmpl_id.warehouse_id or \
        line.product_id.product_tmpl_id.categ_id.warehouse_id

        if wh_id:
            vals['name'] += '/' + wh_id.name
        return vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="product_id.product_tmpl_id.warehouse_id"
    )

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        values = super(SaleOrderLine, self).\
            _prepare_order_line_procurement(group_id=group_id)
        wh_id = self.warehouse_id and self.warehouse_id or \
            self.product_id.product_tmpl_id.warehouse_id or \
            self.product_id.product_tmpl_id.categ_id.warehouse_id
        if wh_id:
            values['warehouse_id'] = wh_id.id
        return values

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="product_id.product_tmpl_id.warehouse_id"
    )

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        wh_id = self.warehouse_id and self.warehouse_id or \
            self.product_id.product_tmpl_id.warehouse_id or \
            self.product_id.product_tmpl_id.categ_id.warehouse_id
        if wh_id and picking.location_dest_id != wh_id.lot_stock_id:
            pick_id = picking.copy()
            pick_id.update({'location_dest_id': wh_id.lot_stock_id.id})
            for move in res:
                move.update({
                'picking_id': pick_id.id,
                'warehouse_id': wh_id.id,
                'location_dest_id': wh_id.lot_stock_id.id,
                'name': move.get('name') + '/' + wh_id.name,
                })
        return res
