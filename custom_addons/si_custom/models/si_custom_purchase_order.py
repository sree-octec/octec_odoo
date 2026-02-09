from odoo import models, fields


class SiCustomPurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    po_reference = fields.Char(string="Po Reference")