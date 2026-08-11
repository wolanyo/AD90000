# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import  ValidationError
from lxml import etree
from num2words import num2words
from datetime import datetime
from datetime import date
import time
import locale
from datetime import timedelta

class historiquekkiapay(models.Model):
    _name = 'benin_petro.historiquekkiapay'
    _order = 'create_date desc'
    

    client_id = fields.Many2one(comodel_name='res.partner')
    source = fields.Char(string='source') 
    source_common_name = fields.Char(string='source name') 
    amount = fields.Char(string='montant') 
    country = fields.Char(string='pays') 
    transactionId = fields.Char(string='Transaction') 
    performedAt = fields.Char(string='date paiement') 

