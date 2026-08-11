# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from collections import OrderedDict
import collections
#from unidecode import unidecode
from random import randint
# from keyid import keyid
import time
#import swagger_client
#from swagger_client.rest import ApiException
from pprint import pprint

class api_stock(models.Model):
    @api.multi
    def addSignature(self,qrcode):
        
        data = []
        
	
      
	emp = self.env['stock.picking'].search([('id','=', int( qrcode.get("id")  ) )])
        emp.image1= qrcode.get("image1")
        emp.image2= qrcode.get("image2")
        
	
           

        data.append([('transfere_id',emp.id),('source_name',emp.location_id.name),('source_id',emp.location_id.id),('destination_name',emp.location_dest_id.name),("destination_id",emp.location_dest_id.id), ('Date_prevue',emp.min_date), ('Delivery_Type',emp.move_type)])
	#data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
	
        return data
    @api.multi
    def getListeDesProduitsParTransfere(self,qrcode):
	
        data = []
        
	print qrcode.get("id")
      
	emps = self.env['stock.picking'].search([('id','=', int( qrcode.get("id")  ) )])
        
        print emps
	for emp in emps:
            for em in emp.move_lines:

		data.append([("product_id",em.product_id.id),('name',em.product_id.name),('qte',em.product_uom_qty)])
	#data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
	print data
        return data
        
    @api.multi
    def TransfereValider(self,qrcode):
	
	 data = []
        
	 
       
	 emp = self.env['stock.picking'].search([('id','=', int( qrcode.get("id")  ) )])
      
      
       
         
         if emp.id and emp.state!='done':
           
            emp.do_transfer()
            
            return 1
         elif emp.id and emp.state=='done' :
            return 0
         else:
           return -1

    @api.multi
    def getTransfereParEmplacement(self,qrcode):
        data = []
        emplacement_id = self.env['benin_petro.point.vente'].search([('id','=', int( qrcode.get("id")))]).location_id
	emps = self.env['stock.picking'].search([('location_dest_id','=', int(emplacement_id))])
	for emp in emps:
          data.append([('transfere_id',emp.id),('source_name',emp.location_id.name),('source_id',emp.location_id.id),('destination_name',emp.location_dest_id.name),("destination_id",emp.location_dest_id.id), ('Date_prevue',emp.min_date), ('Delivery_Type',emp.move_type)])
	#data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
        return data

    @api.multi
    def getTransfere(self,qrcode):
        print 'kvdjvdv'
        
        data = []
        
	
      
	emps = self.env['stock.picking'].search([('id','=', int( qrcode.get("id")  ) )])
        
        
	for emp in emps:
           

          data.append([('transfere_id',emp.id),('source_name',emp.location_id.name)
          ,('source_id',emp.location_id.id),('destination_name',emp.location_dest_id.name),("destination_id",emp.location_dest_id.id), ('Date',emp.min_date), 
          ("image1",emp.image1),("image2",emp.image2),('Delivery_Type',emp.move_type)])
	#data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
	print data
        return data
    @api.multi
    def produitsParEmplacement(self,qrcode):
      
        
        data = []
        p=[]
        
	
      
	emps = self.env['stock.quant'].search([('location_id','=', int( qrcode.get("id")  ) )])
        
        
	for emp in emps:
         #self.env['stock.quant'].search([('location_id','=', int( qrcode.get("id")  ) ),('product_id','=', emp.product_id.id  ) )])
       
         res =emp.search([('location_id','=', int( qrcode.get("id")  )),('product_id','=',emp.product_id.id)])
         if len(res)>1:
            
            
             if not emp.product_id.id in p:
               qty=0
               for r in res:
                qty +=r.qty
               data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",qty)])
             p.append(emp.product_id.id)
               
         else:
              data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",emp.qty)])
         

           
         
       
         
       
	
        return data
    @api.multi
    def produitsParEmplacementCategorie(self,qrcode):
        
        
        data = []
        p=[]
        
	
      
	emps = self.env['stock.quant'].search([('location_id','=', int( qrcode.get("id")  ) ),('product_id.categories_consomable','=' ,qrcode.get("categorie")) ])
        
        print emps
	for emp in emps:
         #self.env['stock.quant'].search([('location_id','=', int( qrcode.get("id")  ) ),('product_id','=', emp.product_id.id  ) )])
         print 'lol'
         res =emp.search( [('location_id','=', int( qrcode.get("id")  )),('product_id','=',emp.product_id.id)  ] )
         if len(res)>1:
            
             print 'hell' 
             print p
             if not emp.product_id.id in p:
               qty=0
               for r in res:
                qty +=r.qty
               data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",qty)])
             p.append(emp.product_id.id)
               
         else:
              data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",emp.qty)])
         

           
         
       
         
       
	print data
        return data
        


