from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    age = fields.Integer(string="Age")