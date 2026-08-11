# -*- coding: utf-8 -*-
from odoo import  api, fields, models
from odoo.exceptions import ValidationError
import datetime
from random import randint
import collections


class Planification(models.Model):
    _name = 'benin_petro.transfert.planification'
   
    
    planification_id = fields.Many2one(comodel_name='benin_petro.transfert', string='')
    Date_prevue = fields.Date(string=' Date prévue')
    source=fields.Many2one(
        'stock.location', "Source")
    Destinations = fields.Many2one(
        'stock.location', "Destination")

   

class Transfer(models.Model):
    _name = 'benin_petro.transfert'
   
    _rec_name='num'
    _order = "create_date desc"
    typeDesProuduit = fields.Selection(selection=[('blanch', 'Produits blancs'), ('autre', 'Autre')],string='Type de produits')
   
    stock_picking_id = fields.Many2one('stock.picking', "pickin id")
    stock_picking_id2 = fields.Many2one('stock.picking', "pickin id2")
    progress = fields.Float(string='Progression',compute='_compute_states')
    transfer_type = fields.Selection(string=' Type de transfert', selection=[('a', 'Dépot-Camion'), ('b', 'Dépot-Camion-station'),('c','Camion-station'),('d', 'Dépot-Dépot')],required=True,default='a')
    location_id = fields.Many2one(
        'stock.location', "Source")
    camion_id = fields.Many2one('fleet.vehicle', string='Camion')
    camion_id_info = fields.One2many(comodel_name='fleet.vehicle', inverse_name='transfer_id', string='Camon Info')
    camion_id_Planification=fields.One2many(comodel_name='benin_petro.transfert.planification', inverse_name='planification_id', string='Planification')
    Date_prevue = fields.Date(string=' Date prévue',required=True)
    current_qty = fields.Float(string='Capacité libre sur le camion',compute='chak_qty')
    unit_qty = fields.Float(string='default Capacité disponible ')
    location_dest_id = fields.Many2one(
        'stock.location', "Destination")
    location_dest_depot_id = fields.Many2one(
        'stock.location', "Destination")
    move_lines = fields.One2many('benin_petro.transfert.move', 'transfere_id', string="Stock Moves", copy=True)
    station_move_lines = fields.One2many(comodel_name='stock.move.station', inverse_name='transfer_id', string=u'Transfert')
    location_id_for_view=fields.Many2one( 'stock.location')

    chauffeur_id = fields.Many2one(comodel_name='hr.employee', string='Chauffeur')
    test2=fields.Boolean(default=False)
    hide = fields.Boolean(default=True)
    annuler = fields.Boolean(default=False)
    num = fields.Char(string="num")
    states = fields.Selection(string='État', selection=[('test','Bon de commande'),
    ('test2','Pré-Brouillon'),('brouillon','Brouillon'),('partiellementv', 'Partiellement Validé'),
    ('Valider', 'Validé'),('Annuler', 'Annulé')],default='test2',compute='_compute_states')
    products_report = fields.One2many("benin_petro.product.report","transfert")
    prod_report_id = fields.One2many('benin_petro.product.total.report','report_idd')
    

    commande_id = fields.Many2one(comodel_name='sale.order')

    client=fields.Many2one(comodel_name='res.partner', string='Client')
    is_done = fields.Char(string='is done')
    
    @api.constrains('move_lines')
    def move_lines_emputy(self):
        if not self.client.id:
            if self.transfer_type=='a' or self.transfer_type=='d' :
                if len(self.move_lines)<1:
                    raise ValidationError("Vous devez choisir des produits pour compléter le transfert   ")
    @api.constrains('station_move_lines')
    def station_move_lines_emputy(self):
        if self.transfer_type!='a' and self.transfer_type!='d' :
         if len(self.station_move_lines)<1:
            raise ValidationError("Vous devez choisir des points de ventes pour compléter le transfert   ")
    def produit_double(self,move_lines):
        unit=[]
        for move_line in move_lines:
            unit.append(move_line.product_id.id)
        unit =[item for item, count in collections.Counter(unit).items() if count > 1]
        return unit
    @api.constrains('move_lines')
    @api.onchange('move_lines')
    def produit_double_validation(self):
        if not self.client.id:
            for  move_line in self.move_lines:
                    if move_line.product_id.id in self.produit_double(self.move_lines):
                        raise ValidationError("Vous ne pouvez pas choisir le meme produit plus qu'une fois dans chaque transfert ")
    # @api.constrains('move_lines')
    @api.one
    @api.depends('states')
    def _compute_states(self):
        print '------------------------'
        print self.states
        print ' _compute_states'
        countValide=0.0
        countAnnuler=0.0
        if self.transfer_type=='a':
            if self.stock_picking_id.state=='done':
                self.states='Valider'
                self.progress=100.0
            elif self.stock_picking_id.state=='cancel':
                 self.states='Annuler'
                 self.progress=0
            elif  self.annuler:
                self.states='Annuler'
            elif not self.test2:
                self.states='test2'
                self.progress=0
            
            else:
                self.states='brouillon'
                self.progress=0.0
        elif  self.transfer_type=='d':
            if self.stock_picking_id.state=='done' and  self.stock_picking_id2.state=='done':
                self.states='Valider'
                self.progress=100.0
            elif  self.stock_picking_id.state=='done' or  self.stock_picking_id2.state=='done':
                self.states='partiellementv'
                self.progress=50.0
            elif  self.client.id:
                self.states='test'
            elif  self.annuler:
                self.states='Annuler'
            elif not self.test2:
                self.states='test2'
                self.progress=0
            
            else:
                self.states='brouillon'
           
        else:

            for  station_move in self.station_move_lines:
                if station_move.stock_picking_id.state=='done':
                    countValide+=1.0
                elif station_move.stock_picking_id.state=='cancel':
                    countAnnuler+=1.0
          
           
         
            if  countAnnuler==len(self.station_move_lines):
                self.states='Annuler'
            elif countValide==len(self.station_move_lines):
                self.states='Valider'
            elif  self.annuler:
                self.states='Annuler'
            elif countValide>0:
            
               self.states='partiellementv'
            elif  self.annuler:
                self.states='Annuler'
            
            elif not self.test2:
                self.states='test2'
                self.progress=0
           
            else:
               
                self.states='brouillon'
            if len(self.station_move_lines)>0:
             self.progress=(countValide/len(self.station_move_lines))*100
            else:
                 self.progress=0
    @api.multi
    def Valider2(self):
        self.test2=True
        self.states='test2'
              

    
    @api.model 
    def create(self,vals):
        vals["num"] = "T-"+ str(randint(1111,9999))
        print 'into write---------'
        print vals
        pa = super(Transfer, self).create(vals)
        print 'CREAAAAAAAAAAAATE '
        if pa.transfer_type == 'c' or pa.transfer_type =='b':    
            print 'CREAAAAAAAAAAAATE REPORT'
            print vals
            dataa=[]
            p=[]
            unit=[]
            products=[]
            allprod=[]
            prod=[]
            stat='hh'
            id_stat=0
            for  station_move in pa.station_move_lines:
                for move_line in  station_move.move_lines:
                    unit.append(move_line.product_id.id)
                    print 'uuuuuuuuuuuuuuuihuihihuhi'
            import collections
            res =[item for item, count in collections.Counter(unit).items() if count > 1]
            for  station_move in pa.station_move_lines:
                print 'uuuuuuuuuup'
                for move_line in  station_move.move_lines:  
                    print 'res =='+str(res)
                    if move_line.product_id.id in res:
                        qty=0
                        for  station_move2 in pa.station_move_lines:

                            for move_line2 in  station_move2.move_lines:
                                if move_line.product_id.id== move_line2.product_id.id:
                                    qty +=move_line2.qty

                        dataa.append((0,0 ,{'name':move_line.product_id.name,'qte':float(qty),'id_prod':move_line.product_id.id}))
                        res.remove(move_line.product_id.id)
                        p.append(move_line.product_id.id)
                    elif move_line.product_id.id not in p:
                        dataa.append((0,0 ,{'name':move_line.product_id.name,'qte':float(move_line.qty),'id_prod':move_line.product_id.id})) 
            for ob in pa.station_move_lines:
                for a in ob.move_lines :
                    if a.product_id.id not in allprod:
                        allprod.append(a.product_id.id)
            print 'alprod'
            print allprod
            for ob in pa.station_move_lines:
                
                for a in ob.move_lines :
                    
                    products.append(a.product_id.id)
                    ad=self.env['benin_petro.product.report'].create({
                    'name':a.product_id.name,
                    'qte':a.qty,
                    'station':a.stastion_move_ids.point_vente_id.libelle,
                    'transfert':pa.id,
                    'id_prod':a.product_id.id,
                    'id_stat':a.stastion_move_ids.point_vente_id.id,
                    'prod_report_id':dataa
                    })
                    stat=a.stastion_move_ids.point_vente_id.libelle
                    id_stat=a.stastion_move_ids.point_vente_id.id
                    pa.write({
                        'products_report':ad
                    })
                    
                prod=[]
                for ab in allprod :
                    if ab not in products :
                        prod.append(ab)
                for pro in prod :
                    ad=self.env['benin_petro.product.report'].create({
                    'name':pro,
                    'qte':0,
                    'id_prod':pro,
                    'station':stat,
                    'transfert':pa.id,
                    'prod_report_id':dataa
                    })
                    pa.write({
                        'products_report':ad
                    })
                prod=[]
                products=[]
            pa.write({
                    'prod_report_id':dataa
            })
        print  ' create --------22222 '
        return pa

    @api.multi
    def write(self, vals):
        print 'WRITE 88888888888888888'
        print vals
        if 'station_move_lines'  in vals:
            print 'into write---------'
            self.env['benin_petro.product.report'].search([("transfert","=",self.id)]).unlink()
            self.env['benin_petro.product.total.report'].search([("report_idd","=",self.id)]).unlink()
            pa= super(Transfer, self).write(vals)
            if self.transfer_type == 'c' or self.transfer_type =='b':    
                print 'WRIIIIIIIIIIIIIIIIIIITE REPORT'
                print vals
                dataa=[]
                p=[]
                unit=[]
                products=[]
                allprod=[]
                prod=[]
                stat='hh'
                id_stat=0
                for  station_move in self.station_move_lines:
                    for move_line in  station_move.move_lines:
                        unit.append(move_line.product_id.id)
                        print 'uuuuuuuuuuuuuuuihuihihuhi'
                import collections
                res =[item for item, count in collections.Counter(unit).items() if count > 1]
                for  station_move in self.station_move_lines:
                    print 'uuuuuuuuuup'
                    for move_line in  station_move.move_lines:  
                        print 'res =='+str(res)
                        if move_line.product_id.id in res:
                            qty=0
                            for  station_move2 in self.station_move_lines:

                                for move_line2 in  station_move2.move_lines:
                                    if move_line.product_id.id== move_line2.product_id.id:
                                        qty +=move_line2.qty

                            dataa.append((0,0 ,{'name':move_line.product_id.name,'qte':float(qty),'id_prod':move_line.product_id.id}))
                            res.remove(move_line.product_id.id)
                            p.append(move_line.product_id.id)
                        elif move_line.product_id.id not in p:
                            dataa.append((0,0 ,{'name':move_line.product_id.name,'qte':float(move_line.qty),'id_prod':move_line.product_id.id})) 
                for ob in self.station_move_lines:
                    for a in ob.move_lines :
                        if a.product_id.id not in allprod:
                            allprod.append(a.product_id.id)
                print 'alprod'
                print allprod
                for ob in self.station_move_lines:
                    
                    for a in ob.move_lines :
                        
                        products.append(a.product_id.id)
                        ad=self.env['benin_petro.product.report'].create({
                        'name':a.product_id.name,
                        'qte':a.qty,
                        'station':a.stastion_move_ids.point_vente_id.libelle,
                        'transfert':self.id,
                        'id_prod':a.product_id.id,
                        'id_stat':a.stastion_move_ids.point_vente_id.id,
                        'prod_report_id':dataa
                        })
                        stat=a.stastion_move_ids.point_vente_id.libelle
                        id_stat=a.stastion_move_ids.point_vente_id.id
                        self.write({
                            'products_report':ad
                        })
                        
                    prod=[]
                    for ab in allprod :
                        if ab not in products :
                            prod.append(ab)
                    for pro in prod :
                        ad=self.env['benin_petro.product.report'].create({
                        'name':pro,
                        'qte':0,
                        'id_prod':pro,
                        'station':stat,
                        'transfert':self.id,
                        'prod_report_id':dataa
                        })
                        self.write({
                            'products_report':ad
                        })
                    prod=[]
                    products=[]
                self.write({
                        'prod_report_id':dataa
                        })

            return pa
        else :
            return super(Transfer, self).write(vals)
       
       
    
       
    @api.onchange('transfer_type')
    def _onchange_transfer_type(self):
        self.location_id=''
        self.station_move_lines=''
        self.move_lines=''
        self.camion_id=''
    def _get_qty_produits(self):
        qty=0.0
        if self.transfer_type=='a' or  self.transfer_type=='d':
            for move_line in self.move_lines:
               if move_line.product_id.categories_consomable=="Produits blancs":
                    qty+=move_line.qty
        else:
             for  station_move in self.station_move_lines:
                for move_line in  station_move.move_lines:
                    if move_line.product_id.categories_consomable=="Produits blancs":
                         qty+=move_line.qty
        return qty
    @api.depends('camion_id','station_move_lines','move_lines')
    @api.onchange('camion_id','station_move_lines','move_lines')
    def _current_qty(self):
        if self.camion_id.capacite-self._get_qty_produits()>0:
            self.current_qty=self.camion_id.capacite-self._get_qty_produits()
        else:
            self.current_qty=0.0
    
    def chak_qty(self):
        self._current_qty()
       
        
        qty=0.0
        unit=[]
        res={}
        prods={}
        prodsname={}
        if self.transfer_type!='a'  and self.transfer_type!='d':
        
            for  station_move in self.station_move_lines:
                unit.append(station_move.point_vente_id.id)
            
                for move_line in  station_move.move_lines:
                   
                    qty+=move_line.qty
                    if move_line.product_id.id  not in prods:
                       
                        prods[move_line.product_id.id]=move_line.qty
                        prodsname[move_line.product_id.id]=move_line.product_id.name
                    else:
                           
                            prods[move_line.product_id.id]+=move_line.qty
            import collections
            resId =[item for item, count in collections.Counter(unit).items() if count > 1]
            for  station_move in self.station_move_lines:
                 if station_move.point_vente_id.id in resId:
                        raise ValidationError("Vous ne pouvez pas choisir le meme point vante plus qu'une fois dans chaque transfert ")

         

                  

        
    @api.constrains('station_move_lines','move_lines')
    def _qty_globle(self):
        if not self.client.id:
            if self.camion_id.capacite:
                if self.camion_id.capacite<self._get_qty_produits():
                    raise ValidationError('La  capacité de Camion insuffisante')
    @api.onchange('camion_id')
    def get_planns(self):
        current_date=datetime.datetime.now().date()
        ids=[]
        if self.location_dest_id.id :
       
            current_date= datetime.datetime.strftime(current_date, "%Y-%m-%d ")
            Planification=self.env['stock.picking'].search(['|',('location_id','=',self.location_dest_id.id),('location_dest_id','=',self.location_dest_id.id)])
        
            
            for p in Planification:
                if p.id!=self.stock_picking_id.id and p.min_date>=current_date and self.stock_picking_id.state!='cancel' and  self.stock_picking_id.state!='done':
                    ids.append((0,0,{'Destinations':p.location_dest_id,'Date_prevue':p.min_date,"source":p.location_id}))
            self.camion_id_Planification=''
            self.camion_id_Planification=ids
                
    @api.onchange('camion_id','location_id','location_dest_id','transfer_type')
    def _onchange_location_id(self):
        self.unit_qty=self.camion_id.capacite
        
        self.ensure_one()
       
        if self.transfer_type=='c':

            if self.camion_id.id :
                self.location_id= self.env['stock.location'].search([('camion_id','=',self.camion_id.id)]).id
                self.location_dest_id=self.location_id
                
        else:
            if self.camion_id.id :
                self.location_dest_id= self.env['stock.location'].search([('camion_id','=',self.camion_id.id)]).id
        self.location_id_for_view=self.location_id
        
       
        # self.camion_id_info=''
        # self.camion_id_info=[(4,self.camion_id.id)]
        self.chauffeur_id=self.camion_id.employee_id.id
        res={}
        ids=[]
        
        ids=[]
        locations=self.env['stock.location'].search([('camion_id','!=',False)])
        
        for  l  in locations:
          
                ids.append(l.camion_id.id)
        
    
        res['domain']={'camion_id':[('id','in',ids) ]}
    
        return res
       

    
    
    @api.multi
    def Check_qty(self):
        flag=1
        print 'test client '
        print self.client
        client_id=self.client
        for a in self.move_lines:
            print a.id
            print a.product_id
            qte=0
            qte_dispo=self.env["stock.quant"].search([('location_id','=',self.location_id.id),('product_id','=',a.product_id.id)])           
            qte_demande=a.qty
            for q in qte_dispo:
                qte+=q.qty
            print 'qte dispo'
            print qte
            if qte_demande > qte:
                flag=0
          
        if flag==1:
            
            data=[]

            for move_line in self.move_lines:
                data.append((0,0 ,{'name':'nn', 'product_id':move_line.product_id.id,'product_uom_qty':float(move_line.qty),'state':'draft','product_uom':1,
                'location_id':self.location_id.id,'location_dest_id':self.location_dest_id.id,'date_expected':datetime.datetime.now()}))
           
            av= self.env['stock.picking'].create({
                    
                'location_id':self.location_id.id,
                'location_dest_id':self.location_dest_id.id,
                'picking_type_id':5,
                'move_type':'direct',
                'move_lines':data,
                'min_date':self.Date_prevue,
                'location_id_for_view':self.location_id.id,
                'client_id':client_id.id
                    
                    })
            print 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
            print client_id 
            self.stock_picking_id=av.id
            print av
            av= self.env['stock.picking'].create({                
                'location_id':self.location_dest_id.id,
                'location_dest_id':self.location_dest_depot_id.id,
                'picking_type_id':5,
                'move_type':'direct',
                'move_lines':data,
                'min_date':self.Date_prevue,
                'location_id_for_view':self.location_id.id,
                'client_id':client_id.id       
                    })

            print 'CREAAAAAAAAAAAAAAAAAAAAAAAATED'
        else :
            raise ValidationError("La quantité disponible dans l\'emplacement demandé est supérieure à la quantité disponible veuillez la vérifier  ")
    
    @api.multi
    def Valider(self):
            print 'VALIIIIIIDER'
            # if  self.client.id:
            #     self.Check_qty()
            self.states='Valider'
            a=self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)])
            print a
            a.do_transfer()
            if self.stock_picking_id2.id:
              self.env['stock.picking'].search([("id","=",self.stock_picking_id2.id)]).do_transfer()
            for  station_move in self.station_move_lines:
                
            
                station_move. Valider()
    @api.multi
    def  action_cancel(self):
        self.annuler = True
        self.states='Annuler'
        self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).action_cancel()
        for  station_move in self.station_move_lines:
            station_move.action_cancel()
    @api.constrains('Date_prevue') 
    def _Date_prevue(self):
       
        if datetime.datetime.strptime(self.Date_prevue, '%Y-%m-%d').date()<datetime.datetime.now().date():
            raise ValidationError('Date prévue doit être supérieure ou égale à la date courante')
    def qty_par_emplacements(self,emp,prod):
            res=self.env["stock.quant"].search([('location_id','=',emp),('product_id','=',prod)])
            
            qty_globle=0
            if len(res)>1:
                for r in res:
                    qty_globle +=r.qty
            else:
                qty_globle=res.qty
            return qty_globle
    
    @api.constrains('move_lines','location_dest_id','location_id','camion_id','station_move_lines','transfer_type','location_dest_depot_id')
    def create_tarnsfer(self):
       
     
        if self.stock_picking_id.id:
            self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).unlink()
            
        if self.stock_picking_id2.id:
            self.env['stock.picking'].search([("id","=",self.stock_picking_id2.id)]).unlink()
            self.stock_picking_id2=''
        qty=0.0
        
        if self.location_dest_id.id and self.location_id.id  :
            data=[]
            p=[]
            unit=[]
            point_vente_ids=[]
            if self.transfer_type =='b':
                for  station_move in self.station_move_lines:
                    point_vente_ids.append(station_move.point_vente_id.id)
            
                    for move_line in  station_move.move_lines:
                        unit.append(move_line.product_id.id)
                import collections
                res =[item for item, count in collections.Counter(unit).items() if count > 1]
                point_vente_ids =[item for item, count in collections.Counter(point_vente_ids).items() if count > 1]
                 
                for  station_move in self.station_move_lines:
                    if station_move.point_vente_id.id in point_vente_ids:
                        raise ValidationError("Vous ne pouvez pas choisir le meme point vante plus qu'une fois dans chaque transfert ")
                    for move_line in  station_move.move_lines:

                       
                       
                        if move_line.product_id.id in res:
                            qty=0
                            for  station_move2 in self.station_move_lines:

                                 for move_line2 in  station_move2.move_lines:

                                   if move_line.product_id.id== move_line2.product_id.id:
                                       
                                     qty +=move_line2.qty
                                   if qty> self.qty_par_emplacements(self.location_id.id,move_line.product_id.id):
                                          raise ValidationError("La Quantité de produit "+str( move_line.product_id.name)+" disponible dans "+str(self.location_id.name)+" est supérieure à la quantité disponible veuillez  la vérifier  ")

                            data.append((0,0 ,{'name':'nn', 'product_id':move_line.product_id.id,'product_uom_qty':float(qty),'state':'draft','product_uom':1,
                                  'location_id':self.location_id.id,'location_dest_id':self.location_dest_id.id,'date_expected':datetime.datetime.now()}))
                            res.remove(move_line.product_id.id)
                            p.append(move_line.product_id.id)

                            
                            
                        elif move_line.product_id.id not in p:
                           data.append((0,0 ,{'name':'nn', 'product_id':move_line.product_id.id,'product_uom_qty':float(move_line.qty),'state':'draft','product_uom':1,
                            'location_id':self.location_id.id,'location_dest_id':self.location_dest_id.id,'date_expected':datetime.datetime.now()}))




                        
            elif self.transfer_type =='a' or  self.transfer_type=='d':
                print ' tarnsfer 1'

                for move_line in self.move_lines:
                    qty+=move_line.qty
                    data.append((0,0 ,{'name':'nn', 'product_id':move_line.product_id.id,'product_uom_qty':float(move_line.qty),'state':'draft','product_uom':1,
                    'location_id':self.location_id.id,'location_dest_id':self.location_dest_id.id,'date_expected':datetime.datetime.now()}))
                   
        
            if self.camion_id.capacite:
            
                if self.camion_id.capacite<qty:
                    raise ValidationError(' La capacité de Camion insuffisante')
            if self.transfer_type!='c' and not self.client.id :
                print 'ppppppppppppppppppppppppppppppppppppppp'
                av= self.env['stock.picking'].create({
                    
                'location_id':self.location_id.id,
                'location_dest_id':self.location_dest_id.id,
                'picking_type_id':5,
                'move_type':'direct',
                'move_lines':data,
                'min_date':self.Date_prevue,
                'location_id_for_view':self.location_id.id
                    
                    
                    })
                self.stock_picking_id=av.id
                print av
            else :
                prods={}
                prodsname={}
                for  station_move in self.station_move_lines:
                    for move_line in  station_move.move_lines:
                        
                        if move_line.product_id.id  not in prods:
                            
                            prods[move_line.product_id.id]=move_line.qty
                            prodsname[move_line.product_id.id]=move_line.product_id.name
                        else:
                           
                             prods[move_line.product_id.id]+=move_line.qty
                  
               
                for key,value in prods.iteritems():
                    
                    res=self.env["stock.quant"].search([('location_id','=',self.location_dest_id.id),('product_id','=',key)])
                
                    qty_globle=0
                    if len(res)>1:
                        for r in res:
                            qty_globle +=r.qty
                    else:
                        qty_globle=res.qty
                   
                    if value >qty_globle:
                         raise ValidationError("La Quantité de produit "+str( prodsname[key])+" demandée est indisponible  dans "+str(self.location_dest_id.name)+"  ")
            if self.transfer_type=='d' and not self.client.id :
             
                av= self.env['stock.picking'].create({
                    
                'location_id':self.location_dest_id.id,
                'location_dest_id':self.location_dest_depot_id.id,
                'picking_type_id':5,
                'move_type':'direct',
                'move_lines':data,
                'min_date':self.Date_prevue,
                'location_id_for_view':self.location_id.id
                    
                    
                    })
                self.stock_picking_id2=av.id
                
         
            
          
            for  station_move in self.station_move_lines:
           
               station_move.create_tarnsfer()
    @api.one
    @api.multi
    def unlink(self):
        self.ensure_one()
        if self.states=='Valider' or self.states=='partiellementv' :
            raise ValidationError("Impossible d'annuler un mouvement de stock qui est dans l'état 'Validé' ou 'Partiellement Validé  '.")
        else :

            self.ensure_one()
            if self.stock_picking_id.id:
                self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).unlink()
            for station_move_line in self.station_move_lines:
                station_move_line.unlink()
    
        return super(Transfer, self).unlink()




class move(models.Model):
    _name = 'benin_petro.transfert.move'
    _description = 'New move'
    _rec_name='libelle'
    
    libelle = fields.Char(string='libelle')
    @api.onchange('source','product_id','location_id_for_view')
    def _get_domin(self):
    
     ids=[]
     notIds=[]
     res={}
     toappned=[]
   
   
     for prod in self.transfere_id.move_lines:
       
        notIds.append(prod.product_id.id)

     
     locations = self.env['stock.quant'].search([('location_id','=',self.location_id_for_view.id)])
     
     for  l  in locations:
        if self.typeDesProuduit=='blanch':
            if l.product_id.id and l.qty>0 and l.product_id.categories_consomable=="Produits blancs":
            
                ids.append(l.product_id.id)
                toappned.append([(4,l.product_id.id)])
        else:
                    
            if  l.product_id.id and l.qty>0 and l.product_id.categories_consomable!="Produits blancs":
                ids.append(l.product_id.id)

    
    
     res['domain']={'product_id':[('id','in',ids) ]}
    
    
     return res
    booltest=fields.Boolean(string='',default=False)
    typeDesProuduit = fields.Selection(selection=[('blanch', 'Produits blancs'), ('autre', 'Autre')],string='Type de produits')
    no_edit = fields.Boolean(string='')
    product_id = fields.Many2one('product.product', 'Produit',required=True)
    Date_prevue = fields.Date(string='')
    states = fields.Selection(string='states', selection=[('done', 'done'), ('cancel', 'cancel'),('draft','draft'),])
    location_id_for_view=fields.Many2one( 'stock.location',required=True)
    source=fields.Many2one( 'stock.location',required=True)
    destinations = fields.Many2one(comodel_name='stock.location')
    transfere_id = fields.Many2one(comodel_name='benin_petro.transfert', string='parent')
    stastion_move_ids=fields.Many2one(comodel_name='stock.move.station', string='parent')
    for_domin = fields.Integer()
    qty_unitv = fields.Float(string='Quantité existent dans la source',compute="_get_qty_unit",store=True)
   
    qty_pointv = fields.Float(string='Quantité existent dans le Point de  vente',compute="_get_qty_point",store=True)
  
    qty = fields.Float(string='Quantité à livrer',required=True)
    def qty_par_emplacements(self,emp,prod):
            res=self.env["stock.quant"].search([('location_id','=',emp),('product_id','=',prod)])
            
            qty_globle=0.0
            if len(res)>1:
                for r in res:
                    qty_globle +=r.qty
            else:
                qty_globle=res.qty
            return qty_globle
    @api.one        
    @api.depends('no_edit','product_id','qty','source')
    def _get_qty_unit(self):
        if self.product_id.id:
           self.qty_unitv =self.qty_par_emplacements(self.location_id_for_view.id,self.product_id.id)
    @api.one   
    @api.depends('no_edit','product_id','qty','source')
    def _get_qty_point(self):
        if self.product_id.id:
           self.qty_pointv =self.qty_par_emplacements(self.destinations.id,self.product_id.id)

    
    @api.depends('no_edit','product_id','qty')
    def _compute_no_edit(self):
        if  self.id:
            self.no_edit =True
        
        else:
             self.no_edit =False
    
    @api.constrains('qty')
    def _qty(self):
        if not self.booltest:
            if self.qty<=0:
                self.no_edit =True
                raise ValidationError("La Quantité de produit "+str(self.product_id.name)+"  doit étre supérieure à zéro  ")
            elif self.qty_par_emplacements(self.location_id_for_view.id,self.product_id.id)<self.qty:
                raise ValidationError("La Quantité de produit "+str(self.product_id.name)+" est insuffisante   ")
    @api.model
    def create(self, values):
        # Add code here
        values['no_edit']=True
       
         
        return super(move, self).create(values)
    

    
    
    
class MoveStasion(models.Model):
    _name = 'stock.move.station'
    _rec_name='libelle'
    @api.one
    @api.depends('libelle','move_lines')
    def _compute_libelle(self):
         self.libelle = str(len(self.move_lines))+' produits'
    @api.onchange('point_vente_id')
    def _onchange_point_vente_id(self):
       
        if  self.point_vente_id.id:
            
            des=self.env['stock.location'].search([('point_vente_id','=',self.point_vente_id.id)]).id
            

            self.location_dest_id= des
        res={}
        ids=[]
        locations=self.env['stock.location'].search([('point_vente_id','!=',False)])
        for  l  in locations:
          
           
                ids.append(l.point_vente_id.id)
        
    
        res['domain']={'point_vente_id':[('id','in',ids) ]}
    
        return res
    def _qty_globle_par_prod(self,ids):
         qty=0.0
         for move_line in self.move_lines:
             if move_line.product_id.id==ids:
                 qty+=move_line.qty
         return qty

    def qty_par_emplacements(self,emp,prod):
        res=self.env["stock.quant"].search([('location_id','=',emp),('product_id','=',prod)])
        
        qty_globle=0
        if len(res)>1:
            for r in res:
                qty_globle +=r.qty
        else:
            qty_globle=res.qty
        return qty_globle

    @api.constrains('move_lines')
    @api.onchange('move_lines')
    def pord_in_empl(self):
        for move_line in self.move_lines:
            if move_line.qty > self.qty_par_emplacements(self.location_id_for_view.id,move_line.product_id.id) or self.qty_par_emplacements(self.location_id_for_view.id,move_line.product_id.id)< self._qty_globle_par_prod(move_line.product_id.id):
                 raise ValidationError("La Quantité de produit "+str( move_line.product_id.name)+" demandée est indisponible dans "+str(self.location_id_for_view.name))
                        
   
  
    @api.constrains('move_lines') 
    def chak_coans(self):
        
        qty=0.0
        res={}
        prods={}
        prodsname={}
        unit=[]
        resId=[]

        for  move_line in self.move_lines:
                qty+=move_line.qty

                if move_line.product_id.id  not in prods:
                    
                    prods[move_line.product_id.id]=move_line.qty
                    prodsname[move_line.product_id.id]=move_line.product_id.name
                else:
                        
                        prods[move_line.product_id.id]+=move_line.qty
                unit.append(move_line.product_id.id)
        import collections
        resId =[item for item, count in collections.Counter(unit).items() if count > 1]

        self.current_qty= self.transfer_id.camion_id.capacite-qty
        if self.transfer_id.camion_id.capacite:
            if self.transfer_id.camion_id.capacite<qty:
                raise ValidationError(' La capacité de Camion est insuffisante')
        qty=0.0
        for key,value in prods.iteritems():
            if key in resId:
                  raise ValidationError(' Point Vante '+ str(self.point_vente_id.name)+": Vous ne pouvez pas choisir le meme produit plus qu'une fois dans chaque transfert ")
            res=self.env["stock.quant"].search([('location_id','=',self.location_id_for_view.id),('product_id','=',key)])
        
            qty_globle=0
            if len(res)>1:
                for r in res:
                    qty_globle +=r.qty
            else:
                qty_globle=res.qty
           
            if value >qty_globle:
                    raise ValidationError(" La Quantité de produit "+str( prodsname[key])+" effectuée  pour "+str(self.point_vente_id.name)+" est supérieure à la quantité disponible veuillez la vérifier  ")


   
    
    def chak_qty(self):
        self. ensure_one()
        
        qty=0.0
        res={}
        prods={}
        prodsname={}
        unit=[]
        resId=[]
       
        for  move_line in self.move_lines:
                qty+=move_line.qty

                if move_line.product_id.id  not in prods:
                    
                    prods[move_line.product_id.id]=move_line.qty
                    prodsname[move_line.product_id.id]=move_line.product_id.name
                else:
                        
                        prods[move_line.product_id.id]+=move_line.qty
                unit.append(move_line.product_id.id)
        import collections
        resId =[item for item, count in collections.Counter(unit).items() if count > 1]

        self.current_qty= self.current_qty-qty
        if self.transfer_id.camion_id.capacite:
            if self.transfer_id.camion_id.capacite<qty:
                raise ValidationError(' La capacité de Camion est  insuffisante')
        qty=0.0
        for key,value in prods.iteritems():
            if key in resId:
                  raise ValidationError("Vous ne pouvez pas choisir le meme produit plus qu'une fois dans chaque transfert ")
            res=self.env["stock.quant"].search([('location_id','=',self.location_id_for_view.id),('product_id','=',key)])
        
            qty_globle=0
            if len(res)>1:
                for r in res:
                    qty_globle +=r.qty
            else:
                qty_globle=res.qty
           
            if value >qty_globle:
                    raise ValidationError("La Quantité de produit "+str( prodsname[key])+" demandée est indisponible dans "+str(self.location_id_for_view.name))
                    

    

    Date_prevue = fields.Date(string='')
    current_qty = fields.Float(string='Capacite disponible')
    libelle = fields.Char(string='Produits',compute='_compute_libelle')
    
    transfer_id = fields.Many2one(comodel_name='benin_petro.transfert',ondelete='cascade')
    location_id_for_view = fields.Many2one('stock.location', "source pour view",required=True)
    
    location_dest_id = fields.Many2one('stock.location', "destaination real",required=True)
    stock_picking_id = fields.Many2one('stock.picking', "pickin id")
    typeDesProuduit = fields.Selection(selection=[('blanch', 'Produits blancs'), ('autre', 'Autre')],string='Type de produits')
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente",required=True)
    source=fields.Many2one( 'stock.location')

    move_lines = fields.One2many(comodel_name='benin_petro.transfert.move', inverse_name='stastion_move_ids', string='Details',required=True)
    states = fields.Selection(string='État', selection=[('brouillon','Brouillon'),('Annuler', 'Annulé'),('Valider', 'Validé'),],default='brouillon',compute='_compute_states')
    @api.one
    @api.depends('states')
    def _compute_states(self):
        
       
        
        if self.stock_picking_id.state=='done':
            self.states='Valider'
        elif self.stock_picking_id.state=='cancel':
            self.states='Annuler'
        else:
                self.states='brouillon'
    @api.constrains('move_lines')
    def move_lines_emputy2(self):
        if len(self.move_lines)==0:
            raise ValidationError("Vous devez choisir des produits pour compléter le transfert pour  chaque point de vente ")
  
    
    @api.constrains('move_lines','source','location_dest_id','transfer_id')
    def create_tarnsfer(self):
        if self.stock_picking_id.id:
            self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).unlink()
     
       
       
        if self.location_dest_id.id and self.location_dest_id.id  and self.move_lines :
            data=[]
            for move_line in self.move_lines:
                
                 
                 data.append((0,0 ,{'name':'nn', 'product_id':move_line.product_id.id,'product_uom_qty':float(move_line.qty),'state':'draft','product_uom':1,
                  'location_id':self.source.id,'location_dest_id':self.location_dest_id.id,'date_expected':datetime.datetime.now()}))
           
            av= self.env['stock.picking'].create({
                
            'location_id':self.transfer_id.location_dest_id.id,
            'location_dest_id':self.location_dest_id.id,
                'picking_type_id':5,
                'move_type':'direct',
                'move_lines':data,
                'min_date':self.Date_prevue,
                'location_id_for_view':self.location_id_for_view.id
                
                
                })
                
           

            
          
            self.stock_picking_id=av.id
        #  av.post()
    @api.multi
    def unlink(self):
        if self.stock_picking_id.id:
            self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).unlink()
        if self.stock_picking_id.id:
              self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).unlink()
       
   
        return super(MoveStasion, self).unlink()
   
   
    @api.multi
    def Valider(self):
        
        
        self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).do_transfer()
    @api.multi
    def action_cancel(self):
        
        
        self.env['stock.picking'].search([("id","=",self.stock_picking_id.id)]).action_cancel()
    
    