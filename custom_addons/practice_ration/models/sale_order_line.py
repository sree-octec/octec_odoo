from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
from odoo.tools import date_utils


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    is_auto_created = fields.Boolean(default=False)
    
    @api.constrains('product_uom_qty', 'product_template_id', 'order_id')
    def _check_monthly_quota(self):
        for line in self:
            quota = self.env['ration.product.detail'].search(
                [('partner_id', '=', line.order_id.partner_id.id),
                 ('product_template_id', '=', line.product_template_id.id)], limit=1
            )
            start_date = date_utils.start_of(line.order_id.date_order, "month") 
            end_date = date_utils.end_of(line.order_id.date_order, "month")
            
            total_records = self.env['sale.order.line'].search(
                [('order_id.partner_id', '=', line.order_id.partner_id.id),
                 ('product_template_id', '=', line.product_template_id.id),
                  ('order_id.date_order', '>=', start_date),
                  ('order_id.date_order', '<=', end_date), 
                  ('order_id.state','in', ['sale', 'done'])]
            )
            total_quantity = sum(total_records.mapped('product_uom_qty'))
            if quota and total_quantity > quota.reserved_quantity:
                raise ValidationError('Quantity cant be exceded')

    
    @api.model
    def create(self, values):
        if values.get('is_auto_created'):
            return super().create(values)

        line = super().create(values)

        categ = line.product_id.categ_id
        if not categ or not categ.product_service_id:
            return line
        else:
            self.env['sale.order.line'].create({
                'order_id': line.order_id.id,
                'product_id': categ.product_service_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': categ.product_service_id.list_price,
                'is_auto_created': True,
            })

        return line
        
    @api.onchange('product_id')
    def _onchange_product_id(self):

        if not self.product_id:
            return

        description = self.name or self.product_id.name

        for spec in self.product_id.product_tmpl_id.product_specification_ids:
            description += f"\n{spec.name}: {spec.value}"

        self.name = description

        