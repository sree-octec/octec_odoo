from odoo import fields, models


class PracticeProjectDetail(models.Model):
    _name = 'practice.project.detail'
    _description = 'practice project detail'
    
    name = fields.Char(string="Name")
    cost = fields.Float(string="Project Cost")
    domain = fields.Char(string="Related Area")
    start_date = fields.Date(string="Start Date")
    phase = fields.Selection([
        ('phase1', 'Phase 1'), ('phase2', 'Phase 2'), ('phase3', 'Phase 3'), ('phase4', 'phase 4')
    ], default='phase1', string="Project Phase")
    practice_employee_ids = fields.Many2many('practice.employee.detail')
    member_count = fields.Integer(string="Project Assistants", compute='_compute_member_count', store=True)
    
    def _compute_member_count(self):
        for rec in self:
            rec.member_count = len(rec.practice_employee_ids)
    