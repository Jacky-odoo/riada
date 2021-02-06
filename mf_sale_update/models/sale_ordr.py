from odoo import fields, models, api, _
from lxml import etree


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def fields_view_get(self, view_id='sale.view_order_form',
                        view_type='form', toolbar=False, submenu=False):
        res = super(SaleOrder, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)
        doc = etree.XML(res['arch'])
        if self.env.context.get('default_opportunity_id') and (
                not self.env.user.has_group('sales_team.group_sale_manager') and not self.env.user.has_group(
                'base.group_erp_manager')):
            for node in doc.xpath("//field[@name='user_id']"):
                node.set('modifiers', '{"readonly": true}')
            for node in doc.xpath("//field[@name='team_id']"):
                node.set('modifiers', '{"readonly": true}')
        res['arch'] = etree.tostring(doc)
        return res
