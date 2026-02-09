from odoo import api, fields, models


class ProductSpecification(models.Model):
    _name = 'product.specification'
    _description = 'Product Specifications'
    
    name = fields.Char(string="Specification Name")
    value = fields.Char(string="Specification Value")
    reference_field_id = fields.Many2one(
        'ir.model.fields', 
        string="Specification Related Field",
        domain=[
            ('model', '=', 'product.product'),
            ('ttype', 'in', ['char','float','integer','boolean','date','datetime'])
        ])
    product_template_id = fields.Many2one('product.template', string="products")
    
    @api.model
    def create(self, vals):
        record = super().create(vals)

        # auto-clean empty lines
        if not record.name or not record.value:
            record.unlink()
            return self.env['product.specification']

        return record