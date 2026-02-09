from odoo import fields, models


class QuickOrderMailWizard(models.TransientModel):
    _name = 'quick.order.mail.wizard'
    _description = 'Quick Order Mail Wizard'
    
    email_id = fields.Char(string="Email", required=True)
    
    def action_quick_order_send_mail(self):
        self.ensure_one()
        template = self.env.ref('odoo_freelance.quick_order_mail_template')
        template.send_mail(self.id, force_send=True)
        return {'type': 'ir.actions.act_window_close'}
    