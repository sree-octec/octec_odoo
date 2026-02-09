from odoo import models, fields


class SiCustomResPartner(models.Model):
    _inherit = "res.partner"
    
    customer_product_id = fields.Many2one('product.product', string="Customer Products")
    
    