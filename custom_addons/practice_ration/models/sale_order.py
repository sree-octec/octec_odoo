from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    dummy_field = fields.Char(string="check field")
    
    def get_delivered_orders(self):
        self.ensure_one()
        return {
            'name': 'Deliveries for %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking', 
            'view_mode': 'list,form',      
            'domain': [('id', 'in', self.picking_ids.ids)],
            'context': {
                'default_origin': self.name,
                'default_sale_id': self.id,
                'create': False
            },
            'target': 'new', 
        }
        
    def get_delivered_orders_wizard(self):
        self.ensure_one()
        return {
            'name': 'Deliveries for %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'product.delivered.detail', 
            'view_mode': 'list,form',      
            'context': {
                'default_origin': self.name,
                'default_sale_id': self.id,
                'create': False
            },
            'target': 'new', 
        }
        
