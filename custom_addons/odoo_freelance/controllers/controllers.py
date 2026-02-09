# -*- coding: utf-8 -*-
# from odoo import http


# class OdooFreelance(http.Controller):
#     @http.route('/odoo_freelance/odoo_freelance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_freelance/odoo_freelance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_freelance.listing', {
#             'root': '/odoo_freelance/odoo_freelance',
#             'objects': http.request.env['odoo_freelance.odoo_freelance'].search([]),
#         })

#     @http.route('/odoo_freelance/odoo_freelance/objects/<model("odoo_freelance.odoo_freelance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_freelance.object', {
#             'object': obj
#         })

