# from odoo import http


# class Ausencias(http.Controller):
#     @http.route('/ausencias/ausencias', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ausencias/ausencias/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ausencias.listing', {
#             'root': '/ausencias/ausencias',
#             'objects': http.request.env['ausencias.ausencias'].search([]),
#         })

#     @http.route('/ausencias/ausencias/objects/<model("ausencias.ausencias"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ausencias.object', {
#             'object': obj
#         })
