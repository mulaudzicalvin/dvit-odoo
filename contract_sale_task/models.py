# -*- coding: utf-8 -*-

from openerp import models, fields, api



class saleOrder(models.Model):
    _inherit = 'sale.order'

    # client_order_ref = fields.Char(string="Reference/Description", required=True)
    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(saleOrder, self).action_button_confirm(cr, uid, ids, context)
        task_obj = self.pool.get('project.task')
        orders = self.browse(cr, uid, ids)
        # order_lines_for = sale_order.order_line
        for order in orders:
            ref = order.client_order_ref and order.client_order_ref or "No Refrence"
            for line in order.order_line:
                task_ids = task_obj.search(cr, uid, [('sale_line_id','=', line.id)])
                tasks = task_obj.browse(cr, uid, task_ids)
                for task in tasks:
                    task.name = task.name + " " + "[" + ref + "]"
        return res
