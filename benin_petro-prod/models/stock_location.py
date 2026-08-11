# -*- coding: utf-8 -*-
from odoo import  api, fields, models
from odoo.exceptions import ValidationError

class Location(models.Model):
    _inherit = 'stock.location'
    
    
    typedeEmp = fields.Selection(string='Type de Emplacement interne', selection=[('depot', 'Dépôt'),('point', 'Point de vente'), ('camion', 'Camion'),])
    
    camion_id = fields.Many2one('fleet.vehicle', string='Camion')
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point vente")
    #bon_de_commande = fields.One2many(comodel_name='sale.order', inverse_name='stock', string='Bon de commande')
    #  return res
    @api.onchange('usage')
    def _usage(self):
        print ' ------ usge -----'
        self.point_vente_id=''
        self.camion_id=''
  

    @api.constrains('camion_id')
    def _camion_(self):
     ids=[]
     print 'constrants'
     locations=self.env['stock.location'].search([('id','!=',self.id)]) 
     for  l  in locations:
        if l.camion_id.id:
           
            ids.append(l.camion_id.id)
    
     print ids
     if self.camion_id.id in ids:

    
       raise ValidationError(' Le Camion choisi est déjà affecté a un autre emplacement  ')

    @api.constrains('point_vente_id')
    def _point_vente_id_(self):
     ids=[]
     print 'constrants'
     locations=self.env['stock.location'].search([('id','!=',self.id)]) 
     for  l  in locations:
        if l.point_vente_id.id:
           
            ids.append(l.point_vente_id.id)
    
     print ids
     if self.point_vente_id.id in ids:

    
       raise ValidationError(' Le Point vente choisi est déjà affecté a un autre emplacement  ')

     


        
