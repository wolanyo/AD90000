# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
class customer(models.Model):
    _name = "benin_petro.customer"
    _rec_name = "name"
    def getContryByDefault(self):
        return self.env['res.country'].search([['code', '=', 'BJ']]).id

    libelle = fields.Integer(string="id")
    name = fields.Char(size=18,string="Nom",required=True)
    email = fields.Char(string="Email",size=100)
    mobile = fields.Char(string="Téléphone",size=20,required=True)
    adresse = fields.Char(size=200,string="Adresse")
    city = fields.Char(size=30,string="Ville")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=getContryByDefault)
    carte_ids = fields.One2many("benin_petro.carte","libelle",string="cartes",required=True)
    taux = fields.Float(string="Taux",required=True)
    partner_id = fields.Many2one("res.partner",string="Partner")
    bonus = fields.Float(string="Cumul de bonus")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )


