from odoo import models, fields, api


class ProductInsurance(models.Model):
    _name = 'product.insurance'
    _description = 'Product Insurance'
    
    name = fields.Char(string='Name', index='trigram', required=True)
    insurance_rate = fields.Float(string='Insurance Rate')
    category_id = fields.Many2one('product.category')