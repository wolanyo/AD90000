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
from num2words import num2words
import pandas as pd

class benin_petro_point_vente(models.Model):
    _name = 'benin_petro.point.vente'

    _rec_name = 'libelle'
    _description = ''

    @api.multi
    def setToActive(self):
        self.ensure_one()
        self.state="activee"
	self.date_activation=fields.datetime.now()

    @api.multi
    def setToSuspendu(self):
        self.ensure_one()
        print "###########"
        #Load the data of csv
        df = pd.read_csv('/opt/odoo/odoo-10.0/bp/benin_petro/models/import_x.csv', encoding ='latin1', sep=';', engine='python', names=['0','num_serie'])
        
        # Print the Dataframe
        i=0
        for index, row in df.iterrows():
            i=i+1
            # tv_type = row['tv_type']
            num_serie = row['num_serie']
            # num_incr = row['num_incr']
            # client = row['client']
            print str(i)+ str('/')
            tv = self.env["benin_petro.ticket_valeur"].search([('num_serie','=',str(num_serie))])
            if tv:
                tv.etat = 'util'
            # c = self.env["res.partner"].search([('name','=',str(client))])
            # if not c:
            #     o = {
            #         'name' : client,
            #         'phone' : '55555555'
            #     }
            #     c = self.env['res.partner'].sudo().create(o)
            # print str(i)+ str('/') + str(c[0].id)
            # if(len(tv) == 0):
            #     obj = {
            #         'tv_type': tv_type,
            #         'client':int(c[0].id),
            #         'num_serie' : str(num_serie),
            #         'num_serie_incr' : str(num_incr).zfill(10),
            #         'num_incr': num_incr,
            #         'imported_state': True
            #     }
            #     #print(obj)
            #     self.env['benin_petro.ticket_valeur'].sudo().create(obj)



#         liste = self.env["benin_petro.log"].search([('champ','=','Solde non affecte')])
#         for l in liste:
#             user =  self.env["res.users"].search([('name','=',l.acteur_name)])
#             sous_chargeur =  self.env["benin_petro.sous_chargeur"].search([('access','=',user.id)])
#             res = self.env['benin_petro.historique'].create({
# #            qq = {
#             'type_op':'Recharge compte client',
#             'client_id':self.env["benin_petro.carte"].search([('id','=',l.carte_id.id)]).owner_id.id,
#             'type_af':'sublime carte',
#             'sous_chargeur':sous_chargeur.id,
#             'carte_sublim':l.carte_id.id,
#             'debit':abs(float(l.new_version)-float(l.old_version)),
#             'credit':0,
#             'diff' : abs(float(l.new_version)-float(l.old_version)),
#             'solde_carte':l.new_version,
#             'create_date':l.create_date
#             })
#             self.env.cr.execute("""UPDATE benin_petro_historique SET create_date = '"""+l.create_date+"""' where id = %s""" % (res.id))
#            print qq

	# self.date_suspension=fields.datetime.now()

    @api.multi
    def setToAnnule(self):
        self.ensure_one()
        self.state="annule"
	self.date_annulation=fields.datetime.now()

    libelle = fields.Char(string="Code")
    name = fields.Char(string="Point de vente")
    adress = fields.Text(string="Adresse")
    historique_ids = fields.One2many("benin_petro.carte.consommation","carte_id",string="Historiques", readonly=True)
    agent_ids = fields.One2many("benin_petro.agent","point_vente_id",string="Agents")
    state = fields.Selection([('brouillon','Brouillon'),('activee','Activé'),('suspendu','Suspendu'),('annule','Annulé')] , string="Statut" , default="activee")
    type = fields.Selection([('avec','Avec Boutique'),('sans','Sans Boutique') ] , string="Boutique" , default="avec")
    date_activation = fields.Datetime("Date d'activation", readonly=True)
    date_suspension = fields.Datetime("Date de suspension", readonly=True)
    date_annulation = fields.Datetime("Date d'annulation", readonly=True)
    log_ids = fields.One2many("benin_petro.log","point_vente_id",string="Historiques", readonly=True)
    transaction_ids_card = fields.One2many("benin_petro.carte.consommation","point_vente_id_tv",string="Historiques", readonly=True,domain=[('type_vente','=','Vente par SUBLIME CARTE')])
    transaction_ids_tv = fields.One2many("benin_petro.carte.consommation","point_vente_id_card",string="Histormljiques", readonly=True,domain=[('type_vente','=','Vente par TV')])
    Total_vente = fields.Float(string="Total des ventes",readonly=True)
    total_vente_tv = fields.Float(string="TOTAL VENTE TV",readonly=True)
    total_vente_easy_card = fields.Float(string="VENTE SUBLIME CARTE",readonly=True)
    promoteur = fields.Many2one("res.partner",string="Promoteur")
    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte annalytic')
    hestory_ids = fields.One2many('benin_petro.tv_station_hestory','tv_station',string='Ventes')
    point_vente_id = fields.Many2one("benin_petro.carte",string="Point de vente")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    



    @api.multi
    def write(self, vals):
	for carte in self:
		logs = []
		acteurName = self.env.user.name
		if vals.get("acteur_name",False):
			acteurName = vals.get("acteur_name",False)
		
		if vals.get("libelle",False):
		   logs.append(self.log(self.id,acteurName,self.libelle,vals.get("libelle",False),"Libellé"))
		
		if vals.get("adress",False):
		   logs.append(self.log(self.id,acteurName,self.adress,vals.get("adress",False),"Adresse"))

		if vals.get("type",False):
		   logs.append(self.log(self.id,acteurName,self.type,vals.get("type",False),"Type"))


		if logs:
			vals['log_ids'] = logs
	
	return super(benin_petro_point_vente, self).write(vals)

    def log(self,ObjtId,acteurName,old_version,new_version,champ):
	return (0,0, {
				"point_vente_id" : ObjtId,
				"acteur_name" : acteurName,
				"old_version" : old_version,
				"new_version" : new_version,
				"champ" : champ,
			})



class StationHestory(models.Model):
    _name = "benin_petro.tv_station_hestory"
    _order= "create_date desc"

    tv_station = fields.Many2one('benin_petro.point.vente',string='Tv Station')
    type_payment = fields.Selection([('Espece','Espece'),('cheque','Cheque'),('Note de credit','Note de crédit')],string="Type de paiment")
    montant = fields.Float(string='Montant')
    #ticket_ids = fields.One2many('benin_petro.tv_station_line','payement_id',string='Tickets')
    #carte_ids = fields.One2many('benin_petro.easycard_station_line','payement_id',string='Cartes')
    state = fields.Selection([('cancel','Annulé'),('valide','Validé')],default='valide')
    datec=fields.Date(string='Paiement  jusqu\'au')
    type_vente=fields.Selection([('Vente par SUBLIME CARTE','Vente par SUBLIME CARTE'),('Vente par TV','Vente par TV')],string="Type de vente",required=True)
    montant_commission = fields.Float(string='Montant commission')
    montant_net = fields.Float(string='Montant net')
    facture_num = fields.Char("Numéro de facture")

    def print_report(self):
        return self.env['report'].get_action(self,'benin_petro.facture_promoteur')

    def getMontantWords(self):
       # mnt = self.remise_ids.montant + self.montant
        text = num2words(self.montant_net, lang='fr')
        return text.upper()
    
