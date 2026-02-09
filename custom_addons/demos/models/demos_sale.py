from odoo import models, fields


class DemosSale(models.Model):
    _name = "demos.sale"
    _description = "Demos Sale"
    
    sale_order_number = fields.Integer(string="Sale Order Number")
    customer_id = fields.Many2one(
        'demos.customer', string="customer", 
        required=True, index=True)
    bill_datetime = fields.Datetime(string="Bill Date & Time")
    sale_order_line_ids = fields.One2many(
        'demos.sale_order_line', 'sale_order_id', string="Product", 
        required=True, index=True)
    
    states = fields.Selection([
        ('draft', "Draft"),
        ('first_approval', "First Approval"),
        ('second_approval', "Second Approval"),
        ('order', "Order")
    ], string="States", default="draft")
    
    def send_by_email(self):
        pass
    def send_for_approval(self):
        pass
