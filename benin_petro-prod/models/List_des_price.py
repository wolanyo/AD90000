# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint

from datetime import date
from datetime import datetime, timedelta
import math

class Pricelist(models.TransientModel):
    _name = 'benin_petro.wizard.valider.client'
   
   
    @api.multi
    def get_report_data(self):
        #room_lines service_lines food_lines transport_lines  laundry_lines
        data=[]
        i=0
        print ' get_report_data --------  '
        count=len(self.env['res.partner'].search([]))
        print count
        defi = 0
        for res_p in self.env['res.partner'].search([]):
            i+=1
            
            print str(i)+'/'+str(count)
           
            first =self.req_f(res_p.id)[0][0]
            secound=False
            if self.req_g(res_p.id)[0][0]:
                secound=self.req_g(res_p.id)[0][0]+res_p.solde_carte+res_p.solde_compte
                if secound and first:
                    defi = float(secound)-float(first)
                valuer=0
                if  secound and  first and  self.req_f(res_p.id)[0][0] and self.req_g(res_p.id)[0][0] and defi!=0:
                    data.append({'client':res_p.name, 'price':defi})             
        return data

    def get_report(self):
        return self.env['report'].get_action(self,'benin_petro.validation_reportt1')
    @api.multi
    def req_f(self,id):
        self._cr.execute("select sum((CAST(new_version as float)-CAST(old_version as float))) from benin_petro_log where champ='Solde non affecte' and client_id="+str(id)+" and acteur_name!='Administrator' and CAST(new_version as float)>CAST(old_version as float);")
        data = self._cr.fetchall()
        return  data
    @api.multi
    def req_g(self,id):
        
        self._cr.execute("select sum(montant) from benin_petro_carte_consommation gc,benin_petro_carte c where gc.carte_id=c.id and c.owner_id = "+str(id)+" and gc.state!='annuler';")
        data = self._cr.fetchall()
        return  data
