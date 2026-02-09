from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        # If our custom bypass flag is in the context, we skip the UserError check
        if 'pricelist_id' in vals and self.env.context.get('bypass_pricelist_check'):
            return super(models.Model, self).write(vals) 
        return super().write(vals)
    
    