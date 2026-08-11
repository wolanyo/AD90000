# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
import datetime
import math

class benin_petro_recharger_compte_client(models.TransientModel):
    _name = 'benin_petro.wizard.recharger.compte.client'
    _rec_name = 'id'
    _description = 'New Description'

    def _getClient_id(self):
        return self._context.get('active_ids',False)[0]

    def _getsolde(self):
        return self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)]).montant_plafond

   

    @api.onchange('client_id')
    def _onchange_client(self):
	self.update({
		'solde': self.client_id.solde_compte_hide
	})


    client_id = fields.Many2one("res.partner",string="Client",default=_getClient_id)
    solde = fields.Float(string='Solde non affecté',readonly=True ,compute="_getSolde" ,store=True)
    montant = fields.Float(string='Montant à recharger',required=True)
    montant_remise = fields.Float(string='Montant remise accorde')
    solde_m = fields.Float(string='Votre solde',default=_getsolde)
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',required=True,selection=[('cheque', 'Chèque'), ('especes', 'Espèces'),('versement','Versement'),('A credit','à crédit'),('virement', 'Virement')])
    type_de_recharge= fields.Selection(string='Type  de recharge',
    selection=[(1, 'ESSENCE'), (3, 'GASOIL'),(4,'PETROLE'),(5,' DIVERS PRODUITS BENIN PETRO')],required=True)
    client_type = fields.Selection([('Oui','Oui'),('Non','Non')],string="TVA retenue à la source",dafault="Non")
    document = fields.Binary(string='Piece jointe')
    numero_cheque = fields.Char(string='Numéro de chèque')
    quitance_tva = fields.Selection([('OUI','OUI'),('NON','NON')],string="Quittance TVA ramené?",default="NON")
    numero_quitance_tva = fields.Char(string='Numéro de quittance')
    #demande = fields.Many2one("benin_petro_crm.demande_client",string="Demande client")
    

    @api.multi
    def save_recharger(self):
        print "sssssssssssssssssss"
        print "xxxxxxxxxxxxxxxxxx"
        print "sssssssssssssssssss"
        #print self.
        #start oussama's code
        print self.client_type
        if  True:
            montant_bonus = 0
            montant_a_pa = 0
            # if self.client_id.client_type == 'client_acc' :
            #     montant_bonus = self.montant *( self.client_id.valuer_a_accorde/100)
            #     montant_a_pa = self.montant - montant_bonus

            # #end oussama's code
            # print self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.uid)]).id
            # print self.env.uid
            
            print 'TTTTTTTTTTTTTTEST'
            if self.montant <= 0:
                raise ValidationError(_("Merci de renseigner un montant supérieur à zéro"))
            
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)])
            print self.env.user.id
            print po
            if self.montant<=po.montant_plafond:
                m_init =self.montant
                montant = self.client_id.solde_compte_hide + self.montant+self.montant_remise
                self.client_id.solde_compte_hide = montant
                body = """Merci de noter que votre compte vient d'etre credite par un montant de """+str(self.montant)+"""
                Votre solde actuel du compte est : """+str(montant)
                Subject = "BENIN PETRO"
                mobile = self.client_id.mobile
                mailsto =  self.client_id.email  
                # try:
                #     if mailsto:
                #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
                # except ApiException as e:
                #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)

                montant_bonus = 0
                montant_a_pa = 0
                TVA=0
                montant_a_recharge_remise=0
                montant_hor_taxes=0
                qte=0

                if self.client_id.client_type == 'client_acc' :
                    montant_bonus = self.montant * 0.01
                    # montant_a_pa = self.montant - montant_bonus
                # prix_init=self.env['product.product'].search([('id','=',1)]).lst_price
                qte=1
                
            
                tva_l=self.env['account.tax'].search([('name','=','TVA - ESSENCE')])
                if self.type_de_recharge==1:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - ESSENCE')])
                elif  self.type_de_recharge==3:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - GASOIL')])
                elif  self.type_de_recharge==4:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - PETROLE')])
                elif  self.type_de_recharge==5:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - DIVERS PRODUIT')])
                # TVA = float((self.montant / prix_init))*float(tva_l.amount)

                montant_a_recharge_remise=0
            
                # print '88888888888888888888888aaaa'
                last_historique = self.env['benin_petro.historique'].search([('type_op','=','Recharge SUBLIME CARTE')],order='create_date desc')
                dt = datetime.datetime.today()
                day = dt.day
                month = '%02d' % dt.month
                year = dt.year
                date_format = str(day)+str(month)+str(year)
                if last_historique:
                    facture_num = last_historique[0].facture_num
                    print facture_num
                    facture_num = facture_num.split("/",1)[1]
                    print facture_num
                    if facture_num:
                        facture_num = int(facture_num)+1
                        facture_num = str(date_format)+str("/")+str(int(facture_num)+1)
                else:
                    facture_num = date_format+"/1"
                num_recharge = 'zzzzzzzzzz'
                laste_recharge = self.env['benin_petro.historique'].sudo().search([('type_op','in',['Recharge compte client','Vente de tv']),('num_recharge','!=',False)],order='create_date desc')

                if laste_recharge:
                    if laste_recharge[0].num_recharge:
                        num_recharge = 'V%06d' % (int(laste_recharge[0].num_recharge.split("V")[1]) + 1)
                    else:
                        num_recharge = 'V%06d' % (1)
                else:
                    num_recharge = 'V%06d' % (1)

                state = 'valide'
                if self.moyen_de_paiement == 'cheque':
                    moyen_de_paiement = 'Chèque' 
                if self.moyen_de_paiement == 'especes':
                    moyen_de_paiement = 'Espèces'
                if self.moyen_de_paiement == 'versement':
                    moyen_de_paiement = 'Versement'
                if self.moyen_de_paiement == 'virement':
                    moyen_de_paiement = 'virement'
                if self.moyen_de_paiement == 'A credit':
                    moyen_de_paiement = 'A crédit'
                    state = 'a credit'

                res = self.env['benin_petro.historique'].create({
                    'montant_init':po.montant_plafond,
                    'montant_fin':po.montant_plafond-m_init,
                    'type_op':'Recharge compte client',
                    'diff':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'reste':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'client_id':self.client_id.id,
                    'moyen_de_paiement':moyen_de_paiement,
                    'prix_init':self.type_de_recharge,
                    'facture_num' : facture_num,
                    'document' : self.document,
                    'produit' : self.env['product.product'].search([('id','=',self.type_de_recharge)]).id,
                    'numero_cheque':self.numero_cheque,
                    'quitance_tva':self.quitance_tva,
                    'numero_quitance_tva':self.numero_quitance_tva,
                    'type_af':'sublime carte',
                    'debit':0,
                    'credit':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'solde_carte':montant,
                    'state':state
                    })
                    
                res = self.env['benin_petro.historique'].create({
                    'montant_init':po.montant_plafond,
                    'montant_fin':po.montant_plafond-m_init,
                    'sous_chargeur':po.id,
                    'type_op':'Recharge compte client',
                    'diff':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'reste':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'client_id':self.client_id.id,
                    'moyen_de_paiement':self.moyen_de_paiement,
                    'prix_init':self.type_de_recharge,
                    'facture_num' : facture_num,
                    'document' : self.document,
                    'produit' : self.env['product.product'].search([('id','=',self.type_de_recharge)]).id,
                    'numero_cheque':self.numero_cheque,
                    'quitance_tva':self.quitance_tva,
                    'numero_quitance_tva':self.numero_quitance_tva,
                    'type_af':'sublime carte',
                    'debit':abs(po.montant_plafond-m_init-po.montant_plafond),
                    'credit':0,
                    'solde_carte':montant,  
                    'num_recharge':num_recharge ,
                    'state':state 
                    })
                po.write({
                        'montant_plafond':po.montant_plafond-self.montant
                    })
                print res
                prix_init=self.env['product.product'].search([('id','=',self.type_de_recharge)]).lst_price
                #qte=round(self.montant/prix_init, 2)
                TVA="{:.4f}".format(qte*tva_l.amount)
                prix_ht = self.env['product.product'].search([('id','=',self.type_de_recharge)]).lst_price-tva_l.amount
                montant_hor_taxes= "{:.4f}".format(prix_ht*qte)
                print montant_hor_taxes
                print TVA
                TVA = float(self.montant * 0.18)
                montant_hor_taxes = float(float(self.montant) - TVA)
                detail_id =self.env['benin_petro.historique_ben_detail'].sudo().create({
                    'prix_init':prix_init,
                    'qte':qte,
                    'montant_hor_taxes':montant_hor_taxes,
                    'tva_init':tva_l.amount,
                    'tva':TVA,
                    #'historique_id' : res,
                    'prix_ht':self.env['product.product'].search([('id','=',self.type_de_recharge)]).lst_price-tva_l.amount,
                    'montant_ttc':self.montant,
                    'type_de_recharge':self.env['product.product'].search([('id','=',self.type_de_recharge)]).name
                    
                })
                historique_id = self.env['benin_petro.historique'].search([('id','=',res.id)])
                historique_id.detail_id = detail_id
                return {'type': 'ir.actions.act_window_close'}
            else:
                raise ValidationError(_("Votre solde est insuffisant pour effectuer l\'opération demandé"))
        else:
                raise ValidationError(_("Merci de remplir la TVA retenu a la source"))
# -------------------------------------------------


class benin_petro_recharger_carte(models.TransientModel):
    _name = 'benin_petro.wizard.recharger.carte'
    _rec_name = 'id'
    _description = 'New Description'


    def _getClient_id(self):
        return self._context.get('active_ids',False)[0]

    @api.onchange('client_id')
    def _onchange_client(self):
        self.update({
		'solde': self.client_id.solde_compte,
		'carte_ids': self.client_id.carte_ids
	})



    client_id = fields.Many2one("res.partner",string="Client",default=_getClient_id)
    solde = fields.Float(string='Solde non affecté',readonly=True)#,compute="_getSolde", store=True)
    carte_ids = fields.Many2many("benin_petro.carte", "wizard_recharger_carte", "recharge_id", "carte_id","Liste des Cartes")


    @api.multi
    def save_recharger(self):
        return {'type': 'ir.actions.act_window_close'}

