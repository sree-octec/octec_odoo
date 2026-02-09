from odoo import models, fields
import logging


class DemosSaleOredrLine(models.Model):
    _name = "demos.sale_order_line"
    _description = "Sale Order Lines"
    _logger = logging.getLogger(__name__)
    
    product_id = fields.Many2one('demos.product')
    sale_order_id = fields.Many2one('demos.sale')
    name = fields.Char(related="product_id.name", store=True)
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    currency_id = fields.Many2one(
        'res.currency', string="Currency", 
        required=True,
        default=lambda self: self.env.ref('base.INR'))
    sub_total = fields.Monetary(string="Amount")
    total = fields.Monetary(string="Total")
    
