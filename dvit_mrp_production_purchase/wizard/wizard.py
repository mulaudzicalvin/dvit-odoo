from odoo import models, fields, api

class WizMrpPurchase(models.TransientModel):
    _name = 'wiz.mrp.purchase'
    request_all = fields.Boolean(string="Request all materials",
        help="Request all materials or only unavailable materials.")
    vendor_id = fields.Many2one(
        string="Vendor",
        comodel_name="res.partner",
        domain="[('supplier', '=', 1)]",
        )

    def _prepare_po(self):
        production_id = self.env['mrp.production'].browse(self._context.get('active_id'))
        picking_type_id = self.env['stock.picking.type'].sudo().search([
        ('warehouse_id','=',production_id.move_raw_ids[0].group_id.procurement_ids[0].warehouse_id.id),
        ('code','=','incoming')
        ])
        po_id = self.env['purchase.order'].sudo().create({
            'partner_id': self.vendor_id.id,
            'origin': production_id.name,
            'date_planned': production_id.date_planned_start,
            'picking_type_id': picking_type_id.id,
        })

        if self.request_all:
            raw_ids = production_id.move_raw_ids
        else:
            raw_ids = production_id.move_raw_ids.filtered(lambda m: m.state == 'confirmed')

        for rm_line in raw_ids:
            self.env['purchase.order.line'].sudo().create({
            'product_id': rm_line.product_id.id,
            'name': rm_line.product_id.name,
            'product_qty': rm_line.product_uom_qty,
            'product_uom': rm_line.product_uom.id,
            'price_unit': 0.0,
            'order_id': po_id.id,
            'date_planned': production_id.date_planned_start,
            })

        po_id.action_set_date_planned()
        production_id.purchase_ids += po_id

        return po_id

    @api.multi
    def add_po(self):
        po_id = self._prepare_po()

        return po_id
