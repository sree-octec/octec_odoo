from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_specification_ids = fields.One2many('product.specification', 'product_template_id', string="specifications")