# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
import datetime
import math
import locale

class benin_petro_add_paiement_credit(models.TransientModel):
    _name = 'benin_petro.wizard.add.paiement.credit'

    def _getsolde(self):
        return 1500

    def _getHistorique_id(self):
        return self._context.get('active_ids',False)[0]

    historique_id = fields.Many2one("benin_petro.historique",string="Historique",default=_getHistorique_id)
    reste = fields.Float(string='Reste',readonly=True ,compute="_getSolde" ,store=True)
    montant = fields.Float(string='Montant à payé',required=True)
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',required=True,selection=[('cheque', 'Chèque'), ('especes', 'Espèces'),('versement','Versement')])


    @api.multi
    def recharger(self):
        result = []
        if self.montant <= 0:
                raise ValidationError(_("Merci de renseigner un montant supérieur à zéro"))
        if self.historique_id.reste >= self.montant:
            montant_reste = self.historique_id.reste - self.montant
            montant_deja_paye = self.historique_id.diff - self.historique_id.reste
            result.append((0, 0, {'montant_credit':locale.format("%d", float(self.montant), grouping=True),'montant_reste' :locale.format("%d", float(montant_reste), grouping=True),'montant_deja_paye':locale.format("%d", float(montant_deja_paye), grouping=True),'moyen_de_paiement': self.moyen_de_paiement,'historique_id':self.historique_id,'journal_id':self.journal_id}))
            self.historique_id.liste_paiement = result
            self.historique_id.reste = self.historique_id.reste - self.montant
            if self.historique_id.reste > 0:
                self.historique_id.state = 'partiellement payer'
            else:
                self.historique_id.state = 'valide'
            data = [(0,0 ,{'account_id':1713 ,'partner_id':self.historique_id.client_id.id,'name':'à crédit','debit':self.montant}),
                    (0,0 ,{'account_id': 1724,'partner_id':self.historique_id.client_id.id,'name':'à crédit','credit':self.montant})]
            av= self.env['account.move'].create({
            
            'journal_id':self.journal_id.id,
            'date':datetime.datetime.now().date(),
            'ref': self.historique_id.client_id.name+'-'+str(datetime.datetime.now()),
            'line_ids':data
            
            })
            av.post()
        else:
            raise ValidationError(_("Merci de renseigner un montant inferieur au reste"))
        print '8888888888888888888'
        print self.historique_id
        return {'type': 'ir.actions.act_window_close'}

