from odoo import models, fields


class SiCustomCustomerUpdate(models.TransientModel):
    _name = 'si_custom.customer_update'
    _description = 'Si custom customer update'
    
    customer_id = fields.Many2one('res.partner', string="Customer")
    
    def update_sale_order_customer(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
        sale_order.partner_id = self.customer_id
        return {'type': 'ir.actions.act_window_close'}