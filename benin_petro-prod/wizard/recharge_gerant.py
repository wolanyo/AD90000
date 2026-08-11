# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
from pprint import pprint


class recharge_gerant(models.TransientModel):

    _name="benin_petro.wizard.recharge_gerant"
    _rec_name='id'

    def _getChargeur_id(self):
        return self._context.get('active_ids',False)[0]
    
    def _getsolde(self):
        return self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.uid)]).montant_plafond

    montant = fields.Float(string='Montant plafond',required=True)
    booltest=fields.Selection([('Augmenter','A augmenter'),('Diminuer','A diminuer')],default='Augmenter')
    gerant = fields.Many2one("benin_petro.agent",string="Gérant",default=_getChargeur_id)
    solde = fields.Float(string='Votre solde',default=_getsolde)
    
    @api.multi
    def recharger(self):
        if self.booltest=='Augmenter': 
            print '8888888888888888888888888888888'
            p=self.env["benin_petro.sous_chargeur"].search([(('access','=',self.env.uid))])
            if True:
                nv_montant= p.montant_plafond-self.montant
                nv_montant_gerant= self.gerant.montant_plafond+self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond,
                'montant_fin':nv_montant,
                'sous_chargeur':p.id,
                'type_op':'RECHARGE MONETIQUE Gérant',
                'type_af':'sublime carte',
                'diff':abs(p.montant_plafond-nv_montant),
                'debit':abs(p.montant_plafond-nv_montant),
                'credit':0 
                })
                vals = {
                'montant_init':self.gerant.montant_plafond,
                'montant_fin':nv_montant_gerant,
                'gerant':self.gerant.id,
                'type_op':'RECHARGE MONETIQUE Gérant',
                'type_af':'sublime carte',
                'diff':abs(float(self.gerant.montant_plafond)-nv_montant_gerant),
                'debit':0,
                'credit':abs(float(self.gerant.montant_plafond)-nv_montant_gerant) 
                }
                self.env['benin_petro.historique'].create(vals)
                
                p.write({
                    'montant_plafond':nv_montant,
                })
                po=self.env["benin_petro.agent"].search([('id','=',self.gerant.id)])
                nv_m= po.montant_plafond+self.montant
                # po.montant_super = nv_montant
                # p=self.env["benin_petro.sous_chargeur"].search([('id','=',self.gerant.superv.id)])
                # nv_montant= p.montant_plafond+self.montant

                po.write({
                    'montant_plafond':nv_m,
                })

            else :
                raise ValidationError('Votre solde est insuffisant ')
        # elif self.booltest=='Diminuer':
        #     if self.montant <= self.gerant.montant_plafond:
        #         p=self.env["benin_petro.chargeur"].search([('id','=',self.gerant.superv.id)])
        #         nv_montant= p.montant_plafond+self.montant
        #         self.env['benin_petro.historique'].create({
        #         'montant_init':p.montant_plafond,
        #         'montant_fin':nv_montant,
        #         'chargeur':p.id,
        #         'type_op':'Rappel de fonds TRESORIER',
        #         'type_af':'sublime carte',
        #         'diff':abs(p.montant_plafond-nv_montant),
        #         'debit':0,
        #         'credit':abs(p.montant_plafond-nv_montant) 
        #         })
                
        #         p.write({
        #             'montant_plafond':nv_montant,
        #         })
        #         po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.gerant.id)])
        #         nv_m = po.montant_plafond-self.montant
        #         po.montant_super = nv_montant
        #         self.env['benin_petro.historique'].create({
        #         'montant_init':self.gerant.montant_plafond,
        #         'montant_fin':nv_m,
        #         'sous_chargeur':self.gerant.id,
        #         'type_op':'Rappel de fonds TRESORIER',
        #         'type_af':'sublime carte',
        #         'diff':abs(self.gerant.montant_plafond-nv_m),
        #         'debit':abs(self.gerant.montant_plafond-nv_m),
        #         'credit': 0
        #         })
        #         po.write({
        #             'montant_plafond':nv_m,
        #         })

        #     else :
        #         raise ValidationError('Le  solde est insuffisant ')

