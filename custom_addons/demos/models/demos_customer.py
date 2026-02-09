from odoo import models, fields


class DemosCustomer(models.Model):
    _name = "demos.customer"
    _description = "Demos Customer Data"
    
    name = fields.Char(string="Name", required=True)
    phone_number = fields.Char(string="Phone Number")
    email = fields.Char(string="Email", required=True)
    dob = fields.Date(string="Date of Birth")
    address = fields.Text(string="Address")
    pin_code = fields.Integer(string="Pin code")
    country = fields.Char(string="Country") 

    
