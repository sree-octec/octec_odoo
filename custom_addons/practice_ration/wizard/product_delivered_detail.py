from odoo import models, fields, api


class ProductDeliveredDetail(models.TransientModel):
    _name = 'product.delivered.detail'
    _description = 'product delivered detail'

    sale_order_ids = fields.Many2many('sale.order', string="sale orders")