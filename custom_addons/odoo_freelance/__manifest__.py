# -*- coding: utf-8 -*-
{
    'name': "odoo freelance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'account', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/quick_order_report.xml',
        'views/quick_order_mail_template.xml',
        'wizard/quick_order_mail_wizard_view.xml',
        "report/report_quick_order_with_payments.xml",
        'wizard/odoo_freelance_quick_order_view.xml',
        'wizard/odoo_freelance_customer_change_view.xml',
        'views/quick_order_product_line_view.xml',
        'views/sale_order_view.xml',
        'views/sale_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True
}

