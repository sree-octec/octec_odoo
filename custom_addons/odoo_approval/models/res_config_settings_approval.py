# -*- coding: utf-8 -*-


from odoo import fields, models


class ResConfigSettingsApproval(models.TransientModel):
    _inherit = 'res.config.settings'
    
    is_po_two_level_approval = fields.Boolean(
            string="Second Stage approval", 
            help="Enable additional approval layer",
            related="company_id.is_po_two_level_approval",
            readonly=False
        )
    approval_user = fields.Many2one('res.users', 
                                    string="Choose Approver",
                                    related="company_id.approval_user",
                                    readonly=False)