# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from random import randint


class benificiare(models.Model):
    _inherit = "res.partner"


    owner_id = fields.Many2one("res.partner",string="Client", required=True)
    taux = fields.Char(string="taux")
