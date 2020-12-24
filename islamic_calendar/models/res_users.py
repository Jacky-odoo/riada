# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    calendear_localisation = fields.Selection([('ar', 'Arabic'), ('fa', 'Farsi')], 'Localization')

    def get_localisation(self):
        for record in self:
            lang_record = self.env['res.lang'].search([('code', '=', record.lang)])
            return {
                'lang': record.calendear_localisation,
                'date_format': lang_record.date_format if lang_record else '%m/%d/%Y'
            }
