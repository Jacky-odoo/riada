from odoo import fields, models, api,_


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    def action_new_quotation(self):
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': self.tag_ids.ids,
            'default_user_id': self.user_id.id,
        }
        if self.user_id != self.env.uid:
            action['context'].update({
                'not_self_saleperson': True,
                'default_team_id': self.team_id.id,
                'default_user_id': self.user_id.id,
            })
        return action
