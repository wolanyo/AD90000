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

class recharge_par_carte(models.Model):
    _name = 'benin_petro.recharge_par_carte'

    client = fields.Many2one("res.partner",string="Client")
    carte = fields.Many2one('benin_petro.carte',string='Carte',domain=[('state','=','generee')], required=True)
    type_operation = fields.Selection([('credit','Crédit'),('debit','Débit'),],string="Type d'opération",default="credit")
    list_releve_client = fields.One2many('benin_petro.liste_releve_recharge','con',string='Liste releve carte')
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

    @api.onchange('carte','start_date','end_date','type_operation')
    def _onchange_consommateur(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()
        data = []
        if self.carte.id:
            if self.type_operation == 'credit':
                liste_recharge = self.env["benin_petro.historique"].search([("carte_sublim","=",self.carte.id),('type_op','=','Recharge carte')])
            else:
                liste_recharge = self.env["benin_petro.historique"].search([("carte_sublim","=",self.carte.id),('debit','!=',0.0)])

            for recharge in liste_recharge:
                if dateutil.parser.parse(recharge.create_date).date() >= ds and dateutil.parser.parse(recharge.create_date).date()<= de:
                    print recharge.type_op
                    if self.type_operation == 'credit':
                        montant = recharge.credit
                    else:
                        montant = recharge.debit
                    data.append({'date_recharge':recharge.create_date,'consomateur':recharge.carte_sublim.libelle.name,'montant':montant,'type_operation':recharge.type_op})
            
            return {'value':{'list_releve_client':data}}


    @api.multi
    def print_report_pdf(self):
        ds=dateutil.parser.parse(self.start_date).date()
        de=dateutil.parser.parse(self.end_date).date()

        datas = []
        data = []
        total = {}
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if self.carte.id:
            if self.type_operation == 'credit':
                liste_recharge = self.env["benin_petro.historique"].search([("carte_sublim","=",self.carte.id),('type_op','=','Recharge carte')])
            else:
                liste_recharge = self.env["benin_petro.historique"].search([("carte_sublim","=",self.carte.id),('debit','!=',0.0)])

            for recharge in liste_recharge:
                if dateutil.parser.parse(recharge.create_date).date() >= ds and dateutil.parser.parse(recharge.create_date).date()<= de:
                    print recharge.type_op
                    if self.type_operation == 'credit':
                        montant = recharge.credit
                    else:
                        montant = recharge.debit
                    data.append({'date_recharge':recharge.create_date,'consomateur':recharge.carte_sublim.libelle.name,'montant':locale.format("%d", float(montant), grouping=True),'type_operation':recharge.type_op})
                    # res[tresorier.access.name] = data
            print data
        datas = {
                'form':
                {
                    'date_debut':datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin':datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date':d1,
                    'carte':self.carte.libelle.name,
                    'type_operation':self.type_operation,
                    'transactions':data,
                    'total':total,
                }
        }
        return self.env['report'].get_action(self, 'benin_petro.etat_recharge_par_carte', data=datas)


class etat_recharge_par_carte(models.AbstractModel):
    _name = 'report.benin_petro.etat_recharge_par_carte'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_recharge_par_carte')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.etat_recharge_par_carte', docargs)
class liste_releve_recharge(models.Model):
    _name="benin_petro.liste_releve_recharge"

    con = fields.Many2one(comodel_name='benin_petro.recharge_par_carte', string='con')
    date_recharge = fields.Date(string="Date recharge")
    consomateur = fields.Char(string='Consomateur')
    numSerie = fields.Char(string='Numéro du serie')
    type_operation = fields.Char(string='Type d\'opération')
    montant = fields.Float(string='Montant')