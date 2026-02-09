from odoo import models, fields

class demoUrlAction(models.Model):
  _name = "demo.url.action"
  _description = "Implement all the use cases of url actions"
  
  name = fields.Char(string="Name", required=True)
  external_link = fields.Char(string="External Link (Any Url)")
  dynamic_param = fields.Char(string="Dynamic Parameter")
  
