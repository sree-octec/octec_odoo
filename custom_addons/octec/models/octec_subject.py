from ..helper.semester import SEMESTER
from odoo import api, fields, models

class OctecSubject(models.Model):
    _name= "octec.subject"
    _description = " Subjects Available"
    _rec_name = "name"
    
    name = fields.Char(string="Subject Name", required=True)
    semester = fields.Selection(SEMESTER, string="Semester")
    scheme_id = fields.Many2one("octec.scheme", required=True)
    dept_id = fields.Many2one("octec.department", required=True)
    session_ids = fields.One2many("octec.student.session","subject_id")
    staff_ids = fields.Many2many("octec.staff", required=True)