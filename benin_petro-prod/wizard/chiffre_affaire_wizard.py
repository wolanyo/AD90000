# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_chiffre_affaire(models.TransientModel):
    _name = 'benin_petro.wizard.chiffre_affaire'

    point_vente_id=fields.Many2one('benin_petro.point.vente', string='Point de  Vente',required=True)
    product_id =fields.Many2one('product.product', string='Produit')
    type_vente = fields.Selection([('Vente par SUBLIME CARTE','Vente par SUBLIME CARTE'),('Vente par TV','Vente par TV')] , string="Type de vente")
    start_date = fields.Datetime(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )
    end_date = fields.Datetime(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )
    @api.model
    def default_get(self, fields):
        print '5555555555555555555555555'
        res =  super(benin_petro_chiffre_affaire, self).default_get(fields)
        user=self.env["res.users"].search([('id','=',self.env.user.id)])
        client = self.env["res.partner"].search([('access','=',self.env.user.id)])
        point_vente = self.env["benin_petro.point.vente"].search([('promoteur','=',client.id)])
        if point_vente:
            res['point_vente_id'] = point_vente[0].id
        return res

    def _getPointVente(self):
        print "11111111111111111111111111111111"
        return 6
    # @api.model
    # def default_get(self, fields):
    #     res = super(benin_petro_chiffre_affaire, self).default_get(fields)     
    #     print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    #     print res

    # @api.multi
    # def print_report_test(self):

    #     tresoriers = self.env['benin_petro.chargeur'].search([])
    #     total = 0
    #     res = {}
    #     for tresorier in tresoriers:
    #         transferts = self.env['benin_petro.historique'].search([('chargeur','=',tresorier.id)])
            
    #         for transfert in transferts:
    #             print transfert
    #             total+= transfert.diff
    #             if tresorier.access.name not in res:
    #                 res[tresorier.access.name]['Total_tv'] = transfert.diff
    #             else:
    #                 res[tresorier.access.name]['Total_tv'] = total
    #     print '###################################'
    #     print res
    #     print '###################################'
    #     datas = []
    #     print aaaa
    #     return self.env['report'].get_action(self, 'benin_petro.gouvernor', data=datas)       

    @api.multi
    def print_report(self):
        ds=datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
        de=datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
        
        liste_produit = self.env['product.product'].search([])
        res={}
        client_name = ""
        produit = "Tous"
        data_len = []
        i=0
        k=0
        c=0
        for pr in liste_produit:
            if self.point_vente_id and not self.product_id:
                if self.type_vente:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=',self.type_vente),('point_vente_id','=',self.point_vente_id.id),('product_ids','=',pr.id)])
                else:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('product_ids','=',pr.id)])
            if self.product_id and not self.point_vente_id:
                produit = self.product_id.name 
                if self.type_vente:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=',self.type_vente),('product_ids','=',self.product_id.id),('product_ids','=',pr.id),('point_vente_id','=',self.point_vente_id.id)])
                else:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('product_ids','=',self.product_id.id),('product_ids','=',pr.id),('point_vente_id','=',self.point_vente_id.id)])
            if self.product_id and self.point_vente_id:
                produit = self.product_id .name
                if self.type_vente:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=',self.type_vente),('point_vente_id','=',self.point_vente_id.id),('product_ids','=',self.product_id.id),('product_ids','=',pr.id)])
                else:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('product_ids','=',self.product_id.id),('product_ids','=',pr.id)])
            else:
                if self.type_vente:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','=',self.type_vente),('product_ids','=',pr.id),('point_vente_id','=',self.point_vente_id.id)])
                else:
                    liste_transactions = self.env['benin_petro.carte.consommation'].search([('product_ids','=',pr.id),('point_vente_id','=',self.point_vente_id.id)])
            data = {}
            print "#########################"
            print len(liste_transactions)
            print "#########################"
            
            if len(liste_transactions) >0:
                for tr in liste_transactions:
                    print tr
                    if pr.name not in res:
                        if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                            if tr.type_vente == 'Vente par TV':
                                client_name = tr.ticket_id.client.name
                            if tr.type_vente == 'Vente par SUBLIME CARTE':
                                client_name = tr.carte_id.owner_id.name

                            dat = {
                                'produit':tr.product_ids.name,
                                'client':client_name,
                                'qte':tr.quantite,
                                'nombre_tr':1,
                                'montant_horstaxe':tr.total_hors_taxe,
                                'tva':tr.total_tva,
                                'montant_ttc':tr.montant,
                                }

                            if client_name not in data:
                                data[client_name] = dat
                                i=i+1
                            else:
                                data[client_name]['qte']=float(tr.quantite)
                                data[client_name]['nombre_tr']=int(1)
                                data[client_name]['montant_horstaxe']=float(tr.total_hors_taxe)
                                data[client_name]['tva']=float(tr.total_tva)
                                data[client_name]['montant_ttc']=float(tr.montant)
                            res[pr.name] = data
                            
                    else:
                        if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                            if tr.type_vente == 'Vente par TV':
                                client_name = tr.ticket_id.client.name
                            if tr.type_vente == 'Vente par SUBLIME CARTE':
                                client_name = tr.carte_id.owner_id.name

                            dat = {
                                'produit':tr.product_ids.name,
                                'client':client_name,
                                'qte':tr.quantite,
                                'nombre_tr':1,
                                'montant_horstaxe':tr.total_hors_taxe,
                                'tva':tr.total_tva,
                                'montant_ttc':tr.montant,
                                }

                            if client_name not in data:
                                data[client_name] = dat
                                i=i+1 
                            else:
                                
                                qte = float(str(data[client_name]['qte']).replace(",", ""))
                                nombre_tr = float(str(data[client_name]['nombre_tr']).replace(" ", ""))
                                montant_horstaxe = float(str(data[client_name]['montant_horstaxe']).replace(",", ""))
                                tva = float(str(data[client_name]['tva']).replace(",", ""))
                                montant_ttc = float(str(data[client_name]['montant_ttc']).replace(",", ""))
                                data[client_name]['qte']=locale.format("%d", float(qte+float(tr.quantite)), grouping=True)
                                data[client_name]['nombre_tr']=int(data[client_name]['nombre_tr'])+int(1)
                                data[client_name]['montant_horstaxe']=locale.format("%d", float(montant_horstaxe+float(tr.total_hors_taxe)), grouping=True)
                                data[client_name]['tva']=locale.format("%d", float(tva+float(tr.total_tva)), grouping=True)
                                data[client_name]['montant_ttc']=locale.format("%d", float(montant_ttc+float(tr.montant)), grouping=True)   
                            res[pr.name] = data
                            # if i == 14:
                            #     data_len.append(res)
                            #     res = {}
                            #     i=0
                            #     k = k+1
                            # if (float(float(len(liste_transactions))+float(len(liste_produit))) - float(14*k))<14 and c != -1:
                            #     data_len.append(res)
                            #     c=-1
        # for key,val in res.items(): 
        #     print val  
            # for v in val:
            #     print "##################################"
            #     print v
            #     print "##################################"
        gerant = ''
        adresse = ''
        email = ''
        telephone = ''
        if self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')]):    
            gerant = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])[0].name
            adresse = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])[0].adress
            email = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])[0].mail
            telephone = self.env['benin_petro.agent'].search([('point_vente_id','=',self.point_vente_id.id),('fonction','=','Gerant')])[0].telephone
        
        sum_qte = 0
        sum_nombre_tr = 0
        sum_montant_horstaxe = 0
        sum_tva = 0
        sum_montant_ttc = 0    
        j=0
        for key,val in res.items():
            
            if len(val)==0:
                del res[key]
           
            for k,v in val.items():
                j= j+1
                sum_qte += float(str(v["qte"]).replace(",", ""))
                sum_nombre_tr += float(str(v["nombre_tr"]).replace(",", ""))
                sum_montant_horstaxe += float(str(v["montant_horstaxe"]).replace(",", ""))
                sum_tva += float(str(v["tva"]).replace(",", ""))
                sum_montant_ttc += float(str(v["montant_ttc"]).replace(",", ""))
        # print '/////////////////////////////////'
        # print j
        # print '/////////////////////////////////'
        total = {"qte":locale.format("%d", float(sum_qte), grouping=True),"sum_nombre_tr":locale.format("%d", float(sum_nombre_tr), grouping=True),"sum_montant_horstaxe":locale.format("%d", float(sum_montant_horstaxe), grouping=True),"sum_tva":locale.format("%d", float(sum_tva), grouping=True),"sum_montant_ttc":locale.format("%d", float(sum_montant_ttc), grouping=True)}
        
        type_vente = ""
        if self.type_vente == 'Vente par SUBLIME CARTE':
            type_vente = 'SUBLIME CARTE'
        if self.type_vente == 'Vente par TV':
            type_vente = 'TV'
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        
        datas = {
                'form':
                {
                    'date_debut':self.start_date,
                    'date_fin':self.end_date,
                    'print_date':d1,
                    'point_vente': self.point_vente_id.name,
                    'type_vente': type_vente,
                    'gerant': gerant,
                    'produit':produit,
                    'adresse': self.point_vente_id.promoteur.street,
                    'telephone': telephone,
                    'email':email,
                    'promoteur':self.point_vente_id.promoteur.name,
                    'transactions':res,
                    'total':total,
                    }
            }
        print len(data_len)
        return self.env['report'].get_action(self, 'benin_petro.chiffre_affaire_report', data=datas)

class chiffre_affaire_report(models.AbstractModel):
    _name = 'report.benin_petro.chiffre_affaire_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.chiffre_affaire_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.chiffre_affaire_report', docargs)
