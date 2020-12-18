from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    # def write(self, values):
    #     if not (self.env.user.has_group('project.group_project_manager')):
    #         if self.create_uid.id == self.env.user.id:
    #             print(self.create_uid.id, self.env.user.id)
    #             return super(MailActivity, self).write(values)
    #         if self.user_id.id != self.env.user.id:
    #             print(self.user_id.id, self.env.user.id)
    #             raise ValidationError(_("You Can't Edit Activity That you didn't create "))
    #     return super(MailActivity, self).write(values)

    # @api.depends('res_model', 'res_id', 'user_id')
    # def _compute_can_write(self):
    #     # valid_records = self._filter_access_rules('write')
    #     for record in self:
    #         record.can_write = False
    #         if record.create_uid.id == self.env.user.id or self.env.user.has_group('project.group_project_manager'):
    #             record.can_write = True
    #             print('1111111111111111')
    #             return
    #         if record.user_id.id == self.env.user.id:
    #             record.can_write = True
    #             print('22222222222222222')
    #             return
    #
    #         print('3333333333333333333')
    #         # record.can_write = record in valid_records

    can_delete = fields.Boolean(string="", compute='check_delete')
    can_edit = fields.Boolean(string="", compute='check_delete')

    @api.depends('user_id')
    def check_delete(self):
        for record in self:
            if record.create_uid.id == self.env.user.id or self.env.user.has_group('project.group_project_manager'):
                record.can_edit = record.can_delete = True
            else:
                record.can_edit = record.can_delete = False
        pass

    # @api.depends('user_id')
    # def check_edit(self):
    #     for record in self:
    #         if record.create_uid.id == self.env.user.id or self.env.user.has_group('project.group_project_manager'):
    #             record.can_edit =True
    #         else:
    #             record.can_edit = False
    #     pass
