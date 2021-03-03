# -*- coding: utf-8 -*-

from odoo import models, fields, api


class smEditor(models.Model):
    _inherit = 'res.partner'

    editor = fields.Text("Editor")
