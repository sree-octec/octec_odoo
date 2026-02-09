{
    'name': 'SI Custom',
    'version': '1.0.0',
    'author': 'sreejith',
    'summary': """ Si Grroup Custom requirements""",
    'depends': ['base','sale','purchase','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/si_custom_customer_update_view.xml',
        
        'views/si_custom_res_partner_view.xml',
        'views/si_custom_purchase_order_view.xml',
        'views/si_custom_sale_order_view.xml'
    ],
    'licence': 'LGPL-3',
    'application': False,
    'installalbe': True
}