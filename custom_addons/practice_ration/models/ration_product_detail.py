from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RationProductDetail(models.Model):
    _name = 'ration.product.detail'
    _description = 'Ration Product Detail'
    _sql_constraints = [
        (
            'partner_product_unique',
            'unique(partner_id, product_template_id)',
            'You cannot add the same product more than once for the same customer.'
        )
    ]
    
    product_template_id = fields.Many2one('product.template', string="Products")
    reserved_quantity = fields.Float(string="Monthly Quota")
    partner_id = fields.Many2one('res.partner', string="Customer")
    
    
    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        if not self.product_template_id or not self.partner_id:
            return

        # Check duplicates in current One2many lines (UI cache)
        duplicates = self.partner_id.ration_product_ids.filtered(
            lambda l: l.product_template_id == self.product_template_id and l != self
        )

        if duplicates:
            self.product_template_id = False
            return {
                'warning': {
                    'title': "Duplicate Product",
                    'message': f"The product '{duplicates[0].product_template_id.name}' "
                            "is already added for this customer."
                }
            }
            
    @api.model
    def create(self, vals):
        record = super().create(vals)

        # auto-clean empty lines
        if not record.product_template_id:
            record.unlink()
            return self.env['ration.product.detail']

        return record

