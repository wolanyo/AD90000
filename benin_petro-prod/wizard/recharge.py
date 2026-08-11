# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
from pprint import pprint


class sous_chargeur(models.TransientModel):

    _name="benin_petro.wizard.sous.chargeur"
    _rec_name='id'

    def _getChargeur_id(self):
        return self._context.get('active_ids',False)[0]
    
    def _getsolde(self):
        return self.env["benin_petro.chargeur"].search([('access','=',self.env.uid)]).montant_plafond

    montant = fields.Float(string='Montant plafond',required=True)
    booltest=fields.Selection([('Augmenter','A augmenter'),('Diminuer','A diminuer')],default='Augmenter')
    sous_chargeur_id = fields.Many2one("benin_petro.sous_chargeur",string="Trésorier",default=_getChargeur_id)
    solde = fields.Float(string='Votre solde',default=_getsolde)
    
    @api.multi
    def test(self):
        if self.booltest=='Augmenter': 
            print '8888888888888888888888888888888'
            if self.montant <= self.sous_chargeur_id.superv.montant_plafond:
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond-self.montant
                nv_montant_cassier= self.sous_chargeur_id.montant_plafond+self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond,
                'montant_fin':nv_montant,
                'chargeur':p.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'sublime carte',
                'diff':abs(p.montant_plafond-nv_montant),
                'debit':abs(p.montant_plafond-nv_montant),
                'credit':0 
                })
                vals = {
                'montant_init':self.sous_chargeur_id.montant_plafond,
                'montant_fin':nv_montant_cassier,
                'sous_chargeur':self.sous_chargeur_id.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'sublime carte',
                'diff':abs(float(self.sous_chargeur_id.montant_plafond)-nv_montant_cassier),
                'debit':0,
                'credit':abs(float(self.sous_chargeur_id.montant_plafond)-nv_montant_cassier) 
                }
                self.env['benin_petro.historique'].create(vals)
                
                p.write({
                    'montant_plafond':nv_montant,
                })
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.sous_chargeur_id.id)])
                nv_m= po.montant_plafond+self.montant
                po.montant_super = nv_montant
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond+self.montant

                po.write({
                    'montant_plafond':nv_m,
                })

            else :
                raise ValidationError('Votre solde est insuffisant ')
        elif self.booltest=='Diminuer':
            if self.montant <= self.sous_chargeur_id.montant_plafond:
                p=self.env["benin_petro.chargeur"].search([('id','=',self.sous_chargeur_id.superv.id)])
                nv_montant= p.montant_plafond+self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond,
                'montant_fin':nv_montant,
                'chargeur':p.id,
                'type_op':'Rappel de fonds TRESORIER',
                'type_af':'sublime carte',
                'diff':abs(p.montant_plafond-nv_montant),
                'debit':0,
                'credit':abs(p.montant_plafond-nv_montant) 
                })
                
                p.write({
                    'montant_plafond':nv_montant,
                })
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.sous_chargeur_id.id)])
                nv_m = po.montant_plafond-self.montant
                po.montant_super = nv_montant
                self.env['benin_petro.historique'].create({
                'montant_init':self.sous_chargeur_id.montant_plafond,
                'montant_fin':nv_m,
                'sous_chargeur':self.sous_chargeur_id.id,
                'type_op':'Rappel de fonds TRESORIER',
                'type_af':'sublime carte',
                'diff':abs(self.sous_chargeur_id.montant_plafond-nv_m),
                'debit':abs(self.sous_chargeur_id.montant_plafond-nv_m),
                'credit': 0
                })
                po.write({
                    'montant_plafond':nv_m,
                })

            else :
                raise ValidationError('Le  solde est insuffisant ')


# # -------------------------------------------------


class benin_petro_chargeur(models.TransientModel):
    _name="benin_petro.wizard.benin_petro.chargeur"
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
        if self.montant !=0:
            p=self.env["benin_petro.chargeur"].search([('id','=',self.chargeur_id.id)])
            if self.booltest=='Augmenter':
                nouveau=self.chargeur_id.montant_plafond + self.montant
                typeop='Approvisionnement'
                debit = 0
                credit = abs(p.montant_plafond-nouveau)
            if self.booltest=='Diminuer':
                nouveau=self.chargeur_id.montant_plafond - self.montant
                typeop='RAPPEL DE FONDS GOUVERNEUR'
                debit = abs(p.montant_plafond-nouveau)
                credit = 0
           
            if nouveau != p.montant_plafond:
                if nouveau >= 0:
                    
                    
                    self.env['benin_petro.historique'].create({
                        'montant_init':p.montant_plafond,
                        'montant_fin':nouveau,
                        'chargeur':self.chargeur_id.id,
                        'type_op':str(typeop),
                        'type_af':'sublime carte',
                        'diff':abs(p.montant_plafond-nouveau),
                        'debit':debit,
                        'credit': credit    
                        })
                    p.write({
                        'montant_plafond':nouveau,
                    })
                else  :
                    raise ValidationError('Solde  insuffisant ')
        else :
            raise ValidationError('Donnez un montant supérieur a zéro')

        
