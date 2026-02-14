{
    "name": "Po Approval",
    "version": "1.0.0",
    "licence": "LGPL-3",
    "author": "sreejith vijayakumar",
    "summary": "Bring Approval to Purchase Orders",
    "depends": ["base","purchase","mail"],
    "data": [
        "security/odoo_approval_security_groups.xml",
        "security/ir.model.access.csv",
        "views/purchase_order_approval_filter_view.xml",
        "views/res_config_settings_approval_views.xml",
        "views/purchase_order_view.xml"
        
    ],
    "application": True,
    "installable": True
    
}