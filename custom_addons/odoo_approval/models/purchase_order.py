# -*- coding: utf-8 -*-


import ast
import logging


from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    # ------------------------------------------------------------------------------
    #                                  FIELDS
    # -------------------------------------------------------------------------------
    
    
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
    can_approve = fields.Boolean(compute='_compute_can_approve')
    
    
    # ------------------------------------------------------------------------------
    #                                  COMPUTE/OVERRIDDEN METHODS
    # -------------------------------------------------------------------------------
    
    def _compute_can_approve(self):
        for order in self:
            order.can_approve = order._approval_allowed()
        
    def _approval_allowed(self):
        """Overrides default approval rights to users specific in the first approver list"""
        
        self.ensure_one()
        params = self.env['ir.config_parameter'].sudo()
        first_level_approvers = params.get_param("odoo_approval.first_approval_user_ids")
        _logger.info("DEBUG: Raw parameter value from DB: %s", first_level_approvers)
        try:
            first_level_approvers_ids = ast.literal_eval(first_level_approvers) if first_level_approvers else []
        except(ValueError, SyntaxError):
            first_level_approvers_ids = []
            
        _logger.info("DEBUG: Parsed Allowed IDs: %s", first_level_approvers_ids)
        _logger.info("DEBUG: Current User ID: %s", self.env.user.id)
        
        is_standard_allowed = (
            self.company_id.po_double_validation == 'one_step'
            or (self.company_id.po_double_validation == 'two_step'
                and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today())))
        return is_standard_allowed or (self.env.user.id in first_level_approvers_ids)
        
        
    
    # ------------------------------------------------------------------------------
    #                                  BUTTON ACTIONS
    # -------------------------------------------------------------------------------
    

    def button_confirm(self):
        """ 
        Inherit confirm button to trigger activities for specific approvers 
        when the order enters the 'to approve' state.
        """
        res = super(PurchaseOrder, self).button_confirm()

        for order in self:
            if order.state == 'to approve':
                # 1. Get the list of approvers from parameters
                params = self.env['ir.config_parameter'].sudo()
                raw_ids = params.get_param("odoo_approval.first_approval_user_ids")
                
                try:
                    approver_ids = ast.literal_eval(raw_ids) if raw_ids else []
                except:
                    continue

                # 2. Schedule an activity for each selected user
                for user_id in approver_ids:
                    order.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=user_id,
                        note=_("Please review and approve this Purchase Order: %s") % order.name,
                        summary=_("Purchase Approval Required")
                    )
                
                # 3. Post a message in the chatter and notify the approvers' inboxes
                order.message_post(
                    body=_("The order is waiting for first-level approval."),
                    partner_ids=self.env['res.users'].browse(approver_ids).partner_id.ids,
                    subtype_xmlid='mail.mt_comment'
                )
        return res
        
    
    def action_final_approve(self):
        pass
