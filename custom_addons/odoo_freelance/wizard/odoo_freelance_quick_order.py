from odoo import api, fields, models
from odoo.exceptions import UserError

class OdooFreelanceQuickOrder(models.TransientModel):
    _name = 'odoo.freelance.quick.order'
    _description = 'Odoo Quick Order'
    
    quick_order_ids = fields.One2many('quick.order.product.line', 'freelance_quick_order_id')
    
    def action_confirm_quick_order(self): 
        self.ensure_one()
                
        quick_order_partner = self.env['res.partner'].search([('name', 'ilike', 'customer')])

        product_lines = []
        for line in self.quick_order_ids:
            available_qty = line.product_id.qty_available
            if available_qty < line.quantity:
                raise UserError(f"Stock insufficient! available {line.product_id.display_name} product is {available_qty}")
            elif line.quantity <= 0:
                raise UserError(f"Quantity for {line.product_id.name} should be greater than 0.")
            else:
                product_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity
                }))
            
        new_sale_order = self.env['sale.order'].create({
            'partner_id': quick_order_partner.id,
            'order_line': product_lines
        })
        
        new_sale_order.action_confirm()
        
        self.action_confirm_and_automate_all(new_sale_order)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'odoo.freelance.quick.order',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_confirm_and_automate_all(self, sale_order):
        pickings = sale_order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
        
        # for picking in pickings:
        #     if picking.state == 'confirmed':
        
        for _ in range(5):
            ready_pickings = pickings.filtered(lambda p: p.state == 'assigned')
            if not ready_pickings:
                to_assign = pickings.filtered(lambda p: p.state == 'confirmed')
                if to_assign:
                    to_assign.action_assign()
                else:
                    break
            
            for picking in ready_pickings:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                picking.button_validate()
            
            if not pickings:
                break

        invoices = sale_order._create_invoices()
        if invoices:
            invoices.action_post()
            journal = self.env['account.journal'].search([('type', 'in', ('bank', 'cash'))], limit=1)
            
            if journal:
                payment_wizard = self.env['account.payment.register'].with_context(
                    active_model='account.move', 
                    active_ids=invoices.ids
                ).create({
                    'journal_id': journal.id,
                    'amount': invoices.amount_total,
                    'payment_date': fields.Date.today(),
                })
                
                payment_wizard._create_payments()
                          
    
    def action_print_report(self):
        return self.env.ref('odoo_freelance.quick_order_report').report_action(self)
