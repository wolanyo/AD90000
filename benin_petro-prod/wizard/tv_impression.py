# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
import datetime
import math

class Tv_impression(models.TransientModel):
    _name = 'benin_petro.wizard.tv_impression'
    
    def _getClient_id(self):
        return self._context.get('active_ids',False)[0]

    print_details = fields.Many2one('benin_petro.tv_print_details',string='print',default=_getClient_id)
    nbr_print = fields.Integer(string='Nombre ticket')

    def save_print(self):
        print self._context
        if self.print_details.tv_print.state != 'valide':
            raise ValidationError('Vous ne pouvez pas générer des tickets valeur avant de valider')
        if self.nbr_print == 0:
            raise ValidationError('Merci de saisir un nombre supérieur à zéro')
        self.print_details.write({
            'print_nb':self.nbr_print,
            'imprime':self.print_details.imprime + self.nbr_print,
            'reste':self.print_details.nbr_tv - (self.print_details.imprime + self.nbr_print)
        })
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOoo"
        tv_print = self.env['benin_petro.tv_print'].sudo().search([('details','=',self.print_details.id)])
        print tv_print
        tv = self.env['benin_petro.ticket_valeur'].sudo().search([('print_id','=',tv_print.id),('print_hestory_id','=',False),('tv_type','=',self.print_details.tv_type.id)],limit=self.nbr_print)
       # print tv
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOoo"
        # for nb in range(self.nb)
        montant = self.print_details.tv_type.montant * self.nbr_print
        self.env['benin_petro.tv_print_hestory'].sudo().create({
            'tv_ids':[(4,it.id) for it in tv],
            'print_id':self.print_details.tv_print.id,
            'nb_tv':self.nbr_print,
            'tv_type':self.print_details.tv_type.id,
            'montant':montant
        })
        print '--------------------------'
        #print self.print_details
        return {
                'view_mode': 'form',
				'res_model': 'benin_petro.tv_print',
				'res_id': self.print_details.tv_print.id,
				'type': 'ir.actions.act_window'
                }
    
    @api.constrains('nbr_print')
    def _check_number(self):
        if self.nbr_print > self.print_details.nbr_tv or self.nbr_print > self.print_details.reste :
            raise ValidationError('ticket insuffisant')
