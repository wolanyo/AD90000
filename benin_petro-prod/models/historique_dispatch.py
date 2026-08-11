# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from datetime import date, datetime, timedelta
import dateutil.relativedelta as relativedelta
from random import randint

class historique_dispatch(models.Model):
    _name = 'benin_petro.historique.dispatch'

    client_id = fields.Many2one("res.partner",string="Client")
    libelle = fields.Char(string="Libellé")
    montant = fields.Float(string='Montant')
