# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class Session(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/api/getCarteBynum/<int:num_serie>', auth='public', type='http')
    def index(self, num_serie=None):
        print "666666666666666"
        print num_serie
        carte =  request.env['benin_petro.carte'].search([('num_serie','=',num_serie)])
        # # sales = []
        vals = {
                'id': carte.id,
                'num_serie': carte.num_serie
            }
        # print vals
        # # sales.append(vals)
        # # data = {'status': 200, 'response': sales, 'message': 'Sale(s) returned'}
        # # print data
        # # return vals
       
        # output = {
        #     'results':{
        #         'response': vals,
        #         'code':200,
        #         'message':'OK'
        #     }
        # }
        return json.dumps(vals, indent=4)
        # return '<script>window.json = {"client":[{"id":3,"name":"Administrator"},{"id":9,"name":"eza"},{"id":7,"name":"hamada baraka 3elik"},{"id":6,"name":"test 1"}]};</script>'






