# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    categories_consomable = fields.Selection([('Lubrifiants','Lubrifiants'),('Produits blancs','Produits blancs'),('Gaz','Gaz'),('Accessoire','Accessoire'),('Autre','Autre')],string="Catégorie produit")
    #type_accessoire = fields.Selection([('avec_logo','AVEC LOGO'),('sans_logo','SANS LOGO'),('Autre','Autre')],string="Type d'accessoire")
    categories_service = fields.Selection([('Lavage','Lavage'),('Autre','Autre')],string="Catégorie service")
    autre_service = fields.Char(string="Autre service")
    categories_lavage = fields.Selection([('brosse','Lavage automatique à brosse'),('eau','Lavage traditionnelle à eau')],string="Type de lavage")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    

    def changeCategory(self,catName,catId):
        products = self.env['product.product'].sudo().search([('categories_consomable','=',catName)])
        products.sudo().write({
            'categ_id':catId
        })

    def change(self):
        self.changeCategory('Lubrifiants',6)
    @api.model
    def default_get(self, fields):
        res = super(ProductProduct, self).default_get(fields)     
        print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
        if self.env.user.has_group('benin_petro.group_benin_petro_adminn'):
            return res
        else :
            raise ValidationError("Vous n'avez pas le droit de créer un article")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)     
        print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
        if self.env.user.has_group('benin_petro.group_benin_petro_adminn'):
            return res
        else :
            raise ValidationError("Vous n'avez pas le droit de créer un article")