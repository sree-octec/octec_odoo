from odoo import api, fields, models

class StudentSession(models.Model):
    _name = "octec.student.session"
    _description = "Student session on subject"
    
    student_id = fields.Many2one("octec.student", string="Student")
    name = fields.Char(related="student_id.name")
    
    subject_id = fields.Many2one("octec.subject", string="Subject", required=True)
    staff_id = fields.Many2one("octec.staff", string="Staff", required=True, domain="[('subject_ids.id', '=', subject_id)]")

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    module_count = fields.Integer()
    selected_modules = fields.Char(required=True,default='')
    currency_id = fields.Many2one(related="student_id.scheme_id.currency_id")
    module_fee = fields.Monetary(related="student_id.module_fee")
    discount = fields.Float(string="Discount(%)")
    total_fee = fields.Float(string="Total Fee",compute="_compute_total_fee")
    status = fields.Selection(selection=[('new','New'),('half','Half'),('done','Done'),('cancelled','Cancelled')],required=True)
    
    @api.depends('discount','module_count','module_fee')
    def _compute_total_fee(self):
      for rec in self:
        rec.total_fee = 0
        if rec.module_count and rec.module_fee:
          if rec.discount:
            rec.total_fee = (rec.module_count*rec.module_fee*(100-rec.discount))/100
          else:
            rec.total_fee = rec.module_count*rec.module_fee

    