# -*- coding: utf-8 -*-
from odoo import fields, api, models
from odoo.exceptions import  ValidationError
class beneficiaire(models.Model):
    _name = "benin_petro.bseneficiaire"
    _rec_name = "name"
    taux = fields.Float(string='Taux',required=True)
    bonus = fields.Float(string='Cumul de bonus')
    owner_id = fields.Many2one("res.partner",string="Client")
    cart_id = fields.Many2one("benin_petro.carte",string="Carte")
    libelle = fields.Integer(string="id")
    name = fields.Char(string="Nom",required=True)
    email = fields.Char(string="Email",size=100)
    phone = fields.Char(string="Téléphone",size=20)
    mobile = fields.Char(string="Mobile",size=20)
    adresse = fields.Char(size=200,string="Adresse")
    city = fields.Char(size=30,string="Ville")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    # @api.constrains('taux')
    # def _check_taux(self):
    #     if self.taux<0 and self.taux>100:
    #         raise ValidationError(("Le Taux doit etre entre 0 est 100"))


    @api.model
    def create(self, vals):
    	print 'hgggggggggggggggghghghghgh'
    	# print vals['taux']
	# if float(vals['taux'])<0 and float(vals['taux'])>100:
     #        raise ValidationError(("Le Taux doit etre entre 0 est 100"))
	#     return null
		
    	return super(beneficiaire, self).create(vals)
