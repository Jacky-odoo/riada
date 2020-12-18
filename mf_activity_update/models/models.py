# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mf_activity_update(models.Model):
#     _name = 'mf_activity_update.mf_activity_update'
#     _description = 'mf_activity_update.mf_activity_update'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
