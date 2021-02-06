# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mf_sale_update(models.Model):
#     _name = 'mf_sale_update.mf_sale_update'
#     _description = 'mf_sale_update.mf_sale_update'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
