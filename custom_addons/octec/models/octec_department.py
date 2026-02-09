from odoo import api, fields, models

class OctecDepartment(models.Model):
    _name= "octec.department"
    _description = " Departments Available"
    _rec_name = "dept_name"
    
    dept_name = fields.Char(string="Department Name", required=True)
    dept_description = fields.Char(string=" Department Description", required=True)