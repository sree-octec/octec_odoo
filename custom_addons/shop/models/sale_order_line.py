from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_product_id = fields.Many2one(
        'shop.customer.link.product',
        string="Customer Product Link"
    )
    
    
    def order_list(self):
        orders = self.env['sale.order'].search(
            [('state', '=', 'sale')]
        )
        _logger.info("confirm orders is %s", orders)
    
    
    @api.onchange('product_id', 'order_id.partner_id')
    def _onchange_customer_product_link(self):
        """
        Automatically links the sale order line to the customer's product quota
        if such record exists.
        """

        for line in self:
            customer = line.order_id.partner_id
            product = line.product_id

            if customer and product:
                record = self.env['shop.customer.link.product'].search([
                    ('shop_partner_id', '=', customer.id),
                    ('product_id', '=', product.id)
                ], limit=1)

                line.customer_product_id = record.id

    @api.constrains('product_uom_qty', 'customer_product_id')
    def _check_customer_product_limit(self):
        """
        Ensures that customer does NOT exceed assigned quota.
        """
        for line in self:
            record = line.customer_product_id

            if record:
                if line.product_uom_qty > record.available_quantity:
                    raise ValidationError(
                        f"Customer '{record.shop_partner_id.name}' is allowed to buy only "
                        f"{record.available_quantity} qty of '{record.product_id.display_name}'. "
                        f"You entered {line.product_uom_qty}."
                    )
