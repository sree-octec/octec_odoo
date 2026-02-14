# -*- coding: utf-8 -*-

import ast


from odoo import api,fields, models


class ResConfigSettingsApproval(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    # ------------------------------------------------------------------------------
    #                                  FIELDS
    # -------------------------------------------------------------------------------
    
    is_po_two_level_approval = fields.Boolean(
            string="Second Stage approval", 
            help="Enable additional approval layer",
            config_parameter="odoo_approval.is_po_two_level_approval"
        )
    first_approval_user_ids = fields.Many2many('res.users',
                                    'rel_first_approvers', 
                                    string="First Level Approver")
    second_approval_user_ids = fields.Many2many('res.users',
                                    'rel_second_approvers', 
                                    string="Second Level Approver")
    
    # ------------------------------------------------------------------------------
    #                                  SET FUNCTIONS
    # -------------------------------------------------------------------------------
    
    def set_values(self):
        super(ResConfigSettingsApproval, self).set_values()
        # Convert list of IDs to a string to store in system parameters
        self.env['ir.config_parameter'].set_param(
            "odoo_approval.first_approval_user_ids",
            self.first_approval_user_ids.ids)
        self.env['ir.config_parameter'].set_param(
            "odoo_approval.second_approval_user_ids", 
            self.second_approval_user_ids.ids
        )
        
    # ------------------------------------------------------------------------------
    #                                  GET FUNCTIONS
    # -------------------------------------------------------------------------------
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettingsApproval, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        
        first_user_ids = params.get_param("odoo_approval.first_approval_user_ids")
        second_user_ids = params.get_param("odoo_approval.second_approval_user_ids")
        
        if first_user_ids:
            res.update(first_approval_user_ids=[(6, 0, ast.literal_eval(first_user_ids))])
            
        if second_user_ids:
            # FIX: Use 'second_approval_user_ids' and 'second_user_ids' here
            res.update(second_approval_user_ids=[(6, 0, ast.literal_eval(second_user_ids))])
            
        return res
    