from odoo import api, fields, models

class OctecStudentFee(models.Model):
  _name = "octec.student.fee"
  _description = "Student Fee Details"
  
  date = fields.Date(string="Date")
  session_id = fields.Many2one("octec.student.session", string="Student")
  subject_id = fields.Many2one(related="session_id.subject_id")
  module = fields.Char(required=True)
  payment_type = fields.Selection(selection=[('fee','fee'),('refund','refund')], required=True)
  currency_id = fields.Many2one(
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
  )
  amount = fields.Monetary(string="Fee Paid", currency_id='currency_id')
  payment_mode = fields.Selection(selection=[('google pay','Google Pay'),('phone pay','Phone Pay'),
                                              ('bank account','Bank Account'),('in hand','In Hand')], required=True)
  remark = fields.Char(string="Description")
  