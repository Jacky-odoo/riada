from odoo import fields, models, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    lead_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    can_be_project = fields.Boolean(string="", )
    have_project = fields.Boolean(string="", default=False, copy=False)

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
                ["&", ('res_id', "=", rec.id), ('model', "=", "crm.lead"),], order='create_date asc')
            for message in all_messages_crm:
                if not message.notification_ids:
                    message.sudo().copy(
                        {'model': 'project.task', 'res_id': task.id,
                         'email_layout_xmlid': message.email_layout_xmlid, 'message_type': message.message_type,
                         'create_date': message.create_date, 'partner_ids': message.partner_ids,
                         })
            all_attach_crm = self.env['ir.attachment'].search(
                ["&", ('res_id', "=", rec.id), ('res_model', "=", "crm.lead")])
            for attach in all_attach_crm:
                attach.sudo().with_context(no_document=True).copy(
                    {'res_model': 'project.project', 'res_id': project.id, 'type': 'binary', })

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
