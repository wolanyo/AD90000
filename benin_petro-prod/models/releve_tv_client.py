# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale
import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict
import dateutil.parser

class Releve_tv_client(models.Model):
    _name = 'benin_petro.releve_tv_client'

    client = fields.Many2one("res.partner",string="Client",required=True)
    coupure = fields.Many2one('benin_petro.tv_type',string='Coupure',required=True)
    list_releve_client = fields.One2many('benin_petro.liste_releve_client','con',string='Liste releve client')
    start_date = fields.Date(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )
    end_date = fields.Date(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )
    # type_affect = fields.Selection([('TV','TV'),('sublime carte','SUBLIM CARTE') ] , string="Type" , default="sublime carte")

    @api.onchange('coupure','client','start_date','end_date')
    def _onchange_consommateur(self):
          ds=datetime.strptime(self.start_date, '%Y-%m-%d').date()
          de=datetime.strptime(self.end_date, '%Y-%m-%d').date()
          print '########################'
          print ds
          print de
          print '########################'
          data = []
          reste_carte = 0
          if self.client.id:
               liste_tv = self.env["benin_petro.ticket_valeur"].search([("client","=",self.client.id),("tv_type","=",self.coupure.id)])
               for tv in liste_tv:
                    if tv.consom:
                         if datetime.strptime(tv.consom.create_date, '%Y-%m-%d %H:%M:%S').date()>= ds and datetime.strptime(tv.consom.create_date, '%Y-%m-%d %H:%M:%S').date()<= de:
                              data.append({'date_consomation':tv.consom.create_date,'numSerie':tv.num_serie,'solde':tv.tv_type.montant,'state':tv.etat})
               

          return {'value':{'list_releve_client':data}}



class liste_releve_client(models.Model):
    _name="benin_petro.liste_releve_client"

    con = fields.Many2one(comodel_name='benin_petro.releve_tv_client', string='con')
    date_consomation = fields.Date(string="Date consomation")
    numSerie = fields.Char(string='Numéro du serie')
    solde = fields.Float(string='Solde')
    state = fields.Char(string='Status')