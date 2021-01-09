# -*- coding: utf-8 -*-
# from odoo import http


# class MfProjectFromLead(http.Controller):
#     @http.route('/mf_project_from_lead/mf_project_from_lead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mf_project_from_lead/mf_project_from_lead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mf_project_from_lead.listing', {
#             'root': '/mf_project_from_lead/mf_project_from_lead',
#             'objects': http.request.env['mf_project_from_lead.mf_project_from_lead'].search([]),
#         })

#     @http.route('/mf_project_from_lead/mf_project_from_lead/objects/<model("mf_project_from_lead.mf_project_from_lead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mf_project_from_lead.object', {
#             'object': obj
#         })
