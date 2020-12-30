from odoo import fields, models, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    lead_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    can_be_project = fields.Boolean(string="", )
    have_project = fields.Boolean(string="", default=False)

    def create_project(self):
        for rec in self:
            project = self.env['project.project'].create({
                'name': rec.name,
                'lead_id': rec.id,
            })
            rec.have_project = True
            task = self.env['project.task'].create({
                'name': 'المرجع',
                'stage_id': self.env.ref('mf_project_from_lead.stage_start').id,
                'project_id': project.id,
                'partner_id': rec.partner_id.id,
                'user_id': self.env.uid,
                'description': rec.description,
            })
            all_messages_crm = self.env['mail.message'].search(
                ["&", ('res_id', "=", rec.id), ('model', "=", "crm.lead"),
                 ('message_type', 'not in', ['comment', 'user_notification'])],order='create_date asc')
            for message in all_messages_crm:
                print(message.message_type)
                message.sudo().copy(
                    {'model': 'project.task', 'res_id': task.id,
                     'email_layout_xmlid': message.email_layout_xmlid, 'message_type': message.message_type,
                     'create_date': message.create_date,
                     })

    def open_project(self):
        project = self.env['project.project'].search([('lead_id', '=', self.id)], limit=1).id
        ctx = dict(
            default_lead_id=self.id)
        return {
            'name': _('Opportunity Visits'),
            'type': 'ir.actions.act_window',
            'res_model': "project.task",
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity,gantt,map',
            'target': 'current',
            'domain': [('project_id', '=', project)],
            'context': ctx,
        }
