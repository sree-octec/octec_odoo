{
    "name": "Ration Shop",
    "version": "1.0.0",
    "licence": "LGPL-3",
    "author": "sreejith vijayakumar",
    "summary": "One place to shop home stationay products",
    "depends": ["base","contacts","sale"],
    "data": [
        "security/ir.model.access.csv",
        
        "wizard/product_delivered_detail_view.xml",
        
        "report/report_sale_order_inherit.xml",
        "views/sale_order_view.xml",
        "views/product_template_view.xml",
        "views/product_specification_view.xml",
        "views/product_category_view.xml",
        "views/ration_product_detail_view.xml",
        "views/res_partner_view.xml"
    ],
    "application": True,
    "installable": True
    
}