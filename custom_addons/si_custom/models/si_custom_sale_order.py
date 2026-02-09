from odoo import models, fields, api


class SiCustomSaleOrder(models.Model):
    _inherit = 'sale.order'
    
    purchase_order_reference = fields.Char(string="PO Reference")
    po_count = fields.Integer(string="Purchase Orders", compute="_compute_purchase_order")
    
    @api.depends('purchase_order_reference')
    def _compute_purchase_order(self):
        for rec in self:
            if rec.purchase_order_reference:
                rec.po_count = self.env['purchase.order'].search_count([('po_reference', '=', self.purchase_order_reference)])
            else:
                rec.po_count = 0
    
    def action_view_po(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Product Orders",
            "view_mode": "list",
            "res_model": "purchase.order",
            "domain": [("po_reference", "=", self.purchase_order_reference)],
            "context":{"form_view_ref":"purchase.purchase_order_view_tree"}
    }