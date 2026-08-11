# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_detail_consommation_par_carte(models.TransientModel):
    _name = 'benin_petro.wizard.detail_consommation_par_carte'

    point_vente_id=fields.Many2one('benin_petro.point.vente', string='Point de  Vente')
    product_id =fields.Many2one('product.product', string='Produit')
    client_id =fields.Many2one('res.partner', string='Client')

    start_date = fields.Datetime(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )
    end_date = fields.Datetime(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )

    def print_excel_report(self):
        datas={"ihoi":"ppppp"}
        print datas
        return self.env['report'].get_action(self, 'res.partner.xlsx',data=datas )

    @api.multi
    def print_report(self):
        datas = []
        res = {}
        ds=str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1))
        de=str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1))
        if not self.product_id:
            liste_transactions = self.env['benin_petro.carte.consommation'].search([('create_date', '>=', ds), ('create_date', '<=', de),('type_vente','=','Vente par SUBLIME CARTE')])
        else:
            liste_transactions = self.env['benin_petro.carte.consommation'].search([('create_date', '>=', ds), ('create_date', '<=', de),('type_vente','=','Vente par SUBLIME CARTE'),('product_ids','=',self.product_id.id)])
        if len(liste_transactions) >0:
            for tr in liste_transactions:
                if self.client_id:
                    if tr.carte_id.owner_id.id == self.client_id.id:
                        dat = {
                                'date':tr.create_date,
                                'carte_id':tr.carte_id.libelle.name,
                                'carte_serie':tr.carte_id.num_serie,
                                'qte':tr.quantite,
                                'produit':tr.product_ids.name,
                                'nombre_tr':1,
                                'montant_horstaxe':tr.total_hors_taxe,
                                'tva':tr.total_tva,
                                'montant_ttc':locale.format("%d", float(tr.montant)),
                                'point_vente':tr.point_vente_id.name
                                }
                        datas.append(dat)
                else:
                    dat = {
                            'date':tr.create_date,
                            'carte_id':tr.carte_id.libelle.name,
                            'carte_serie':tr.carte_id.num_serie,
                            'qte':tr.quantite,
                            'produit':tr.product_ids.name,
                            'nombre_tr':1,
                            'montant_horstaxe':tr.total_hors_taxe,
                            'tva':tr.total_tva,
                            'montant_ttc':locale.format("%d", float(tr.montant)),
                            'point_vente':tr.point_vente_id.name
                            }
                    datas.append(dat)
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if self.client_id:
            client = self.client_id.name
        else:
            client = "Tous"
        datas = {
            'form':
            {
                'date_debut':ds,
                'date_fin':de,
                'print_date':d1,
                'produit': self.product_id.name,
                'client': client,
                'transactions':datas,
                'total':[],
                }
        }

        # print datas["form"]["transactions"]
        return self.env['report'].get_action(self, 'benin_petro.detail_consommation_par_carte_report', data=datas)

    @api.multi
    def print_report2(self):
        datas = []
        ds=datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
        de=datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
        
        point_vente = self.env['benin_petro.point.vente'].search([])
        res={}
        client_name = ""
        for pr in point_vente:
            if not self.product_id:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=','Vente par SUBLIME CARTE'),('point_vente_id','=',pr.id)])
            else:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=','Vente par SUBLIME CARTE'),('point_vente_id','=',pr.id),('product_ids','=',self.product_id.id)])
            data = {}
            # print liste_transactions

            print("##################")
            print(len(liste_transactions))
            print("##################")
            if len(liste_transactions) >0:
                for tr in liste_transactions:
                    
                     if tr.carte_id.owner_id.id == self.client_id.id:
                        if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                            # print "oooooooooooooooo"
                            if pr.name not in res:
                        
                                dat = [{
                                        'date':tr.create_date,
                                        'carte_id':tr.carte_id.libelle.name,
                                        'carte_serie':tr.carte_id.num_serie,
                                        'qte':tr.quantite,
                                        'produit':tr.product_ids.name,
                                        'nombre_tr':1,
                                        'montant_horstaxe':tr.total_hors_taxe,
                                        'tva':tr.total_tva,
                                        'montant_ttc':locale.format("%d", float(tr.montant)),
                                        'point_vente':tr.point_vente_id.name
                                }]
                               
                                if tr.carte_id.libelle.name not in data:
                                    data[tr.carte_id.libelle.name] = dat
                                    
                                else:
                                    data[tr.carte_id.libelle.name].append({
                                        'date':tr.create_date,
                                        'carte_id':tr.carte_id.libelle.name,
                                        'carte_serie':tr.carte_id.num_serie,
                                        'qte':tr.quantite,
                                        'produit':tr.product_ids.name,
                                        'nombre_tr':1,
                                        'montant_horstaxe':tr.total_hors_taxe,
                                        'tva':tr.total_tva,
                                        'montant_ttc':locale.format("%d", float(tr.montant)),
                                        'point_vente':tr.point_vente_id.name
                                    })
                                    
                                    
                                res[pr.name] = data
                                #print res
                            else:
                                
                                if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                                    # print '8888888888888888888888888888'
                                    dat = [{
                                        'date':tr.create_date,
                                        'carte_id':tr.carte_id.libelle.name,
                                        'carte_serie':tr.carte_id.num_serie,
                                        'qte':tr.quantite,
                                        'produit':tr.product_ids.name,
                                        'nombre_tr':1,
                                        'montant_horstaxe':tr.total_hors_taxe,
                                        'tva':tr.total_tva,
                                        'montant_ttc':locale.format("%d", float(tr.montant)),
                                        'point_vente':tr.point_vente_id.name
                                        }]

                                    if tr.carte_id.libelle.name not in data:
                                        data[tr.carte_id.libelle.name] = dat
                                    
                                    else:
                                        data[tr.carte_id.libelle.name].append({
                                            'date':tr.create_date,
                                            'carte_id':tr.carte_id.libelle.name,
                                            'carte_serie':tr.carte_id.num_serie,
                                            'qte':tr.quantite,
                                            'produit':tr.product_ids.name,
                                            'nombre_tr':1,
                                            'montant_horstaxe':tr.total_hors_taxe,
                                            'tva':tr.total_tva,
                                            'montant_ttc':locale.format("%d", float(tr.montant)),
                                            'point_vente':tr.point_vente_id.name
                                        })
                                        
                                    res[pr.name] = data
                                    #print res
        
        sum_qte = 0
        sum_nombre_tr = 0
        sum_montant_horstaxe = 0
        sum_tva = 0
        sum_montant_ttc = 0  
        for key,val in res.items():
            
           
            for k,v in val.items():
                
                for va in v:
                    sum_qte += va["qte"]
                    sum_nombre_tr += va["nombre_tr"]
                    sum_montant_horstaxe += va["montant_horstaxe"]
                    sum_tva += va["tva"]
                    sum_montant_ttc += float(va["montant_ttc"])

        total = {"qte":float(sum_qte),"sum_nombre_tr":locale.format("%d", float(sum_nombre_tr)),"sum_montant_horstaxe": float(sum_montant_horstaxe),"sum_tva":float(sum_tva),"sum_montant_ttc":float(sum_montant_ttc)}
        
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if self.client_id:
            client = self.client_id.name
        else:
            client = "Tous"
        datas = {
                'form':
                {
                    'date_debut':self.start_date,
                    'date_fin':self.end_date,
                    'print_date':d1,
                    'produit': self.product_id.name,
                    'client': client,
                    'transactions':res,
                    'total':total,
                    }
            }

        # print datas["form"]["transactions"]
        return self.env['report'].get_action(self, 'benin_petro.detail_consommation_par_carte_report', data=datas)


class detail_consommation_par_carte_report(models.AbstractModel):
    _name = 'report.benin_petro.detail_consommation_par_carte_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.detail_consommation_par_carte_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.detail_consommation_par_carte_report', docargs)
