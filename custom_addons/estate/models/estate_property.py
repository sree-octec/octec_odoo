from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'
    
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.char(string="Post Code")
    date_availability = fields.Date(string="Date Availaility")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Flaot(string="Selling Price")
    bedrooms = fields.Integer(string="Bed Rooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), 
         ('east', 'East'), ('west', 'West')], 
        string="garden Orientation", default='south'
    )