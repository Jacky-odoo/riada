# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mf_project_from_lead(models.Model):
#     _name = 'mf_project_from_lead.mf_project_from_lead'
#     _description = 'mf_project_from_lead.mf_project_from_lead'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
