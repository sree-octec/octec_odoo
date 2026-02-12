# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    
    
    # ------------------------------------------------------------------------------
    #                                  BUTTON ACTIONS
    # -------------------------------------------------------------------------------
        
    
    def action_final_approve(self):
        pass
