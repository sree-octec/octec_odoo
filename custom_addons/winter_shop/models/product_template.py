from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    insurance_id = fields.Many2one(
        'product.insurance', 
        string="Insurance", 
        ondelete='cascade'
    )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        print("##########################",self.categ_id.name)
        if self.categ_id.name == 'Adult':
            insurances = self.env['product.insurance'].search([
                ('category_id', '=', self.categ_id.id)
            ])
            print("##########################",insurances.ids)
            return {'domain': {'insurance_id': [('id', 'in', insurances.ids)]}}
        else:
            return {'domain': {'insurance_id': []}}
