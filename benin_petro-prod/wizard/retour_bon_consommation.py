# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time

class benin_petro_retour_bon_consommation(models.TransientModel):
    _name = 'benin_petro.wizard.retour_bon_consommation'


    point_vente_id=fields.Many2one('benin_petro.point.vente', string='Point de  Vente',required=True)
    product_id =fields.Many2one('product.product', string='Produit')
    type_vente = fields.Selection([('Vente par SUBLIME CARTE','Vente par SUBLIME CARTE'),('Vente par TV','Vente par TV')] , string="Type de vente")
    compute_field = fields.Boolean(string="check field")

    start_date = fields.Datetime(
         string='Date Début',
         required=True
         )
    end_date = fields.Datetime(
         string='Date Fin',
         required=True
         )

    def print_excel_report(self):
        datas={"ihoi":"ppppp"}
        return self.env['report'].get_action(self, 'retour_bon_consommation.xlsx',data=datas )

    @api.model
    def default_get(self, fields):
        res =  super(benin_petro_retour_bon_consommation, self).default_get(fields)
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        client = self.env["res.partner"].search([('access','=',self.env.user.id)])
        point_vente = self.env["benin_petro.point.vente"].search([('promoteur','=',client.id)])
        if point_vente:
            res['point_vente_id'] = point_vente[0].id
        if not self.env.user.has_group('benin_petro.group_benin_petro_promoteur') :
            res['compute_field'] = False
        else:
            res['compute_field'] = True
        return res

    @api.onchange('point_vente_id')
    def onchange_point_vente(self):
        client = self.env["res.partner"].search([('access','=',self.env.user.id)])
        if client:
            return {'domain':{'point_vente_id':[('promoteur','=',client.id)]}}

    @api.multi
    def print_report(self):
    #     print(self.start_date)
    #     ds=datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
    #     de=datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
        import pytz
        user_tz = self.env.user.tz or pytz.utc
        print(user_tz)
        local = pytz.timezone(user_tz)
        print(local)
        ds = datetime.strftime(pytz.utc.localize(datetime.strptime(self.start_date,DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        de = datetime.strftime(pytz.utc.localize(datetime.strptime(self.end_date,DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        ds=datetime.strptime(ds, '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)
        de=datetime.strptime(de, '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)
        res={}
        data = {}
        if self.type_vente:
            if self.product_id.id:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('type_vente','=',self.type_vente),('product_ids','=',self.product_id.id)])
            else:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('type_vente','=',self.type_vente)])

        else:
            if self.product_id.id:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('product_ids','=',self.product_id.id)])
            else:
                liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id)])
        
        i=0
        for tr in liste_transactions:
            i=i+1
            if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                if tr.quantite != 0:
                    prix_produit = int(tr.montant / tr.quantite)
                    
                else:
                    prix_produit = 0
                if tr.type_vente == 'Vente par TV':
                    for to in tr.ticket_ids:
                        if to.recus == 'Ticket':
                            client_name = to.tv_type.type_name
                            if client_name not in res:
                                if prix_produit != 0 :
                                    qte = float(format((float(to.tv_type.montant) / float(prix_produit)),'.3f'))
                                else:
                                    qte = 0
                                res[client_name] = {
                                    'type':client_name,
                                    'montant_ttc':to.tv_type.montant,
                                    'qte': qte,
                                    'nombre_tv':1,
                                    'montant_horstaxe':0,
                                    'tva':0,
                                }
                                
                            else:
                                res[client_name]["montant_ttc"] = float(res[client_name]["montant_ttc"]) + float(to.tv_type.montant)
                                if prix_produit != 0:
                                    res[client_name]["qte"] = float(res[client_name]["qte"]) + float(format((float(to.tv_type.montant) / float(prix_produit)),'.3f'))
                                else:
                                    res[client_name]["qte"] = float(res[client_name]["qte"]) + 0
                                res[client_name]["nombre_tv"] = int(res[client_name]["nombre_tv"]) + int(1)
                if tr.type_vente == 'Vente par SUBLIME CARTE':
                    client_name = tr.carte_id.owner_id.name
                    if client_name not in res:
                        res[client_name] = {
                            'type':client_name,
                            'montant_ttc':tr.montant,
                            'qte':tr.quantite,
                            'nombre_tv':1,
                            'montant_horstaxe':tr.total_hors_taxe,
                            'tva':tr.total_tva,
                        }
                        
                    else:
                        res[client_name]["montant_ttc"] = float(res[client_name]["montant_ttc"]) + float(tr.montant)
                        res[client_name]["qte"] = float(res[client_name]["qte"]) + float(tr.quantite)
                        res[client_name]["nombre_tv"] = int(res[client_name]["nombre_tv"]) + int(1)
                        res[client_name]["montant_horstaxe"] = float(res[client_name]["montant_horstaxe"]) + float(tr.total_hors_taxe)
                        res[client_name]["tva"] = float(res[client_name]["tva"]) + float(tr.total_tva)
                    
                    #print res
                    #data['qte'] =
                    #res[tr.ticket_id.tv_type.type_name] = float(res[tr.ticket_id.tv_type.type_name]) + float(tr.montant)
                    
                    
        gerant = ""
        gerant = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])
        if gerant:
            gerant = gerant[0].name
        else:
            gerant = ""
        adresse = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])
        if adresse:
            adresse = adresse[0].adress
        else:
            adresse = ""
        email = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])
        if email:
            email = email[0].mail
        else:
            email = ""
        telephone = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])
        if telephone:
            telephone = telephone[0].telephone
        else:
            telephone = ""
        sum_qte = 0
        sum_nombre_tv = 0
        sum_montant_horstaxe = 0
        sum_tva = 0
        sum_montant_ttc = 0
        for key,val in res.items():
            res[key]["tva"] = float(val["qte"]) * 18
            res[key]["montant_horstaxe"] = val["montant_ttc"] - res[key]["tva"]
            sum_qte += val["qte"]
            sum_nombre_tv += val["nombre_tv"]
            sum_montant_horstaxe += val["montant_horstaxe"]
            sum_tva += val["tva"]
            sum_montant_ttc += val["montant_ttc"]

        test = {"qte":sum_qte,"sum_nombre_tv":sum_nombre_tv,"sum_montant_horstaxe":round(sum_montant_horstaxe),"sum_tva":round(sum_tva),"sum_montant_ttc":sum_montant_ttc}
        
        type_vente = ""
        if self.type_vente == 'Vente par SUBLIME CARTE':
            type_vente = 'SUBLIME CARTE'
        if self.type_vente == 'Vente par TV':
            type_vente = 'TV'
        
        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if self.product_id:
            produit = self.product_id.name
        else:
            produit = "Tous"
        datas = {
                 'form':
                    {
                        'date_debut':str(datetime.strptime(str(ds + timedelta(hours=1)) , '%Y-%m-%d %H:%M:%S')),
                        'date_fin':str(datetime.strptime(str(de + timedelta(hours=1)) , '%Y-%m-%d %H:%M:%S')),
                        'print_date':d1,
                        'point_vente': self.point_vente_id.name,
                        'produit': produit,
                        'type_vente': type_vente,
                        'gerant': gerant,
                        'adresse': self.point_vente_id.promoteur.street,
                        'telephone': telephone,
                        'email':email,
                        'promoteur':self.point_vente_id.promoteur.name,
                        'transactions':res,
                        'test':test
                        
                     }
                }
                
        return self.env['report'].get_action(self, 'benin_petro.retour_bon_consommation_report', data=datas)

class retour_bon_consommation_report(models.AbstractModel):
    _name = 'report.benin_petro.retour_bon_consommation_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.retour_bon_consommation_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.retour_bon_consommation_report', docargs)
