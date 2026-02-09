from ..helper.semester import SEMESTER
from odoo import api, fields, models


class OctecStudent(models.Model):
    _name= "octec.student"
    _description = " Students Available"
    
    name = fields.Char(string="Name", required=True)
    address_1 = fields.Char(string="Address Line 1", required=True)
    address_2 = fields.Char(string="Address Line 2", required=True)
    city = fields.Char(string="City", required=True)
    state = fields.Char(string="State", required=True)
    pin_code = fields.Char(string="Pin Code", required=True)
    qualification = fields.Char(string="Qualification", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    email = fields.Char(string="Email", required=True)
    photo = fields.Image()
    parent_name = fields.Char(string="Parent Name", required=True)
    parent_phone_number = fields.Char(string="Parent Number", required=True)
    college = fields.Char(string="College", required=True)
    semester = fields.Selection(SEMESTER, string="Semester")
    student_type = fields.Selection(selection=[('1','Regular'),('2','Pass Out')], required=True)
    
    scheme_id = fields.Many2one("octec.scheme", required=True)
    currency_id = fields.Many2one(related="scheme_id.currency_id")
    module_fee = fields.Monetary(related="scheme_id.module_fee")
    dept_id = fields.Many2one("octec.department", required=True)
    subject_ids = fields.Many2many("octec.subject", required=True)
    
    def action_get_students_session_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Student Session",
            "view_mode": "list,form",
            "res_model": "octec.student.session",
            "domain": [("student_id", "=", self.id)],
            "context": {"default_student_id": self.id}
    }
    
    def action_get_students_fee_payment_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Student Fee",
            "view_mode": "list,form",
            "res_model": "octec.student.fee",
            "domain": [("session_id.student_id", "=", self.id)],
            "context":{"form_view_ref":"octec_student_fee_form"}
    }