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
from decimal import Decimal

class rapport_kilometrage(models.Model):
    _name = 'benin_petro.rapport_kilometrage'

    client = fields.Many2one("res.partner",string="Client")
    list_releve = fields.One2many('benin_petro.liste_releve_kilometrage','con',string='Liste releve')
    start_date = fields.Datetime(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )
    end_date = fields.Datetime(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )

    @api.onchange('client','start_date','end_date')
    def _onchange_client(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        if self.client:
            liste_kilometrage = self.env["benin_petro.kilometrage"].search([('client','=',self.client.id)])
        else:
            liste_kilometrage = self.env["benin_petro.kilometrage"].search([])
        for conso in liste_kilometrage:
            print conso.create_date
            if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                
                data.append({'date_kilometrage':conso.create_date,'carte_id':conso.carte_id,'point_vente':conso.point_vente,'produit':conso.produit,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
            #print data
        data.sort(key = lambda x:x['date_kilometrage'])
        return {'value':{'list_releve':data}}

    def print_excel_kilometrage_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'releve_kilometrage.xlsx',data=datas )


    @api.multi
    def print_report_pdf(self):
        print 555555555555555555555
        print self.start_date
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        if self.client:
            liste_kilometrage = self.sudo().env["benin_petro.kilometrage"].search([('client','=',self.client.id)])
        else:
            liste_kilometrage = self.sudo().env["benin_petro.kilometrage"].search([])
        res={}
        data = []
        for conso in liste_kilometrage:
            if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                # print conso.carte_id.owner_id.name 
                data_res_carte = []
                if conso.carte_id.owner_id.name not in res:
                    res_carte = {}
                    if 'Carte : '+str(conso.carte_id.num_serie) not in res_carte:
                        data = []
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : data
                        }
                    else:
                        data =  res_carte['Carte : '+str(conso.carte_id.num_serie)]['transcation']
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : data
                        }
                    res[conso.carte_id.owner_id.name] = res_carte
                else:
                    res_carte = {}
                    if 'Carte : '+str(conso.carte_id.num_serie) in res[conso.carte_id.owner_id.name]:
                        data =  res[conso.carte_id.owner_id.name]['Carte : '+str(conso.carte_id.num_serie)]['transcation']
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                    else:
                        data = []
                        # print res[conso.carte_id.owner_id.name]
                        # print 'Carte : '+str(conso.carte_id.num_serie)
                        res_carte = res[conso.carte_id.owner_id.name]
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : [{'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite}]
                        }

                        # print res_carte
                        res[conso.carte_id.owner_id.name] = res_carte

        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if self.client:
            client = self.client.name
        else:
            client = 'Tous'
        datas = {
            'form':
                {
                    'date_debut':str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')),
                    'date_fin':str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')),
                    'client': client,
                    'print_date':d1,
                    'transactions' : res
                }
        }
                
        return self.env['report'].get_action(self, 'benin_petro.kilometrage_report', data=datas)

class kilometrage_report(models.AbstractModel):
    _name = 'report.benin_petro.kilometrage_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.kilometrage_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.kilometrage_report', docargs)

class liste_releve_kilometrage(models.Model):
    _name="benin_petro.liste_releve_kilometrage"

    con = fields.Many2one(comodel_name='benin_petro.rapport_kilometrage', string='con')
    point_vente = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    carte_id = fields.Many2one("benin_petro.carte",string="Carte")
    produit = fields.Many2one("product.product",string="Produit")
    date_kilometrage = fields.Char(string="Date")
    type_operation = fields.Char(string="Type opération")
    kilometrage = fields.Float(string="Kilometrage")
    quantite = fields.Char(string="Quantité consommée")

