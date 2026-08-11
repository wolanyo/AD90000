# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from random import randint
import time



class sold_transfert(models.Model):
    _name = "benin_petro.sold_transfert"
    _rec_name="code_tran"
    code_tran = fields.Char(string="Code de Transfert")
    type_transfert = fields.Selection([('compte-carte','Compte à Carte'),('carte-compte','Carte au Compte'),('carte-carte','Carte à Carte')],string="Type du transfert")
    compte = fields.Many2one("res.partner",string='Compte',default=lambda self:self.env.user.partner_id.id)
    carte_sr = fields.Many2one('benin_petro.carte',string="Carte Source")
    carte_di = fields.Many2one('benin_petro.carte',string="Carte Destinataire")
    montant = fields.Float(string=u"Montant à transferer")
    sold_compte = fields.Float(string="Solde du Compte")
    sold_carte_source = fields.Float(string="Solde de la Carte Source")
    sold_carte_dis = fields.Float(string="Solde de la Carte Destinataire")
    state = fields.Selection([('brouillon','Brouillon'),('valide','Validé'),('annule','Annulé')],string="Statut",default="brouillon")
    sold_comptee = fields.Float(string="Solde du Compte")
    @api.onchange('carte_sr')
    def _onchange_carte_source(self):
        if self.carte_sr:
            return {'value':{'sold_carte_source':float(self.carte_sr.solde)}}
        return False
    
    @api.onchange('carte_di')
    def _onchange_carte_destinataire(self):
        if self.carte_di:
            return {'value':{'sold_carte_dis':float(self.carte_di.solde)}}
        return False
    
    @api.onchange('compte')
    def _onchange_compte(self):
        if self.compte:
            return {'value':{'sold_compte':float(self.compte.solde_compte_hide),'sold_comptee':float(self.compte.solde_compte_hide)}}
        return False

    @api.model
    def create(self,vals):
        print vals
        code = randint(1111,9999)
        vals['code_tran'] = 'TR-'+str(code)+'-'+str(datetime.datetime.now().date())
        vals['sold_comptee'] = self.env["res.partner"].search([("id","=",int(self.env.user.partner_id.id))]).solde_compte_hide
        if "carte_sr" in vals.keys():    
            vals['sold_carte_source'] = self.env["benin_petro.carte"].search([("id","=",int(vals.get("carte_sr")))]).solde
        if "carte_di" in vals.keys():    
            vals['sold_carte_dis'] = self.env["benin_petro.carte"].search([("id","=",int(vals.get("carte_di")))]).solde
        return super(sold_transfert, self).create(vals)

    @api.constrains('montant', 'type_transfert','sold_carte_source','sold_carte_dis','sold_compte')
    def _check_montant(self):
        print 'ccccccccccccccccccccccccccccccccccccccccccc'
        print self.montant
        print self.sold_comptee
        print self.sold_compte
        print '---------------------------------------'
        if self.montant<=float(0):
            raise ValidationError(_("Le montant a transfert doit être supérieur à zéro"))
        if self.type_transfert == 'carte-carte' or self.type_transfert == 'carte-compte' :
            if self.montant > self.carte_sr.solde:
                raise ValidationError(_("Le montant a transfert doit être inferieur ou egale le solde de la carte source "))
        if self.type_transfert == 'compte-carte':
            if self.montant > self.compte.solde_compte_hide:
                print self.montant
                print self.sold_comptee
                raise ValidationError(_("Le montant a transfert doit être inferieur ou egale le solde de compte "))

    @api.multi
    def setValide(self):
        if self.type_transfert == 'compte-carte':
            carte_des = self.env['benin_petro.carte'].search([('id','=',self.carte_di.id)])
            cmt = self.env['res.partner'].search([('id','=',self.compte.id)])
            carte_des.write({
                'solde':float(carte_des.solde + float(self.montant))
            })
            old = cmt.solde_compte_hide
            cmt.write({
                'solde_compte_hide':float(cmt.solde_compte_hide - float(self.montant))
            })
        elif self.type_transfert == 'carte-compte':
            carte_sour = self.env['benin_petro.carte'].search([('id','=',self.carte_sr.id)])
            cmt = self.env['res.partner'].search([('id','=',self.compte.id)])
            carte_sour.write({
                'solde':float(carte_sour.solde -float(self.montant))
            })
            old = cmt.solde_compte_hide
            cmt.write({
                'solde_compte_hide':float(cmt.solde_compte_hide + float(self.montant))
            })
        elif self.type_transfert == 'carte-carte':
            carte_sour = self.env['benin_petro.carte'].search([('id','=',self.carte_sr.id)])
            carte_des = self.env['benin_petro.carte'].search([('id','=',self.carte_di.id)])
            carte_sour.write({
                'solde':float(carte_sour.solde -float(self.montant))
            })
            carte_des.write({
                'solde':float(carte_des.solde + float(self.montant))
            })
        self.compte.solde_carte = 0
        for carte in self.compte.carte_ids:
            self.compte.solde_carte += carte.solde
        self.write({
            'state':'valide'
        })

    @api.multi
    def setAnnule(self):
        self.write({
            'state':'annule'
        })

