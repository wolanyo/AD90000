# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
from pprint import pprint


class sous_chargeur(models.TransientModel):

    _name="benin_petro.wizard.soustv"
    _rec_name='id'

    def _getChargeur_id(self):
        return self._context.get('active_ids',False)[0]
    
    def _getsolde(self):
        return self.env["benin_petro.chargeur"].search([('access','=',self.env.uid)]).montant_plafond_tv

    montant = fields.Float(string='Montant plafond',required=True)
    booltest=fields.Selection([('Augmenter','A augmenter'),('Diminuer','A diminuer')],default='Augmenter')
    sous_chargeur_id = fields.Many2one("benin_petro.sous_chargeur",string="Trésorier",default=_getChargeur_id)
    solde = fields.Float(string='Votre solde',default=_getsolde)
    
    @api.multi
    def test(self):
        if self.booltest=='Augmenter': 
            if self.montant <= self.sous_chargeur_id.superv.montant_plafond_tv:
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond_tv-self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond_tv,
                'montant_fin':nv_montant,
                'chargeur':p.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'TV',
                'diff':abs(p.montant_plafond_tv-nv_montant),
                'debit':abs(p.montant_plafond_tv-nv_montant),
                'credit':0 
                
                })
                
                p.write({
                    'montant_plafond_tv':nv_montant,
                })
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.sous_chargeur_id.id)])
                nv_m= po.montant_plafond_tv+self.montant
                po.montant_super_tv = nv_montant
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond_tv+self.montant

                self.env['benin_petro.historique'].create({
                'montant_init':po.montant_plafond_tv,
                'montant_fin':nv_m,
                'sous_chargeur':self.sous_chargeur_id.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'TV',
                'diff':abs(po.montant_plafond_tv-nv_m),
                'debit':0,
                'credit':abs(po.montant_plafond_tv-nv_m), 
                
                })

                po.write({
                    'montant_plafond_tv':nv_m,
                })

            else :
                raise ValidationError('Votre solde est insuffisant ')
        elif self.booltest=='Diminuer':
            if self.montant <= self.sous_chargeur_id.montant_plafond_tv:
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond_tv+self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond_tv,
                'montant_fin':nv_montant,
                'chargeur':p.id,
                'type_op':'Rappel de fonds TRESORIER',
                'type_af':'TV',
                'diff':abs(p.montant_plafond_tv-nv_montant),
                'debit':0,
                'credit':abs(p.montant_plafond_tv-nv_montant)
                })
                p.write({
                    'montant_plafond_tv':nv_montant,
                })
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.sous_chargeur_id.id)])
                nv_m = po.montant_plafond_tv-self.montant
                po.montant_super_tv = nv_montant
                self.env['benin_petro.historique'].create({
                'montant_init':po.montant_plafond_tv,
                'montant_fin':nv_m,
                'sous_chargeur':self.sous_chargeur_id.id,
                'type_op':'Rappel de fonds TRESORIER',
                'type_af':'TV',
                'diff':abs(po.montant_plafond_tv-nv_m),
                'debit':abs(po.montant_plafond_tv-nv_m),
                'credit':0
                
                })
                po.write({
                    'montant_plafond_tv':nv_m,
                })

            else :
                raise ValidationError('Le  solde est insuffisant ')


# # -------------------------------------------------


class benin_petro_chargeur(models.TransientModel):
    _name="benin_petro.wizard.benin_petro.chargeurtv"
    _rec_name = 'id'

    def _getChargeur_id(self):
        return self._context.get('active_ids',False)[0]

    montant = fields.Float(string='Montant plafond',required=True)
    booltest=fields.Selection([('Augmenter','A augmenter'),('Diminuer','A diminuer')],default='Augmenter')
    chargeur_id = fields.Many2one("benin_petro.chargeur",string="Trésorier",default=_getChargeur_id)

    @api.multi
    def recharger(self):
        nouveau=0
        typeop='hh'
        debit = 0
        credit = 0
        p=self.env["benin_petro.chargeur"].search([('id','=',self.chargeur_id.id)])
        if self.montant !=0:
            if self.booltest=='Augmenter':
                nouveau=self.chargeur_id.montant_plafond_tv + self.montant
                typeop='Approvisionnement'
                debit = 0
                credit = abs(p.montant_plafond_tv-nouveau)

            if self.booltest=='Diminuer':
                nouveau=self.chargeur_id.montant_plafond_tv - self.montant
                typeop='RAPPEL DE FONDS GOUVERNEUR'
                debit = abs(p.montant_plafond_tv-nouveau)
                credit = 0
            if nouveau != p.montant_plafond_tv:
                if nouveau >= 0:                  
                    
                    self.env['benin_petro.historique'].create({
                        'montant_init':p.montant_plafond_tv,
                        'montant_fin':nouveau,
                        'chargeur':self.chargeur_id.id,
                        'type_op':str(typeop),
                        'type_af':'TV',
                        'diff':abs(p.montant_plafond_tv-nouveau),
                        'debit':debit,
                        'credit':credit    
                        })
                    p.write({
                        'montant_plafond_tv':nouveau,
                    })
                else  :
                    raise ValidationError('Solde  insuffisant ')
        else :
            raise ValidationError('Donnez un montant supérieur a zéro')

        
