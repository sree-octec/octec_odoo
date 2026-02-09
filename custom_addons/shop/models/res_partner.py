from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    customer_product_ids = fields.One2many(
        'shop.customer.link.product', 
        'shop_partner_id', 
        string="Customer Products"
    )