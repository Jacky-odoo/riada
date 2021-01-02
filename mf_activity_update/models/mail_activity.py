from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from collections import defaultdict

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    can_delete = fields.Boolean(string="", compute='check_delete')
    can_edit = fields.Boolean(string="", compute='check_delete')

    @api.depends('user_id')
    def check_delete(self):
        for record in self:
            if (record.create_uid.id == self.env.user.id and not record.is_reply) or self.env.user.has_group('project.group_project_manager'):
                record.can_edit = record.can_delete = True
            else:
                record.can_edit = record.can_delete = False
        pass


    is_reply = fields.Boolean(string="",default=False  )

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        print(self.is_reply, '111111111111111')

        # if self.is_reply:
        #     self.reply_done()
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )
            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message
        next_activities = self.env['mail.activity'].create(next_activities_values)
        print(activity.res_model,activity._name,activity.activity_type_id,activity.id,'######')
        print(activity.id)
        data = {
            'res_model_id': self.env['ir.model'].search(
                [('model', '=',activity.res_model )]).id,
            'res_id': activity.res_id,
            'activity_type_id': self.env['mail.activity.type'].search(
                    [('name', 'like', 'Handle Ticket')]).id,
            'summary': _(' I did it' ),
            'note': _('لقد اتممت المهمة بنجاح يمكنك الاطلاع الان'),
            'date_deadline': fields.Datetime.now(),
            'user_id': activity.create_uid.id,
            'is_reply': True,
        }

        if not self.is_reply:
            noti = self.env['mail.activity'].create(data)
            noti.unlink()
        self.unlink()  # will unlink activity, dont access `self` after that

        return messages, next_activities

    def action_notify(self):
        if not self:
            return
        original_context = self.env.context
        if self.is_reply:
            print("******************************************")
            body_template = self.env.ref('mf_activity_update.message_activity_assigned_for_replay')
        else:
            body_template = self.env.ref('mail.message_activity_assigned')
        for activity in self:
            if activity.user_id.lang:
                # Send the notification in the assigned user's language
                self = self.with_context(lang=activity.user_id.lang)
                body_template = body_template.with_context(lang=activity.user_id.lang)
                activity = activity.with_context(lang=activity.user_id.lang)
            model_description = self.env['ir.model']._get(activity.res_model).display_name
            body = body_template.render(
                dict(activity=activity, model_description=model_description),
                engine='ir.qweb',
                minimal_qcontext=True
            )
            record = self.env[activity.res_model].browse(activity.res_id)
            if activity.user_id:
                record.message_notify(
                    partner_ids=activity.user_id.partner_id.ids,
                    body=body,
                    subject=_('%s: %s assigned to you') % (activity.res_name, activity.summary or activity.activity_type_id.name),
                    record_name=activity.res_name,
                    model_description=model_description,
                    email_layout_xmlid='mail.mail_notification_light',
                )
            body_template = body_template.with_context(original_context)
            self = self.with_context(original_context)