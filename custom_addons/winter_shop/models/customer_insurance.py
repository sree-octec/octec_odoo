from odoo import models, fields


class CustomerInsurance(models.Model):
    _name = 'customer.insurance'
    _inherits = {"res.partner": "insurance_partner_id"}
    
    insurance_partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    insurance_count = fields.Integer(string="Count Insurance")