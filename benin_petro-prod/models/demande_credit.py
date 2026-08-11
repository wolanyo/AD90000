# -*- coding: utf-8 -*-
from odoo import fields, api, models
from odoo.exceptions import  ValidationError
from datetime import datetime
from datetime import date
import time
import locale
from datetime import timedelta

class benin_petro_demande_credit(models.Model):
    _name = 'benin_petro.demande_credit'
    _rec_name = 'montant'
    _order = 'create_date desc'

    type_credit = fields.Selection([('Sublim carte','Sublim carte'),('TV','TV')] , string="Type de crédit" , default="Sublim carte")
    montant = fields.Float("Montant de crédit")
    agent_monetique = fields.Many2one("benin_petro.sous_chargeur",string="Agent monétique", required=True)
    state = fields.Selection([('Brouillon','Brouillon'),('Valide','Validé'),('Annule','Annulé')] , string="Etat" , default="Brouillon")
    num_demande = fields.Char('Numéro de la demande',readonly=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    @api.model
    def default_get(self, fields):
        print '5555555555555555555555555'
        res =  super(benin_petro_demande_credit, self).default_get(fields)
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        print user
        sous_chargeur = self.env["benin_petro.sous_chargeur"].search([('access','=',user.id)])
        print sous_chargeur
        res['agent_monetique'] = sous_chargeur.id
        
        return res

    @api.model
    def create(self, vals):
        # user=self.env["res.users"].sudo().search([('id','=',self.env.user.id)])
        # sous_chargeur = self.env["benin_petro.sous_chargeur"].search([('access','=',user.id)])
        demmande = self.env["benin_petro.demande_credit"].sudo().search([],order='create_date desc')
        if demmande:
            vals['num_demande'] = 'D%06d' % (int(demmande[0].num_demande.split("D")[1]) + 1)
        else:
            vals['num_demande'] = 'D%06d' % (1)

        res = super(benin_petro_demande_credit, self).create(vals)
        return res

    @api.multi
    def setToAnnule(self):
        self.ensure_one()
        self.state="Annule"

    def getDate(self):
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        print d1
        return d1

    @api.multi
    def setToValide(self):
        self.ensure_one()
        
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        
        p=self.env["benin_petro.chargeur"].sudo().search([('access','=',user.id)])
        if self.type_credit == 'Sublim carte':
            if self.montant <= p.montant_plafond:
                nv_montant= p.montant_plafond-self.montant
                nv_montant_cassier= self.agent_monetique.montant_plafond+self.montant
                self.env['benin_petro.historique'].create({
                'montant_init':p.montant_plafond,
                'montant_fin':nv_montant,
                'chargeur':p.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'sublime carte',
                'diff':abs(p.montant_plafond-nv_montant),
                'debit':abs(p.montant_plafond-nv_montant),
                'credit':0 ,
                'demande_credit':self.id
                })
                vals = {
                'montant_init':self.agent_monetique.montant_plafond,
                'montant_fin':nv_montant_cassier,
                'sous_chargeur':self.agent_monetique.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'sublime carte',
                'diff':abs(float(self.agent_monetique.montant_plafond)-nv_montant_cassier),
                'debit':0,
                'credit':abs(float(self.agent_monetique.montant_plafond)-nv_montant_cassier) ,
                'demande_credit':self.id
                }
                self.env['benin_petro.historique'].create(vals)
                
                p.write({
                    'montant_plafond':nv_montant,
                })
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.agent_monetique.id)])
                nv_m= po.montant_plafond+self.montant
                po.montant_super = nv_montant
                p=self.env["benin_petro.chargeur"].sudo().search([('id','=',self.agent_monetique.superv.id)])
                nv_montant= p.montant_plafond+self.montant

                po.write({
                    'montant_plafond':nv_m,
                })
                self.state="Valide"

            else :
                raise ValidationError('Votre solde est insuffisant ')
        else:   
            if self.montant <= p.montant_plafond_tv:
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
                po=self.env["benin_petro.sous_chargeur"].search([('id','=',self.agent_monetique.id)])
                nv_m= po.montant_plafond_tv+self.montant
                po.montant_super_tv = nv_montant
                p=self.env["benin_petro.chargeur"].sudo().search([('id','=',self.agent_monetique.superv.id)])
                nv_montant= p.montant_plafond_tv+self.montant

                self.env['benin_petro.historique'].create({
                'montant_init':po.montant_plafond_tv,
                'montant_fin':nv_m,
                'sous_chargeur':self.agent_monetique.id,
                'type_op':'RECHARGE MONETIQUE',
                'type_af':'TV',
                'diff':abs(po.montant_plafond_tv-nv_m),
                'debit':0,
                'credit':abs(po.montant_plafond_tv-nv_m), 
                
                })

                po.write({
                    'montant_plafond_tv':nv_m,
                })
                self.state="Valide"

            else :
                raise ValidationError('Votre solde est insuffisant ')
       

class benin_petro_demande_credit_par_treso(models.Model):
    _name = 'benin_petro.demande_credit_par_treso'
    _rec_name = 'montant'
    _order = 'create_date desc'


    type_credit = fields.Selection([('Sublim carte','Sublim carte'),('TV','TV')] , string="Type de crédit" , default="Sublim carte")
    montant = fields.Float("Montant de crédit")
    tresorier = fields.Many2one("benin_petro.chargeur",string="Trésorier", required=True)
    state = fields.Selection([('Brouillon','Brouillon'),('Valide','Validé'),('Annule','Annulé')] , string="Etat" , default="Brouillon")
    compute_field = fields.Boolean(string="check field", compute='_get_user')
    num_demande = fields.Char('Numéro de la demande',readonly=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    @api.model
    def default_get(self, fields):
        print '5555555555555555555555555'
        res =  super(benin_petro_demande_credit_par_treso, self).default_get(fields)
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        print user
        chargeur = self.env["benin_petro.chargeur"].search([('access','=',user.id)])
        print chargeur
        res['tresorier'] = chargeur.id
        
        return res
    @api.one
    @api.depends('compute_field')
    def _get_user(self):
		self.ensure_one()
		if not self.env.user.has_group('benin_petro.group_benin_petro_president') :
			self.compute_field = True
		else:
			self.compute_field = False

    @api.model
    def create(self, vals):
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        chargeur = self.env["benin_petro.chargeur"].search([('access','=',user.id)])
        demmande = self.env["benin_petro.demande_credit_par_treso"].sudo().search([],order='create_date desc')
        if demmande:
            vals['num_demande'] = 'D%06d' % (int(demmande[0].num_demande.split("D")[1]) + 1)
        else:
            vals['num_demande'] = 'D%06d' % (1)

        res = super(benin_petro_demande_credit_par_treso, self).create(vals)
        return res

    @api.multi
    def setToAnnule(self):
        self.ensure_one()
        self.state="Annule"

    def getDate(self):
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        print d1
        return d1

    @api.multi
    def setToValide(self):
        self.ensure_one()
        nouveau=0
        typeop='hh'
        debit = 0
        credit = 0
        if self.type_credit == 'Sublim carte':
            if self.montant !=0:
                p=self.env["benin_petro.chargeur"].search([('id','=',self.tresorier.id)])
                nouveau=self.tresorier.montant_plafond + self.montant
                typeop='Approvisionnement'
                debit = 0
                credit = abs(p.montant_plafond-nouveau)
                if nouveau != p.montant_plafond:
                    if nouveau >= 0:
                        self.env['benin_petro.historique'].create({
                            'montant_init':p.montant_plafond,
                            'montant_fin':nouveau,
                            'chargeur':self.tresorier.id,
                            'type_op':str(typeop),
                            'type_af':'sublime carte',
                            'diff':abs(p.montant_plafond-nouveau),
                            'debit':debit,
                            'credit': credit    
                            })
                        p.write({
                            'montant_plafond':nouveau,
                        })
                        self.state="Valide"
                    else  :
                        raise ValidationError('Solde  insuffisant ')
            else :
                raise ValidationError('Donnez un montant supérieur a zéro')
        else:
            p=self.env["benin_petro.chargeur"].search([('id','=',self.tresorier.id)])
            if self.montant !=0:
                nouveau=self.tresorier.montant_plafond_tv + self.montant
                typeop='Approvisionnement'
                debit = 0
                credit = abs(p.montant_plafond_tv-nouveau)
                if nouveau != p.montant_plafond_tv:
                    if nouveau >= 0:                  
                        
                        self.env['benin_petro.historique'].create({
                            'montant_init':p.montant_plafond_tv,
                            'montant_fin':nouveau,
                            'chargeur':self.tresorier.id,
                            'type_op':str(typeop),
                            'type_af':'TV',
                            'diff':abs(p.montant_plafond_tv-nouveau),
                            'debit':debit,
                            'credit':credit    
                            })
                        p.write({
                            'montant_plafond_tv':nouveau,
                        })
                        self.state="Valide"
                    else  :
                        raise ValidationError('Solde  insuffisant ')
            else :
                raise ValidationError('Donnez un montant supérieur a zéro')




