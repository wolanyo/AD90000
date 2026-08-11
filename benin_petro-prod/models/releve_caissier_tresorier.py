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

class Releve_caissier_tresorier(models.Model):
    _name = 'benin_petro.releve_cassier_tresorier'

    caissier = fields.Many2one("benin_petro.sous_chargeur",string="Cassier")
    tresorier = fields.Many2one(comodel_name='benin_petro.chargeur', string='Trésorier')
    list_releve = fields.One2many('benin_petro.liste_releve_compte','con',string='Liste releve')
    list_releve_client = fields.One2many('benin_petro.liste_releve_compte','con',string='Liste releve client')
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
    type_affect = fields.Selection([('TV','TV'),('sublime carte','SUBLIM CARTE') ] , string="Type" , default="sublime carte")


    @api.onchange('tresorier','start_date','end_date','type_affect')
    def _onchange_consommateur(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        reste_carte = 0
        if self.tresorier.id:
            liste_conso = self.env["benin_petro.historique"].search([("chargeur","=",self.tresorier.id),('type_af',"=",self.type_affect)])
            for conso in liste_conso:
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                    debit = 0
                    credit = 0
                    if conso.montant_init > conso.montant_fin:
                        debit = conso.diff
                        credit = 0
                    else:
                        credit = conso.diff
                        debit = 0
                    if conso.diff !=0 :
                        data.append({'date_releve':conso.create_date,'libelle':conso.type_op,'debit':debit,'credit':credit,'solde':conso.montant_fin,'solde_initial':conso.montant_init,'type_affect':conso.type_af})
            #print data
        data.sort(key = lambda x:x['date_releve'])
        return {'value':{'list_releve':data}}


    @api.onchange('caissier','start_date','end_date')
    def _onchange_client(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        if self.caissier.id:
            liste_conso = self.env["benin_petro.historique"].search([("sous_chargeur","=",self.caissier.id)])
            for conso in liste_conso:
                print conso.create_date
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                    debit = 0
                    credit = 0
                    if conso.montant_init > conso.montant_fin:
                        debit = conso.diff
                        credit = 0
                    else:
                        credit = conso.diff
                        debit = 0
                    if conso.diff !=0 :
                        data.append({'date_releve':conso.create_date,'libelle':conso.type_op,'debit':debit,'credit':credit,'solde':conso.montant_fin,'solde_initial':conso.montant_init})
            #print data
        data.sort(key = lambda x:x['date_releve'])
        

        return {'value':{'list_releve_client':data}}

    def print_excel_tresorier_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'releve_tresorier.xlsx',data=datas )

    @api.multi
    def print_report_tresorier_pdf(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        total = {}
        reste_carte = 0
        if self.tresorier.id:
            liste_conso = self.env["benin_petro.historique"].search([("chargeur","=",self.tresorier.id),('type_af',"=",self.type_affect)])
            print liste_conso
            for conso in liste_conso:
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                    debit = 0
                    credit = 0
                    if conso.montant_init > conso.montant_fin:
                        debit = conso.diff
                        credit = 0
                    else:
                        credit = conso.diff
                        debit = 0
                    if conso.diff !=0 :
                        data.append({'date_releve':conso.create_date,'libelle':conso.type_op,'debit': float(debit),'credit': float(credit),'solde': float(conso.montant_fin),'solde_initial': float(conso.montant_init),'type_affect':conso.type_af})
            #print data
        data.sort(key = lambda x:x['date_releve'])
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            debit += float(v["debit"])
            credit += float(v["credit"])
            solde += float(v["solde"])
            solde_initial += float(v["solde_initial"])
        total = {"debit": float(debit),"credit": float(credit),"solde": float(solde),"solde_initial": float(solde_initial)}
        print total
        datas = {
                'form':
                {
                    'date_debut':datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin':datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date':d1,
                    'tresorier':self.tresorier.access.name,
                    'type':self.type_affect,
                    'transactions':data,
                    'total':total,
                }
        }
        return self.env['report'].get_action(self, 'benin_petro.etat_releve_tresorier', data=datas)

    def print_excel_caissier_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'releve_caissier.xlsx',data=datas )

    @api.multi
    def print_report_caissier_pdf(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        total = {}
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        if self.caissier.id:
            liste_conso = self.env["benin_petro.historique"].search([("sous_chargeur","=",self.caissier.id)])
            print liste_conso
            for conso in liste_conso:
                print conso.create_date
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                    debit = 0
                    credit = 0
                    if conso.montant_init > conso.montant_fin:
                        debit = conso.diff
                        credit = 0
                    else:
                        credit = conso.diff
                        debit = 0
                    if conso.diff !=0 :
                        data.append({'date_releve':conso.create_date,'libelle':conso.type_op,'debit':float(debit),'credit': float(credit),'solde': float(conso.montant_fin),'solde_initial': float(conso.montant_init),'type_affect':conso.type_af})

            #print data
        data.sort(key = lambda x:x['date_releve']) 
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            debit += float(v["debit"])
            credit += float(v["credit"])
            solde += float(v["solde"])
            solde_initial += float(v["solde_initial"])
        total = {"debit": float(debit),"credit": float(credit),"solde": float(solde),"solde_initial": float(solde_initial)}

        datas = {
                'form':
                {
                    'date_debut':datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin':datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date':d1,
                    'caissier':self.caissier.access.name,
                    'type':self.type_affect,
                    'transactions':data,
                    'total':total,
                }
        }
        return self.env['report'].get_action(self, 'benin_petro.etat_releve_caissier', data=datas)


class etat_releve_tresorier(models.AbstractModel):
    _name = 'report.benin_petro.etat_releve_tresorier'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_releve_tresorier')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.etat_releve_tresorier', docargs)

class etat_releve_caissier(models.AbstractModel):
    _name = 'report.benin_petro.etat_releve_caissier'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_releve_caissier')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.etat_releve_caissier', docargs)

















class liste_releve_compte(models.Model):
    _name="benin_petro.liste_releve_compte"

    con = fields.Many2one(comodel_name='benin_petro.releve_compte', string='con')
    date_releve = fields.Date(string="Date d'exécution")
    libelle = fields.Char(string='Libelle')
    debit = fields.Float(string='Débit')
    credit =  fields.Float(string='Crédit')
    solde = fields.Float(string='Solde final')
    solde_initial = fields.Float(string='Solde initial')


