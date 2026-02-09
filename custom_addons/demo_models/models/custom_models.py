from odoo import models, fields


class custom_models(models.Model):
  _name = "custom.models"
  _description = "demo implementation of odoo models"
  
  name = fields.Char(string="Name", required=True)            