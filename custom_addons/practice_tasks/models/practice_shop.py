from odoo import models, fields


class PracticeShop(models.Model):
    _name = 'practice.shop'
    _description = 'practice shop'
    
    name = fields.Char(string="Name")
    email = fields.Char(strinng="Email")
    start_date = fields.Date(string="Start Date")