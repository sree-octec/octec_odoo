from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        line = super().create(vals)

        insurance_value = line.product_template_id.insurance
        if insurance_value == 'adult':
            insurance_price_unit = line.price_unit * 0.1
        elif insurance_value == 'kids':
            insurance_price_unit = line.price_unit * 0.05
        else :
            insurance_price_unit = 0.0

        if not insurance_value:
            return line
        
        if insurance_value:
            self.env['sale.order.line'].create({
                'order_id': line.order_id.id,
                'name': insurance_value,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': insurance_price_unit,
            })

        return line


