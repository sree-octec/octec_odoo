from ..helper.module import MODULE
from odoo import api, fields, models

class OctecDailyClass(models.Model):
    _name = "octec.daily_class"
    _description = "Daily Class Update"

    class_date = fields.Date(string="Date")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
    module = fields.Selection(MODULE, string="Module")
    
    subject_id = fields.Many2one("octec.subject", required=True, domain="[('session_ids.status','not in',['done', 'cancelled'])]")
    staff_id = fields.Many2one("octec.staff", required=True)
    session_ids = fields.Many2many("octec.student.session",required=True,string="Students")
    

        
