# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrViolation(models.Model):
    _name = 'hr_violation'
    _rec_name = 'name'
    _description = 'hr violation'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(tracking=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=lambda self: self.env.company,
                                 required=False, tracking=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", tracking=True, required=False,default=lambda self: self.env.user.employee_id )
    violation_date = fields.Date(string="", required=False, tracking=True)
    description = fields.Text(string="", required=False, tracking=True)
    active = fields.Boolean(default=True,)
    display = fields.Boolean(default=True,)



    def archive(self):
        for rec in self:
            if rec.display == True:
                rec.display = False
            else:
                rec.display = True