from openerp.osv import osv, orm, fields
import openerp.addons.decimal_precision as dp
from openerp import api, models


class my_model_init(osv.osv_memory):

    _name = "my.model.init"
    _columns = {}
    _defaults = {}

    def _init_settings(self, cr, uid, ids=None, context=None):
        sale_settings_pool = self.pool.get('sale.config.settings')
        sale_settings_id = sale_settings_pool.create(cr, uid, {'group_discount_per_so_line':True}, context=context)
        sale_settings_obj = sale_settings_pool.browse(cr, uid, sale_settings_id, context=context)
        sale_settings_obj.execute()  # this call is actually changes the setting, you're missing this step @Yenthe ...
        return True


class account_invoice(osv.osv):

    _inherit = "account.invoice"

    def _discount_all(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        for invoice in self.browse(cr, uid, ids):
            tot_disc = 0.0
            for line in invoice.invoice_line:
                tot_disc += line.disc_amount
            res[invoice.id] = tot_disc
        return res

    def _total_all(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        tot_all = 0.0
        for invoice in self.browse(cr, uid, ids):
            for line in invoice.invoice_line:
                tot_all += line.total_wo_disc
            res[invoice.id] = tot_all
        return res

    _columns = {
        'disc_total': fields.function(_discount_all, string='Total Discount', type="float", digits_compute= dp.get_precision('Account'), store=True),
        'total_b4_disc':fields.function(_total_all, string='Total before discount', type="float", digits_compute= dp.get_precision('Account'), store=True),
    }


class account_invoice_line(osv.osv):

    _inherit = "account.invoice.line"

    def _discount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        for line in self.browse(cr, uid, ids):
            discount = line.price_unit * ((line.discount or 0.0)/100.0) * line.quantity
            res[line.id] = discount
        return res

    def _total_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        for line in self.browse(cr, uid, ids):
           total = line.price_unit * line.quantity
           res[line.id] = total
        return res

    _columns = {
        'disc_amount': fields.function(_discount_line, string='Discount', type="float", digits_compute= dp.get_precision('Account'), store=True),
        'total_wo_disc':fields.function(_total_line, string='Total', type="float", digits_compute= dp.get_precision('Account'), store=True),
    }
