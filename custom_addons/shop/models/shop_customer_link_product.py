from odoo import models, fields, api


class ShopCustomerLinkProduct(models.Model):
    _name = 'shop.customer.link.product'
    _description = 'Shop Customer Link Product'
    _sql_constraints = [
        ('available_quantity_zero', 'CHECK (available_quantity>=0)', 'Allowed quantity exceede')]

    
    shop_partner_id = fields.Many2one('res.partner', string="Customers")
    product_id = fields.Many2one('product.product', string="products")
    product_quantity = fields.Float(string="Quantity")
    
    sale_order_ids = fields.One2many('sale.order.line', 'customer_product_id')
    available_quantity = fields.Float(compute='_available_product_quantity', string="available quantity", store=True)
    
    @api.depends('sale_order_ids.product_uom_qty')
    def _available_product_quantity(self):
        for rec in self:
            match_lines = rec.sale_order_ids.filtered(
                lambda line:line.product_id.id == rec.product_id.id 
            )
            purchase_quantity = sum(match_lines.mapped('product_uom_qty'))
            rec.available_quantity = rec.product_quantity - purchase_quantity
                        
        for rec in self:
            print("available_quantity", rec.available_quantity)
    
            
    

    