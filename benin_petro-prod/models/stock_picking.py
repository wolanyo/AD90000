# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    def a_fun(self):  
     return 5
    # delattr(odoo.addons.account.models.account_invoice.AccountInvoice, 'account_id')
    picking_type_id=fields.Many2one('stock.picking.type',string='Picking Type',required=False,default=a_fun,readonly=True)
    image1 = fields.Binary(string='image1')
    image2 = fields.Binary(string='image1')
    hide = fields.Boolean(default=True)
    location_id_for_view=fields.Many2one( 'stock.location')
    camion_id = fields.One2many('fleet.vehicle','picking_id',string='Camion')
    chauffeur_nom = fields.Char(string='')
    recepteur_nom = fields.Char(string='')
    type = fields.Selection(selection=[('blanch', 'Produits blancs'), ('autre', 'Autre')],string='Type de produit')
    observation = fields.Text(string='Observation')
    
    @api.model 
    def create(self,vals):
        vals['image1'] = 'iVBORw0KGgoAAAANSUhEUgAAAK0AAABqCAIAAABBIEYYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIISURBVHhe7djBjQJBFAPRyT/pBg5IaARUAH579cnlEtN/r+MPgXMuEBB4EuABDV4EeMADHnDgTcDvARf8HnDA7wEHPgn4LvDBd4EDvgsc8F3gwJ2A9wEnvA844H3AAe8DDngfcOAbAe9EXngncsA7kQPeiRzwTuSAdyIHfhFwL3DDvcAB9wIH3AsccC9wwL3AAfcCB/4RcDfyw93IAXcjB9yNHHA3csDdyAF3IwfcjRwoAv5/UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwtHzVfG6U/pf1sAAAAAElFTkSuQmCC'
        vals['image2'] = 'iVBORw0KGgoAAAANSUhEUgAAAK0AAABqCAIAAABBIEYYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIISURBVHhe7djBjQJBFAPRyT/pBg5IaARUAH579cnlEtN/r+MPgXMuEBB4EuABDV4EeMADHnDgTcDvARf8HnDA7wEHPgn4LvDBd4EDvgsc8F3gwJ2A9wEnvA844H3AAe8DDngfcOAbAe9EXngncsA7kQPeiRzwTuSAdyIHfhFwL3DDvcAB9wIH3AsccC9wwL3AAfcCB/4RcDfyw93IAXcjB9yNHHA3csDdyAF3IwfcjRwoAv5/UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwtHzVfG6U/pf1sAAAAAElFTkSuQmCC'
        return super(stock_picking, self).create(vals)
    
    # @api.onchange('camion_id','location_id','location_dest_id')
    # def _onchange_location_id(self):

    #    if self.location_id.usage != 'transit' or self.location_dest_id.usage != 'transit' :
    #        self.hide = True
    #    elif self.location_dest_id.usage == 'transit':
    #         self.camion_id=self.location_dest_id.camion_id
           
    #    elif  self.location_id.usage == 'transit':
    #      self.hide = False
    #      self.camion_id=self.location_id.camion_id
    # @api.constrains('camion_id','location_id','location_dest_id')
    # def _chack_locations(self):
    #     if self.location_id.usage != 'transit':
    #        self.hide = True
    #     elif self.location_dest_id.usage == 'transit':
    #         self.camion_id=self.location_dest_id.camion_id
           
    #     else:
    #      self.hide = False
    #      self.camion_id=self.location_id.camion_id
       
       
           
      
        
        # if self.location_id.id== self.location_dest_id.id:
        #     raise ValidationError(' source et distantion  sont  le meme error')

    # @api.constrains('move_lines','location_id')
    # def _move_lines(self):
    #     print ' my new constraint '
    #     ids=[]
    #     for move in self.move_lines:
    #         print ' my new constraint 3'
    #         ids.append( self.location_id.id)
    #     for i in range (len (ids) -1):
    #         if ids[i] == ids[i+1]:
           

    #   fleet_vehicle_view_search

    # @api.constrains('move_lines','location_id')
    # def _move_lines(self):
    #     print ' my new constraint '

    #     error_n=0
    #     product_name,source='',''
    #     qty_unit=0
    #     product_qty=0
    #     product_ids=[]
    #     print ' my new constraint 2 '
    #     for move in self.move_lines:
    #        product_ids.append(move.product_id.id)
    #     import collections
    #     product_ids =[item for item, count in collections.Counter(product_ids).items() if count > 1]
           
        

    #     for move in self.move_lines:
    #         print ' my new constraint 3'
    #         if move.product_id.id in product_ids:
    #             raise ValidationError("Vous ne pouvez pas choisir le meme produit plus qu'une fois dans chaque transfert ")
    

    #         print self.location_id.name
    #         print self.location_id_for_view.name

    #         res=self.env["stock.quant"].search([('location_id','=',self.location_id_for_view.id),('product_id','=',move.product_id.id)])
         
    #         qty=0
    #         if len(res)>1:
    #          for r in res:
    #             qty +=r.qty
    #         else:
    #             qty=res.qty
    #         print qty
    #         if move.product_uom_qty >qty:
    #             error_n+=1
    #             product_name=move.product_id.name
    #             source=self.location_id_for_view.name

            
            
    #         print move.product_id.name
    #         print ' quant '
    #         print move.product_uom_qty
           
    #         print 'qty'
    #         print qty
             

    #     if error_n>0:

    #        raise ValidationError("La quantité de produit "+str(product_name)+" disponible dans "+str(source)+" est supérieure à la quantité disponible veuillez la vérifier  0a")
    # #     # raise ValidationError(' error')

        # qte_dispo=self.env["stock.quant"].search([('location_id','=',vals['stock']),('product_id','=',product_id)])    
        # if qte_demande > qte_dispo.qty:
        #         flag+=1  
        # if flag==1:
        #     return super(bon_commande, self).create(vals)
        # else :
        #     raise ValidationError("La quantité de produit '+str(product_name)+'  disponible dans l\'emplacement demandé est supérieure à la quantité disponible veuillez la vérifier  ")
       
    
   
        
    