from odoo import fields, models


class PracticeTaskCustomer(models.Model):
    _inherit = 'res.partner'

    
    age = fields.Char(string='Department')
