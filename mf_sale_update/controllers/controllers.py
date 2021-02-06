# -*- coding: utf-8 -*-
# from odoo import http


# class MfSaleUpdate(http.Controller):
#     @http.route('/mf_sale_update/mf_sale_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mf_sale_update/mf_sale_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mf_sale_update.listing', {
#             'root': '/mf_sale_update/mf_sale_update',
#             'objects': http.request.env['mf_sale_update.mf_sale_update'].search([]),
#         })

#     @http.route('/mf_sale_update/mf_sale_update/objects/<model("mf_sale_update.mf_sale_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mf_sale_update.object', {
#             'object': obj
#         })
