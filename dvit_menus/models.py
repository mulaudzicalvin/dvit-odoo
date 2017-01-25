import operator
import copy
from openerp import api, tools

from openerp import models, fields

class IconsModel(models.Model):
	_name = 'icons.model'

	menu = fields.Char(
		string='Menu',
	)

	icon = fields.Char(
		string='Icon',
	)
	
	@api.multi
	def get_icons_menu(self):
		icon_menu = self.search([])
		icon_menu_wrap = []
		for menu in icon_menu:
			try:
				icon_menu_wrap.append({"id": self.env.ref(menu.menu).id, "icon": menu.icon})
			except Exception as e:
				continue
		return icon_menu_wrap

class ir_ui_menu(models.Model):
	_inherit = "ir.ui.menu"

	@api.cr_uid_context
	@tools.ormcache_context(accepted_keys=('lang',))
	def load_menus(self, cr, uid, context=None):
		dvit_res = super(ir_ui_menu, self).load_menus(cr, uid, context)
		ctx = copy.deepcopy(context)
		del ctx['lang']
		del ctx["tz"]
		del ctx['uid']
		icon_menu_wrap = self.pool.get("icons.model").get_icons_menu(cr, uid, ctx)
		for dvm in dvit_res['children']:
			for menu in icon_menu_wrap:
				if  menu['id'] != dvm['id']:
					dvm['dv_icon'] = dvm['id'], "  ", menu['id']
				else:
					dvm['dv_icon'] = menu['icon']
					break 
		return dvit_res