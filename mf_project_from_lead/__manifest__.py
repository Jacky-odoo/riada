# -*- coding: utf-8 -*-
{
    'name': "Project From Leads",

    'summary': """
        create a project From leads """,

    'description': """
    """,

    'author': "Mohamed Fouad",
    'website': "http://www.mfhm95.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','project','documents'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/ir_rule.xml',
        'data/data.xml',
        'views/views.xml',
        'views/crm_lead_view.xml',
        # 'views/templates.xml',
    ],
    # 'qweb': ['static/src/xml/activity_update.xml'],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
