from odoo import fields, models


class PracticeTaskPatient(models.Model):
    _name = 'practice.task.patient'
    _inherits = {'res.partner': 'practice_patient_id'}
    
    practice_patient_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    total_appointments = fields.Integer(string='Appointments Count')