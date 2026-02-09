from odoo import api, fields, models

class OctecPayment(models.Model):
    _name= "octec.payment"
    _description = " Payments Available"
    
    
    date = fields.Date(required=True)
    payment_type = fields.Selection(selection=[('staff','Staff'),('rent','Rent'),('other','Other')], required=True)
    staff_id = fields.Many2one("octec.staff")
    subject_id = fields.Many2one("octec.subject", domain="[('staff_ids.id', '=', staff_id)]")
    session_ids = fields.Many2many("octec.student.session", 
                                   domain="[('staff_id', '=', staff_id),('subject_id', '=', subject_id)]", string="Students")
    student_id = fields.Many2one(related="session_ids.student_id")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    amount = fields.Monetary(string="Fee Paid", currency_id='currency_id')
    payment_mode = fields.Selection(selection=[('google pay','Google Pay'),('phone pay','Phone Pay'),
                                              ('bank account','Bank Account'),('in hand','In Hand')], required=True)
    remark = fields.Char(string="Description")
