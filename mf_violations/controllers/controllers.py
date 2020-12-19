# -*- coding: utf-8 -*-
# from odoo import http


# class MfViolations(http.Controller):
#     @http.route('/mf_violations/mf_violations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mf_violations/mf_violations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mf_violations.listing', {
#             'root': '/mf_violations/mf_violations',
#             'objects': http.request.env['mf_violations.mf_violations'].search([]),
#         })

#     @http.route('/mf_violations/mf_violations/objects/<model("mf_violations.mf_violations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mf_violations.object', {
#             'object': obj
#         })
