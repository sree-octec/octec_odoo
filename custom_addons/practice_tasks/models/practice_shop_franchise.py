from odoo import models, fields


class PracticeShopFranchise(models.Model):
    _name = 'practice.shop.franchise'
    _inherit = 'practice.shop'
    
    phone_number = fields.Char(string="Phone Number")
    branch = fields.Char(strinng="Branch")
    expiry_date = fields.Date(string="Expiry Date")