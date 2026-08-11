# -*- coding: utf-8 -*-
from odoo import fields, models,api

class product_report(models.Model):

    _name="benin_petro.product.report"
    
    name = fields.Char(string='Produit')
    id_prod = fields.Integer(string='id produit')
    id_stat = fields.Integer()
    qte = fields.Integer(string='Qte')
    station = fields.Char()
    transfert = fields.Many2one('benin_petro.transfert')
    prod_report_id = fields.One2many('benin_petro.product.total.report','report_id')
     

class product_total_report(models.Model):

    _name="benin_petro.product.total.report"

    id_prod = fields.Integer(string='id produit')
    name = fields.Char(string='Produit')
    qte = fields.Integer(string='Qte')
    #fields.One2many('benin_petro.product.report','prod_report_id')
    report_id = fields.Many2one('benin_petro.product.report',ondelete='cascade')
    report_idd=fields.Many2one('benin_petro.transfert')