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
    _name = 'benin_petro.wizard.tv_impression_remise'
    
    def _getClient_id(self):
        return self._context.get('active_ids',False)[0]

    remis_id = fields.Many2one('benin_petro.tv_remise',string='print',default=_getClient_id)
    nbr_print = fields.Integer(string='Nombre ticket')
    tv_type = fields.Many2one('benin_petro.tv_type',string='Coupure')
    def save_print_remise(self):
        print self._context
        i = 0
        while i < self.nbr_print:
            self.env['benin_petro.ticket_valeur'].sudo().create({
                    'tv_type':self.tv_type.id,
                    'client':self.remis_id.tv_print.client.id,
                    'remise':self.remis_id.id,
                })
            i+=1
        print self.remis_id.montant_rest-(self.tv_type.montant * self.nbr_print)
        self.remis_id.sudo().write({
            'montant_rest':self.remis_id.montant_rest-(self.tv_type.montant * self.nbr_print)
        })

        return {
                'view_mode': 'form',
				'res_model': 'benin_petro.tv_print',
				'res_id': self.remis_id.tv_print.id,
				'type': 'ir.actions.act_window'
                }
    
    @api.constrains('nbr_print')
    def _check_number(self):
        print self.remis_id.montant_rest
        print (self.tv_type.montant * self.nbr_print)
        if self.remis_id.montant_rest < (self.tv_type.montant * self.nbr_print):
            raise ValidationError('Montant a remise insuffisant')