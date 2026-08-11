# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class Commercial(models.Model):
    _name = 'benin_petro.commercial'
    _rec_name = 'commercial'

    commercial = fields.Many2one('res.users',string='Nom complet')
    clients_ids = fields.One2many(comodel_name='res.partner', inverse_name='commercial', string='Liste des clients')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )