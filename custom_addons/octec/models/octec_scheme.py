from odoo import api, fields, models

class OctecScheme(models.Model):
    _name= "octec.scheme"
    _description = " Schemes Available"
    _rec_name = "scheme_name"
    
    scheme_name = fields.Char(string="Scheme Name", required=True)
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    module_fee = fields.Monetary(string="Fee Per Module", currency_id="currency_id")
