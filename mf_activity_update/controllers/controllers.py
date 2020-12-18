# -*- coding: utf-8 -*-
# from odoo import http


# class MfActivityUpdate(http.Controller):
#     @http.route('/mf_activity_update/mf_activity_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mf_activity_update/mf_activity_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mf_activity_update.listing', {
#             'root': '/mf_activity_update/mf_activity_update',
#             'objects': http.request.env['mf_activity_update.mf_activity_update'].search([]),
#         })

#     @http.route('/mf_activity_update/mf_activity_update/objects/<model("mf_activity_update.mf_activity_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mf_activity_update.object', {
#             'object': obj
#         })
