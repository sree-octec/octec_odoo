from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    approval_state = fields.Selection([
        ("draft", "Draft"),
        ("first", "First Level Approved"),
        ("second", "Final Approved"),
        ("posted", "Posted"),
    ], string="Approval Status", default="draft", tracking=True)

    def action_send_for_approval(self):
        for record in self:
            record.approval_state = "first"

    def action_first_approve(self):
        for record in self:
            record.approval_state = "second"

    def action_second_approve(self):
        for record in self:
            record.approval_state = "posted"
