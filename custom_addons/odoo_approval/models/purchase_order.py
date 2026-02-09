# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    state = fields.Selection(
        selection_add=[
            ('to approve',),
            ('second_approval', 'Final Approve'),
            ('purchase',),  
        ],
        ondelete={
            'second_approval': 'set default',
        }
    )
        
    def action_approve(self):
        """Approval Request to Manager"""
        for record in self:
            if record.state != 'draft':
                continue
            
            record.state = 'to approve'
            manager_group = self.env.ref('purchase.group_purchase_manager')
            managers = manager_group.users

            for manager in managers:
                record.activity_schedule(
                    'mail.mail_activity_data_todo',
                    note=f"New Purchase Order {record.name} requires your approval.",
                    user_id=manager.id,
                    summary="Purchase Approval Needed"
                )
    # def button_confirm(self):
    #     super(PurchaseOrder,self).button_confirm()
    #     for record in self:
    #         if record.state == 'to approve':
    #             manager_group = self.env.ref('purchase.group_purchase_manager')
    #             managers = manager_group.users

    #             for manager in managers:
    #                 record.activity_schedule(
    #                     'mail.mail_activity_data_todo',
    #                     note=f"New Purchase Order {record.name} requires your approval.",
    #                     user_id=manager.id,
    #                     summary="Purchase Approval Needed"
    #                 )
                

    def _approval_allowed(self):
        """Overwrite to include custom permission approval"""
        res = super(PurchaseOrder,self)._approval_allowed()
        has_permission = self.env.user.has_group('odoo_approval.po_group_approval_permission')
        return res and has_permission
    
    def button_approve(self, *args, **kwargs):
        print(f"Approval Logic Result: {self._approval_allowed()}")
        if not self.env.user.has_group('odoo_approval.po_group_approval_permission'):
            raise UserError(_("Warning for %s: Your Permission Access Revoked! Please contact Administrator.", 
                        self.env.user.name))
        approver = self.company_id.approval_user
        if self.company_id.is_po_two_level_approval and approver:
            
            valid_orders = self.filtered(lambda order: order._approval_allowed())
            valid_orders.write({'state': 'second_approval', 'date_approve': fields.Datetime.now()})
            chief_manager_group = self.env.ref('odoo_approval.group_chief_manager')
            chief_managers = chief_manager_group.users
            for order in valid_orders:
                for chief_manager in chief_managers:
                    order.activity_schedule(
                        'mail.mail_activity_data_todo',
                        note=f"New Purchase Order {order.name} requires your approval.",
                        user_id=chief_manager.id,
                        summary="Purchase Approval Needed"
                    )
            valid_orders.action_final_approve()
            return{}
        else:
            return super(PurchaseOrder,self).button_approve(*args, **kwargs)
        
    def _final_approval_allowed(self):
        """Final Permission Approval"""
        return (
            self.company_id.is_po_two_level_approval
             and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today())
             and self.env.user.has_group('odoo_approval.po_group_approval_permission')
            or self.env.user.has_group('odoo_approval.group_chief_manager')
        )

    def action_final_approve(self):
            # 1. Loop through the records
            for order in self:
                # 2. Only process orders in the correct state
                if order.state != 'second_approval':
                    continue
                
                # 3. Check permissions
                if order._final_approval_allowed():
                    # Perform standard Odoo confirmation house-keeping
                    order.order_line._validate_analytic_distribution()
                    order._add_supplier_to_product()
                    
                    # Move to Purchase state
                    order.write({
                        'state': 'purchase', 
                        'date_approve': fields.Datetime.now()
                    })
                    order._create_picking()
                    
                    # Handle the "Lock" setting
                    if order.company_id.po_lock == 'lock':
                        order.write({'state': 'done'})
                        
                    # Add vendor to followers
                    if order.partner_id not in order.message_partner_ids:
                        order.message_subscribe([order.partner_id.id])
                else:
                    # If they clicked the button but aren't allowed
                    raise UserError("You do not have permission for Final Approval.")
                    
            return True
    

        