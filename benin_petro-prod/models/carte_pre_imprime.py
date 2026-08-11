# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from datetime import date, datetime, timedelta
import dateutil.relativedelta as relativedelta
from random import randint
# from keyid import keyid
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint


class benin_petro_carte_preimprime(models.Model):
    _name = 'benin_petro.carte.preimprime'
    _rec_name = 'nombre'


    nombre = fields.Char(string="Nombre des carte á générer")
    carte_ids = fields.One2many("benin_petro.carte","carte_preimprime",string="Liste des cartes", readonly=True)


    @api.model
    def create(self, vals):
        print vals
        res = super(benin_petro_carte_preimprime, self).create(vals)
        i=1
        print 'ooooooooooooooo'
        print vals.get("nombre")
        print res
        for i in range(int(vals.get("nombre"))):
            print i
            
            self.env['benin_petro.carte'].create({
                'type_carte_id': 1, 
                'libelle': False, 
                'code_pin': 0, 
                'state': 'brouillon', 
                'product_ids': [], 
                'qrcode': False, 
                'historique_sublim': [], 
                'point_vente_ids': [],
                'carte_preimprime' : res.id
            })

        return res



class benin_petro_carte_preimprime_validate(models.Model):
    _name = 'benin_petro.carte.preimprime.validate'
    _rec_name = 'carte'


    carte = fields.Many2one("benin_petro.carte",string="Carte")
    agent = fields.Many2one("benin_petro.agent",string="Agent")
