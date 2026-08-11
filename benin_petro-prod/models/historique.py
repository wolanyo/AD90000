# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import  ValidationError
from lxml import etree
from num2words import num2words
from datetime import datetime
from datetime import date
import time
import locale
from datetime import timedelta

class historique(models.Model):
    _name = 'benin_petro.historique'
    _order = 'create_date desc'
    
    # @api.one
    # def _calc(self):
    #     print 'CAAAAAAAAAAAALc'
    #     print self.montant_init-self.montant_fin
    #     return  self.montant_init-self.montant_fin

    montant_init = fields.Float(string='Montant initiale')
    montant_fin =  fields.Float(string='Montant finale')
    chargeur =     fields.Many2one(comodel_name='benin_petro.chargeur')
    type_op = fields.Char(string='Type d\'opération')
    sous_chargeur = fields.Many2one(comodel_name='benin_petro.sous_chargeur',readonly=True)
    sous_chargeur_sublim = fields.Many2one('benin_petro.sous_chargeur',compute='_getRech')
    sous_chargeur_tv = fields.Many2one('benin_petro.sous_chargeur',compute='_getRech')
    chargeur_sublim = fields.Many2one('benin_petro.sous_chargeur',compute='_getRech_chargeur')
    chargeur_tv = fields.Many2one('benin_petro.sous_chargeur',compute='_getRech_chargeur')
    carte_sublim = fields.Many2one('benin_petro.carte')
    diff = fields.Float(string='Montant affecté',readonly=True)
    verse_validate= fields.Boolean(default=False)
    tres_validate=fields.Boolean(default=False)
    versement_id=fields.Many2one(comodel_name='benin_petro.versement')
    client_id = fields.Many2one(comodel_name='res.partner')
    moyen_de_paiement =  fields.Char(string='Moyen de paiement')
    detail_id=fields.Many2one('benin_petro.historique_ben_detail')
    state = fields.Selection(string='Etat', selection=[('a credit', 'A crédit'),('partiellement payer', 'Partiellement payer '),('valide', 'Entièrement payer'), ('annule', 'Annulé')],default='valide')
    produit = fields.Many2one(comodel_name='product.product')
    facture_num = fields.Char("Numéro de facture")
    document = fields.Binary(string='Pièce jointe')
    liste_paiement = fields.One2many('benin_petro.paiement_reste_client','historique_id',string='Liste paiement')
    reste =  fields.Float(string='Montant resté')
    numero_cheque = fields.Char(string='Numéro de chèque')
    quitance_tva = fields.Selection([('OUI','OUI'),('NON','NON')],string="Quittance TVA ramené?",default="NON")
    numero_quitance_tva = fields.Char(string='Numéro de quittance')
    type_af = fields.Selection([('TV','TV'),('sublime carte','sublime carte')],string="Type",default="TV")
    debit =  fields.Float(string='Débit')
    credit =  fields.Float(string='Crédit')
    solde_carte =  fields.Float(string='solde carte')
    demande_credit = fields.Many2one(comodel_name='benin_petro.demande_credit')
    num_recharge = fields.Char('Numéro de la recharge')
    create_date = fields.Datetime('Order Date',readonly=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    gerant = fields.Many2one(comodel_name='benin_petro.agent')
    
    # flag = fields.Boolean(string='',default=False)
    def getMontantWords(self):
        print self.diff
       # mnt = self.remise_ids.montant + self.montant
        text = num2words(self.diff, lang='fr')
        print text
        return text.upper()
    def getDate(self):
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        print d1
        return d1

    @api.multi
    def _getRech(self):
        for s in self:
            #s.sous_chargeur = s.sous_chargeur_id
            s.sous_chargeur_sublim = s.sous_chargeur.id
            s.sous_chargeur_tv = s.sous_chargeur.id

    @api.multi
    def _getRech_chargeur(self):
        for s in self:
            print s
            #s.sous_chargeur = s.sous_chargeur_id
            s.chargeur_sublim = s.chargeur.id
            s.chargeur_tv = s.chargeur.id

    # @api.model
    # def create(self, values):
    #     if values['flag']==True:
    #         return super(historique, self).create(values)
    #     else :
    #         raise ValidationError("Vous n'avez pas le droit d'effectuer cette opération")


    # def fields_view_get(self,view_id=None, view_type='form',toolbar=False, submenu=False):
    #     res = super(historique, self).fields_view_get( view_id=view_id, view_type=view_type,toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     if view_type == 'form' and [0==1]:
    #         for node_form in doc.xpath("//form"):
    #             node_form.set("create", 'false')
    #     res['arch'] = etree.tostring(doc)
    #     return res
        
    # @api.model
    # def default_get(self, fields):
	# 	res = super(historique, self).default_get(fields)     
	# 	if  self.env.user.has_group('base.group_system'):
	# 		return res
	# 	else :
	# 		raise ValidationError("Vous n'avez pas le droit d'effectuer cette opération")


class historique_ben_detail(models.Model):
    _name="benin_petro.historique_ben_detail"
    _rec_name='type_de_recharge'
    tva_init=fields.Float(string='')
    montant_bonus=fields.Float(string='')
    prix_ht=fields.Float(string='')
    prix_init=fields.Float(string='')
    qte = fields.Float(string='')
    montant_hor_taxes = fields.Float(string='')
    tva = fields.Float(string='')
    montant_ttc = fields.Float(string='')
    montant_a_recharge_remise = fields.Float(string='')
    type_de_recharge = fields.Char(string='Produit')
    historique_id = fields.Many2one(comodel_name='detail_id', string='')



class historique_ben_detail(models.Model):
    _name="benin_petro.paiement_reste_client"

    montant_credit = fields.Char(string='Montant à payer')
    montant_reste = fields.Char(string='Montant reste')
    montant_deja_paye = fields.Char(string='Montant déja payé')
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',required=True,selection=[('cheque', 'Chèque'), ('especes', 'Espèces'),('versement','Versement')])
    historique_id = fields.Many2one(comodel_name='benin_petro.historique')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)

    def print_report(self):
        return self.env['report'].get_action(self,'benin_petro.facture_paiment_acredit')

    def getMontantWords(self):
       # mnt = self.remise_ids.montant + self.montant
        print '##################'
        print (self.montant_credit).replace(" ", "")
        print '##################'
        text = num2words(float((self.montant_credit).replace(" ", "")), lang='fr')
        return text.upper()
    
        
