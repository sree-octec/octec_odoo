from odoo import api, fields, models

class OdooFreelanceCustomerChange(models.TransientModel):
    _name = 'odoo.freelance.customer.change'
    _description = 'Odoo Partner change'
    
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    
    def action_update_customer(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        if not active_id:
            return {'type': 'ir.actions.act_window_close'}
        
        sale_order = self.env['sale.order'].browse(active_id)
        new_partner = self.partner_id
        
        addr = new_partner.address_get(['invoice', 'delivery'])
        commercial_partner = new_partner.commercial_partner_id
        
        fpos = self.env['account.fiscal.position'].with_company(
            sale_order.company_id
        )._get_fiscal_position(new_partner)
        

        sale_order.sudo().write({
            'partner_id': new_partner.id,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'payment_term_id': commercial_partner.property_payment_term_id.id,
            'fiscal_position_id': fpos.id if fpos else False
        })
        sale_order.with_context(bypass_pricelist_check=True).sudo().write({
            'pricelist_id': commercial_partner.property_product_pricelist.id,

        })

        if sale_order.state == 'sale':
            sale_order.sudo()._recompute_taxes()
            sale_order.sudo()._recompute_prices()
        

        pickings = sale_order.picking_ids.filtered(lambda p: p.state not in ['cancel'])
        if pickings:
            pickings.sudo().write({
                'partner_id': addr['delivery']
            })
            pickings.move_ids.sudo().write({'partner_id': addr['delivery']})
        invoices = sale_order.invoice_ids
        if invoices:
            invoices.with_context(skip_readonly_check=True).sudo().write({
                'partner_id': new_partner.id
            })
            
        return {'type': 'ir.actions.act_window_close'}