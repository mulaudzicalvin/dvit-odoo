# -*- coding: utf-8 -*-

from odoo import http, tools, _
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale as Base


class WebsiteSale(Base):
    @route()
    def address(self, **kw):
        country = request.website.company_id.country_id
        kw['country_id'] = country.id
        kw['country'] = country.id
        kw['state_id'] = request.env['res.country.state'].sudo().search([('code','=','GZ'),('country_id','=',country.id)]).id
        kw['city'] = 'Giza'
        kw['street'] = 'NA'
        # print '>>>>> kw:', kw

        result = super(WebsiteSale, self).address(**kw)

        result.qcontext["cities"] = request.env['res.country.city'].search([])
        result.qcontext["zones"] = []#request.env['res.country.city.zone'].search([])
        result.qcontext["builds"] = [] #request.env['res.zone.building'].search([])
        result.qcontext["city"] = (result.qcontext.get('city_id') != '') and request.env['res.country.city'].sudo().browse(result.qcontext.get('city_id')).name

        return result

    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        for val in all_values:
            if hasattr(Partner,val):
                checkout[val] = all_values[val]

        partner_id = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
        return partner_id

    @http.route(['/shop/zone_info/<model("res.country.city.zone"):zone>'], type='json',
    auth="public", methods=['POST'], website=True)
    def zone_info(self, zone, **kw):
        return dict(
            builds=[(b.id, b.name) for b in zone.building_ids],
        )

    @http.route(['/shop/city_info/<model("res.country.city"):city>'], type='json',
    auth="public", methods=['POST'], website=True)
    def city_info(self, city, **kw):
        return dict(
            zones=[(z.id, z.name) for z in city.zone_ids],
        )

    @http.route(['/shop/state_info/<model("res.country.state"):state>'], type='json',
    auth="public", methods=['POST'], website=True)
    def state_info(self, city, **kw):
        return dict(
            cities=[(cc.id, cc.name) for cc in state.city_ids],
        )
