# -*- coding: utf-8 -*-
from openerp import http

# class SaleInvestments(http.Controller):
#     @http.route('/sale_investments/sale_investments/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_investments/sale_investments/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_investments.listing', {
#             'root': '/sale_investments/sale_investments',
#             'objects': http.request.env['sale_investments.sale_investments'].search([]),
#         })

#     @http.route('/sale_investments/sale_investments/objects/<model("sale_investments.sale_investments"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_investments.object', {
#             'object': obj
#         })