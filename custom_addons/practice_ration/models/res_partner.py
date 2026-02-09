from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    reservation_type = fields.Selection(
        [('apl', 'APL'), ('bpl', 'BPL')], default='apl', string="Reservation Type"
    )
    ration_product_ids = fields.One2many('ration.product.detail', 
                                         'partner_id', 
                                         string="Products")
    
    @api.model
    def create(self, values):
        partner = super().create(values)

        if partner.is_company and partner.ration_product_ids:
            contacts = self.search([('parent_id', '=', partner.id)])

            for contact in contacts:
                lines = []
                for line in partner.ration_product_ids:
                    if line.product_template_id.id:
                        lines.append((0, 0, {
                            'product_template_id': line.product_template_id.id,
                            'reserved_quantity': line.reserved_quantity,
                        }))
                contact.write({'ration_product_ids': lines})

        return partner

    def write(self, values):
        res = super().write(values)

        if 'ration_product_ids' in values:
            for partner in self:
                if partner.is_company:
                    contacts = self.search([('parent_id', '=', partner.id)])

                    for contact in contacts:
                        contact.ration_product_ids.unlink()  # clear old
                        lines = []
                        for line in partner.ration_product_ids:
                            if line.product_template_id.id:
                                lines.append((0, 0, {
                                    'product_template_id': line.product_template_id.id,
                                    'reserved_quantity': line.reserved_quantity,
                                }))
                        contact.write({'ration_product_ids': lines})

        return res
    
    def user_dummy(self):
        pass


            