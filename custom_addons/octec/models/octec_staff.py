from odoo import api, fields, models


class OctecStaff(models.Model):
    _name= "octec.staff"
    _description = " Staffs Available"
    
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

    dept_id = fields.Many2one("octec.department", required=True)
    subject_ids = fields.Many2many("octec.subject", required=True)
    session_ids = fields.One2many("octec.student.session","staff_id")
    payment_ids = fields.One2many("octec.payment", "staff_id")