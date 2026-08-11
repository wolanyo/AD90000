# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
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


class Releve_compte(models.Model):
    _name = 'benin_petro.releve_compte'

    client_id = fields.Many2one("res.partner", string="Client")
    consommateur = fields.Many2one(comodel_name='benin_petro.carte', string='Consommateur')
    list_releve = fields.One2many('benin_petro.liste_releve_compte', 'con', string='Liste releve')
    list_releve_client = fields.One2many('benin_petro.liste_releve_compte', 'con', string='Liste releve client')

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

    @api.onchange('consommateur', 'start_date', 'end_date')
    def _onchange_consommateur(self):
        ds = dateutil.parser.parse(self.start_date).date()
        de = dateutil.parser.parse(self.end_date).date()
        data = []
        reste_carte = 0
        if self.consommateur.id:
            liste_conso = self.env["benin_petro.carte.consommation"].search([("carte_id", "=", self.consommateur.id)])

            for conso in liste_conso:
                print
                dateutil.parser.parse(conso.create_date).date()
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(
                        conso.create_date).date() <= de:
                    if conso.reste_carte:
                        reste_carte = conso.reste_carte
                    data.append({'date_releve': conso.create_date, 'libelle': 'CONSOMMATION', 'debit': conso.montant,
                                 'credit': 0, 'solde': reste_carte})
            liste_affectation = self.env["benin_petro.log"].search(
                [("carte_id", "=", self.consommateur.id), ('champ', '=', 'Solde')])
            for affect in liste_affectation:
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    credit = float(affect.new_version) - float(affect.old_version)
                    data.append({'date_releve': affect.create_date, 'libelle': 'APPROVISIONNEMENT', 'debit': 0,
                                 'credit': credit, 'solde': credit + float(affect.old_version)})
        data.sort(key=lambda x: x['date_releve'])

        return {'value': {'list_releve': data}}

    @api.onchange('client_id', 'start_date', 'end_date')
    def _onchange_client(self):
        print
        'oooooooooooooo'
        ds = dateutil.parser.parse(self.start_date).date()
        de = dateutil.parser.parse(self.end_date).date()
        data = []
        if self.client_id.id:
            liste_affectation = self.env["benin_petro.log"].search(
                [("client_id", "=", self.client_id.id), ('champ', '=', 'Solde non affecte')])
            libelle = ''
            debit = ''
            credit = ''
            solde = 0
            for affect in liste_affectation:
                print
                dateutil.parser.parse(affect.create_date).date()
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    if float(affect.old_version) > float(affect.new_version):
                        libelle = 'Approvisionnement CARTE'
                        debit = float(affect.old_version) - float(affect.new_version)
                        credit = 0
                        solde -= float(debit)
                    else:
                        libelle = 'RECHARGE'
                        debit = 0
                        credit = float(affect.new_version) - float(affect.old_version)
                        solde += float(credit)
                    print
                    solde
                    data.append(
                        {'date_releve': affect.create_date, 'libelle': libelle, 'debit': debit, 'credit': credit,
                         'solde': solde})
        data.sort(key=lambda x: x['date_releve'])

        return {'value': {'list_releve_client': data}}

    @api.multi
    def print_report_carte_pdf(self):
        ds = dateutil.parser.parse(self.start_date).date()
        de = dateutil.parser.parse(self.end_date).date()
        data = []
        total = {}
        reste_carte = 0
        if self.consommateur.id:
            liste_conso = self.env["benin_petro.carte.consommation"].search([("carte_id", "=", self.consommateur.id)])

            for conso in liste_conso:
                print
                dateutil.parser.parse(conso.create_date).date()
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(
                        conso.create_date).date() <= de:
                    if conso.reste_carte:
                        reste_carte = conso.reste_carte
                    data.append({'date_releve': conso.create_date, 'libelle': 'CONSOMMATION',
                                 'debit': float(conso.montant), 'credit': 0,
                                 'solde': float(reste_carte)})
            liste_affectation = self.env["benin_petro.log"].search(
                [("carte_id", "=", self.consommateur.id), ('champ', '=', 'Solde')])
            for affect in liste_affectation:
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    credit = float(affect.new_version) - float(affect.old_version)
                    data.append({'date_releve': affect.create_date, 'libelle': 'APPROVISIONNEMENT', 'debit': 0,
                                 'credit': float(credit),
                                 'solde': float(credit + float(affect.old_version))})
        data.sort(key=lambda x: x['date_releve'])

        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1, minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            if " " in str(v["debit"]):
                debit += float(v["debit"])
            else:
                debit += float(v["debit"])

            if " " in str(v["credit"]):
                credit += float(v["credit"])
            else:
                credit += float(v["credit"])

            if " " in str(v["solde"]):
                solde += float(v["solde"])
            else:
                solde += float(v["solde"])
        total = {"debit": float(debit),
                 "credit": float(credit),
                 "solde": float(solde)}
        
        datas = {
            'form':
                {
                    'date_debut': datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin': datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date': d1,
                    'consommateur': self.consommateur.libelle.name,
                    'transactions': data,
                    'total': total,
                }
        }
        return self.env['report'].get_action(self, 'benin_petro.etat_releve_compte_client_carte', data=datas)

    def print_excel_carte_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'suivie_compte_carte.xlsx',data=datas )

    def print_excel_client_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'suivie_compte_client.xlsx',data=datas )
    @api.multi
    def print_report_client_pdf(self):
        print 'hamadaaaaaaa'
        ds = dateutil.parser.parse(self.start_date).date()
        de = dateutil.parser.parse(self.end_date).date()
        data = []
        total = {}
        if self.client_id.id:
            liste_affectation = self.env["benin_petro.log"].search(
                [("client_id", "=", self.client_id.id), ('champ', '=', 'Solde non affecte')])
            libelle = ''
            debit = ''
            credit = ''
            solde = 0
            for affect in liste_affectation:
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    if float(affect.old_version) > float(affect.new_version):
                        libelle = 'Approvisionnement CARTE'
                        debit = float(affect.old_version) - float(affect.new_version)
                        credit = 0
                        solde -= float(debit)
                    else:
                        libelle = 'RECHARGE'
                        debit = 0
                        credit = float(affect.new_version) - float(affect.old_version)
                        solde += float(credit)
                    data.append({'date_releve': affect.create_date, 'libelle': libelle,
                                 'debit': locale.format("%d", float(debit), grouping=True),
                                 'credit': locale.format("%d", float(credit), grouping=True),
                                 'solde': locale.format("%d", float(solde), grouping=True)})
        data.sort(key=lambda x: x['date_releve'])

        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1, minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            if " " in str(v["debit"]):
                debit += float(v["debit"].replace(" ", "").replace(",", ""))
            else:
                debit += float(v["debit"])

            if " " in str(v["credit"]):
                credit += float(v["credit"].replace(" ", "").replace(",", ""))
            else:
                credit += float(v["credit"].replace(" ", "").replace(",", ""))

            if " " in str(v["solde"]):
                solde += float(v["solde"].replace(" ", "").replace(",", ""))
            else:
                solde += float(v["solde"])
        total = {"debit": locale.format("%d", float(debit), grouping=True),
                 "credit": locale.format("%d", float(credit), grouping=True),
                 "solde": locale.format("%d", float(solde), grouping=True)}

        datas = {
            'form':
                {
                    'date_debut': datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin': datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date': d1,
                    'client': self.client_id.name,
                    'transactions': data,
                    'total': total,
                }
        }
        return self.env['report'].get_action(self, 'benin_petro.etat_releve_compte_client', data=datas)


class etat_releve_compte_client(models.AbstractModel):
    _name = 'report.benin_petro.etat_releve_compte_client'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_releve_compte_client')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
        }

        return report_obj.render('benin_petro.etat_releve_compte_client', docargs)


class etat_releve_compte_client_carte(models.AbstractModel):
    _name = 'report.benin_petro.etat_releve_compte_client_carte'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_releve_compte_client_carte')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
        }

        return report_obj.render('benin_petro.etat_releve_compte_client_carte', docargs)


class liste_releve_recharge(models.Model):
    _name = "benin_petro.liste_releve_recharge"

    con = fields.Many2one(comodel_name='benin_petro.recharge_par_carte', string='con')
    date_recharge = fields.Date(string="Date recharge")
    consomateur = fields.Char(string='Consomateur')
    numSerie = fields.Char(string='Numéro du serie')
    type_operation = fields.Char(string='Type d\'opération')
    montant = fields.Float(string='Montant')


class liste_releve_compte(models.Model):
    _name = "benin_petro.liste_releve_compte"

    con = fields.Many2one(comodel_name='benin_petro.releve_compte', string='con')
    date_releve = fields.Date(string="Date d'exécution")
    libelle = fields.Char(string='Libelle')
    debit = fields.Float(string='Débit')
    credit = fields.Float(string='Crédit')
    solde = fields.Float(string='Solde')
