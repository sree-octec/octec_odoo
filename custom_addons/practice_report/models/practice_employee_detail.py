from odoo import api, fields, models


class PracticeEmployeeDetail(models.Model):
    _name = 'practice.employee.detail'
    _description = 'practice employee detail'
    
    
    reference_number = fields.Char(string="Reference number", required=True, read_only=True, default=lambda self: 'New')
    
    name = fields.Char(string="Name")
    image = fields.Image(string="Image")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    phone_number = fields.Char(string="Phone Number") 
    practice_project_ids = fields.Many2many('practice.project.detail')
    project_count = fields.Integer(string="Alloted Projects", compute="_compute_project_count", store=True)
    
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 
        string="Working hours", 
        default= lambda self: self.env.company.resource_calendar_id)
    
    def _compute_project_count(self):
        for rec in self:
            rec.project_count = len(rec.practice_project_ids)
    
    @api.model        
    def create(self, vals):
        if vals.get('reference_number', 'New') == 'New':
            vals['reference_number'] = self.env['ir.sequence'].next_by_code('practice.employee.detail') or 'New'
        return super(PracticeEmployeeDetail, self).create(vals)