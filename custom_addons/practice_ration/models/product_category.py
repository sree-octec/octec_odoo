from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    product_service_id = fields.Many2one(
        'product.product',
        string="Insurance Product", 
        domain=[('type', '=', 'service')])