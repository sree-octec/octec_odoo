from odoo import models, fields, api


class CustomKeyoard(models.Model):
    _name = 'custom.keyboard'
    _description = 'Custom Keyboard Details'
    
    name = fields.Char(string="Name")
    price = fields.Char(string="Price")
    
class CustomScreen(models.Model):
    _name = 'custom.screen'
    _description = 'Custom Screen Details'
    
    name = fields.Char(string="Name")
    size = fields.Integer(string="Size", digits="Size of Screen")
    
class CustomComputer(models.Model):
    _name = 'custom.computer'
    _inherits = {
        'custom.keyboard': 'keyboard_id',
        'custom.screen': 'screen_id'
    }
    
    computer_name = fields.Char(string="Name")
    brand = fields.Char(string="Brand")
    
    keyboard_id = fields.Many2one('custom.keyboard', string="Key Board", required=True, ondelete='cascade')
    screen_id = fields.Many2one('custom.screen', string='Screen', required=True, ondelete='cascade')
    
    