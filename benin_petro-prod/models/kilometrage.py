# -*- coding: utf-8 -*-
from odoo import fields, api, models
from odoo.exceptions import  ValidationError
class kilometrage(models.Model):
    _name = "benin_petro.kilometrage"
    _rec_name = "carte_id"

    point_vente = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    carte_id = fields.Many2one("benin_petro.carte",string="Carte")
    client = fields.Many2one("res.partner",string="Clent")
    produit = fields.Many2one("product.product",string="Produit")
    type_operation = fields.Char(string="Type opération",required=True)
    kilometrage = fields.Float(string="Kilometrage")
    quantite = fields.Char(string="Quantité consommée")
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
		
    	return super(kilometrage, self).create(vals)
