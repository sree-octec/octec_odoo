# -*- coding: utf-8 -*-


from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    is_po_two_level_approval = fields.Boolean(string="Second Stage approval")
    approval_user = fields.Many2one('res.users', string="Choose Approver")