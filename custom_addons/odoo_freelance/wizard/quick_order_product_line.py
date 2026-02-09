from odoo import api, fields, models


class QuickOrderProduct(models.TransientModel):
    _name = 'quick.order.product.line'
    _description = 'Odoo Quick Order'
    
    product_id = fields.Many2one('product.product', string="Quick Order", required=True)
    quantity = fields.Integer(string="Quantity")
    
    freelance_quick_order_id = fields.Many2one('odoo.freelance.quick.order')
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        available_qty = self.product_id.qty_available
        self.quantity = 1 if available_qty>0 else 0
    
