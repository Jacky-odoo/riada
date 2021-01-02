# -*- coding: utf-8 -*-
{
    'name': "Activity Updates",

    'summary': """
        schedule Activities Updates and Customizations """,

    'description': """
    """,

    'author': "Mohamed Fouad",
    'website': "http://www.linkedin.com/in/mfhm95",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/ir_rule.xml',
        'views/views.xml',
        'data/mail_data.xml',
    ],
    'qweb': ['static/src/xml/activity_update.xml'],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
