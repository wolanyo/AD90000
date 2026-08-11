# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from random import randint


class proprietaire(models.Model):
    #_inherit = "res.partner"
    _name="benin_petro.proprietaire"

    name = fields.Char(size=20, string="Nom complet")
   
    mobile = fields.Char(string="Mobile")

    ville = fields.Char(string="Ville",size=50)
    email = fields.Char(string="Email")
    bouns = fields.Float(string='Bouns')
    taux = fields.Float(string='Taux', store=True)





