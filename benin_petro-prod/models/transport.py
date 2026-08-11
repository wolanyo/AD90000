# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _rec_name='libelle'
    @api.onchange('capacite','name')
    def _on_libelle(self):
        print ' on change lible'
        print self.capacite
        if self.capacite:
         self.libelle = str(self.name)+'/'+str(self.capacite)+' L'
         print self.libelle
        else:
            self.libelle = str(self.name)
    @api.one
    @api.depends('capacite','name')
    def _compute_libelle(self):
        print ' on comput name'
        if self.capacite:
         self.libelle = str(self.name)+'/'+str(self.capacite)
        else:
            self.libelle = str(self.name)
    libelle = fields.Char(string='')
    name = fields.Char(string='Nom',required=True)
    fleet_type = fields.Selection(
        [('citerne','Camion citerne'),
            ('tractor', "Unité motorisée"),
         ('trailer', 'Remorque'),
         ('dolly', 'Chariot'),
         ('other', 'Autre'),
         
         ],
        string='Type de véhicule')
    
    
    picking_id = fields.Many2one(comodel_name='stock.picking')
    capacite = fields.Float(string='Capacité',required=True)

    transfer_id = fields.Many2one(comodel_name='benin_petro.transfert')
    conteneur_type=fields.Selection([('divisee','Avec Compartiment'),('non divisee','Sans Compartiments')] ,string=' Type de conteneur ',default='non divisee',required=True)
    conteneurs_ids = fields.One2many(comodel_name='fleet.vehicle.camion.conteneur', inverse_name='camion_id', string='Conteneurs')
    operating_unit_id = fields.Many2one(
        'operating.unit', string='Operating Unit',
        required=False)
    @api.constrains('capacite')
    def _capacite(self):
        if self.capacite<=0:
            raise ValidationError('La Capacite de Camion doit être supérieur ou égal à zéro ')
class  Conteneur(models.Model):
    _name = 'fleet.vehicle.camion.conteneur'

    camion_id = fields.Many2one('fleet.vehicle', string='Camion')
    libelle = fields.Char(string='Libellé du Compartimen')
    capacite = fields.Float(string='Capacité du  Compartiment')


class employee(models.Model):
    _inherit = 'hr.employee'
    driver_license = fields.Char(string='Numéro de permis')
    name = fields.Char(string='Nom',required=True)
    
    
    
   

class resource(models.Model):
    _inherit = 'resource.resource'

    name = fields.Char(string='Name',default='resource')
    
   
    

