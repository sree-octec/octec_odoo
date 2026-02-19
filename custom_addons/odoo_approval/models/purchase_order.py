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
        params = self.env['ir.config_parameter'].sudo()
        initial_raw = params.get_param("odoo_approval.first_approval_user_ids")
        final_raw = params.get_param("odoo_approval.second_approval_user_ids")
        
        try:
            initial_ids = ast.literal_eval(initial_raw) if initial_raw else []
            final_ids = ast.literal_eval(final_raw) if final_raw else []
        except:
            initial_ids = final_ids = []

        for order in self:
            if order.state == 'to approve':
                order.can_approve = order._approval_allowed(initial_approval_allowed_ids=initial_ids)
            elif order.state == 'second_approval':
                order.can_approve = order._final_approval_allowed(final_approval_allowed_ids=final_ids)
            else:
                order.can_approve = False
                

    def _approval_allowed(self, initial_approval_allowed_ids=None):
        self.ensure_one()
        
        # Use cached IDs if provided, otherwise fetch (fallback)
        if initial_approval_allowed_ids is None:
            params = self.env['ir.config_parameter'].sudo()
            initial_approval_raw_ids = params.get_param("odoo_approval.first_approval_user_ids")
            try:
                initial_approval_allowed_ids = ast.literal_eval(initial_approval_raw_ids) if initial_approval_raw_ids else []
            except:
                initial_approval_allowed_ids = []

        is_standard_allowed = (
            self.company_id.po_double_validation == 'one_step'
            or (self.company_id.po_double_validation == 'two_step'
                and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today())))
                    
        return is_standard_allowed or (self.env.user.id in initial_approval_allowed_ids)
    
    
    def _final_approval_allowed(self, final_approval_allowed_ids=None):
            """
            Checks if the current user is allowed to give final approval.
            Includes a check for the minimum double validation amount.
            """
            self.ensure_one()
            
            # 1. Fetch IDs if they weren't passed from the compute method
            if final_approval_allowed_ids is None:
                params = self.env['ir.config_parameter'].sudo()
                final_approval_raw_ids = params.get_param("odoo_approval.second_approval_user_ids")
                try:
                    # Use ast to safely parse the string list from System Parameters
                    final_approval_allowed_ids = ast.literal_eval(final_approval_raw_ids) if final_approval_raw_ids else []
                except (ValueError, SyntaxError):
                    final_approval_allowed_ids = []
            _logger.info(f"final approval ids:{final_approval_allowed_ids}")

            # 2. Check the minimum amount (Standard Odoo Double Validation logic)
            is_standard_allowed = (self.amount_total < self.env.company.currency_id._convert(
                        self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                        self.date_order or fields.Date.today()))
            _logger.info(f"cheking final approval: {is_standard_allowed}................")
                        
            # 3. Logic: Allowed if order is under the limit OR user is a designated final approver
            return is_standard_allowed or (self.env.user.id in final_approval_allowed_ids)
        
        
    
    # ------------------------------------------------------------------------------
    #                                  BUTTON ACTIONS
    # -------------------------------------------------------------------------------
    
    
    def button_approve(self, force=False):
        is_two_level = self.env['ir.config_parameter'].sudo().get_param("odoo_approval.is_po_two_level_approval")
        _logger.info(f"{is_two_level} approval............")
        
        for order in self:
            if is_two_level and order.state == 'to approve':
                _logger.info(f"{self.env.user.name} approved. Moving to Second Approval.")
                order.write({'state': 'second_approval'})
                
            elif order.state == 'second_approval':
                if order._final_approval_allowed():
                    _logger.info(f"{self.env.user.name} approved. Finalizing PO.")
                    super(PurchaseOrder, order).button_approve(force=force)
                else:
                    raise UserError("Only an authorized person can provide the final approval.")

            else:
                _logger.info("checking approval............")
                super(PurchaseOrder, order).button_approve(force=force)
                
        return True

    def button_confirm(self):
            res = super(PurchaseOrder, self).button_confirm()
            # Optimization: Fetch settings ONCE before starting the loop
            params = self.env['ir.config_parameter'].sudo()
            initial_approval_raw_ids = params.get_param("odoo_approval.first_approval_user_ids")
            try:
                approver_ids = ast.literal_eval(initial_approval_raw_ids) if initial_approval_raw_ids else []
            except:
                approver_ids = []

            if not approver_ids:
                return res

            # Pre-fetch partner IDs to avoid repeated browse/mapped calls inside loop
            approver_partners = self.env['res.users'].sudo().browse(approver_ids).partner_id.ids

            for order in self.filtered(lambda o: o.state == 'to approve'):
                # Schedule activity
                for user_id in approver_ids:
                    order.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=user_id,
                        note=_("Approval Required for %s") % order.name,
                        summary=_("Purchase Approval Required")
                    )
                
                order.message_post(
                    body=_("Waiting for manager approval."),
                    partner_ids=approver_partners,
                    subtype_xmlid='mail.mt_comment'
                )
            return res
        
    
    def action_final_approve(self):
        # 1. Permission Check
        final_approval_orders = self.filtered(lambda order: order._final_approval_allowed())
        
        if not final_approval_orders:
            raise UserError("You do not have the required permissions for final approval.")

        for order in final_approval_orders:
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            order.write({
                'state': 'purchase',
                'date_approve': fields.Datetime.now(),
            })
            order._create_picking()
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])

            if order.company_id.po_lock == 'lock':
                order.write({'state': 'done'})

        return True