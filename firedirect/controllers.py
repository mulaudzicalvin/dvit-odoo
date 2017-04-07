# -*- coding: utf-8 -*-
from openerp import http

# class Firedirect(http.Controller):
#     @http.route('/firedirect/firedirect/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/firedirect/firedirect/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('firedirect.listing', {
#             'root': '/firedirect/firedirect',
#             'objects': http.request.env['firedirect.firedirect'].search([]),
#         })

#     @http.route('/firedirect/firedirect/objects/<model("firedirect.firedirect"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('firedirect.object', {
#             'object': obj
#         })