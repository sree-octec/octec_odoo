from odoo import models, fields


class DemosProduct(models.Model):
    _name= "demos.product"
    _description = " Demos Product"
    
    name = fields.Char(string="Name", required=True)
    cost_price = fields.Float(string="Cost Price", required=True)
    sell_price = fields.Float(string="Sell Price")
    discount = fields.Float(string="Discount")
    manufacture_date = fields.Date(string="Manufacturing Date")
    product_image = fields.Binary()
    material = fields.Char(string="Material")
    color = fields.Char(string="Color")
    