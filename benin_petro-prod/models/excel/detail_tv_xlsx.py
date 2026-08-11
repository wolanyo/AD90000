# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models,_
import xlsxwriter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import locale

class PartnerXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        # print lines.end_date
        # self.env['benin_petro.wizard.detail_consommation_par_carte'].print_report(lines)
        liste = self.get_date(lines)
        dt = liste["form"]["transactions"]
        # print liste["form"]["transactions"]

        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'border': 1,'font_size':16})
        normal = workbook.add_format({'bold': False, 'border': 1,'font_size':16})

        sheet.write(0, 0, "")
        sheet.write(0, 1, "")
        sheet.write(0, 2, "")
        sheet.write(0, 3, "Client : "+liste["form"]["client"], bold)
        sheet.write(0, 4, "")
        sheet.write(0, 5,  "")
        sheet.write(0, 6,  "")
        sheet.write(0, 7,  "")
        sheet.write(0, 8,  "")

        sheet.write(1, 0, "")
        sheet.write(1, 1, "")
        sheet.write(1, 2, "")
        sheet.write(1, 3,  "")
        sheet.write(1, 4, "")
        sheet.write(1, 5,  "")
        sheet.write(1, 6,  "")
        sheet.write(1, 7,  "")
        sheet.write(1, 8,  "")

        sheet.write(2, 0, "Date debut : ", bold)
        sheet.write(2, 1, liste["form"]["date_debut"], bold)
        sheet.write(2, 2, "")
        sheet.write(2, 3, "")
        sheet.write(2, 4, "Date fin", bold)
        sheet.write(2, 5, liste["form"]["date_fin"], bold)
        sheet.write(2, 6,  "")
        sheet.write(2, 7,  "")
        sheet.write(2, 8,  "")

        sheet.write(3, 0, "")
        sheet.write(3, 1, "")
        sheet.write(3, 2, "")
        sheet.write(3, 3,  "")
        sheet.write(3, 4, "")
        sheet.write(3, 5,  "")
        sheet.write(3, 6,  "")
        sheet.write(3, 7,  "")
        sheet.write(3, 8,  "")

        sheet.write(4, 0, "")
        sheet.write(4, 1, "")
        sheet.write(4, 2, "")
        sheet.write(4, 3,  "")
        sheet.write(4, 4, "")
        sheet.write(4, 5,  "")
        sheet.write(4, 6,  "")
        sheet.write(4, 7,  "")
        sheet.write(4, 8,  "")


        sheet.write(5, 0, "Date", bold)
        sheet.write(5, 1, "Carte", bold)
        sheet.write(5, 2, "Num serie", bold)
        sheet.write(5, 3, "Solde carte", bold)
        sheet.write(5, 4, "Produit", bold)
        sheet.write(5, 5, "Quantite", bold)
        sheet.write(5, 6, "Montant HT", bold)
        sheet.write(5, 7, "TVA", bold)
        sheet.write(5, 8, "MONTANT TTC", bold)
        sheet.write(5, 9, "Kilometrage", bold)
        sheet.write(5, 10, "POINT DE VENTE", bold)
        i = 5
        for v in dt:
            i = i+1
            sheet.write(i, 0, v['date'], normal)
            sheet.write(i, 1, v['carte_id'], normal)
            sheet.write(i, 2, v['carte_serie'], normal)
            sheet.write(i, 3, v['carte_solde'], normal)
            sheet.write(i, 4, v['produit'], normal)
            sheet.write(i, 5, v['qte'], normal)
            sheet.write(i, 6, v['montant_horstaxe'], normal)
            sheet.write(i, 7, v['tva'], normal)
            sheet.write(i, 8, v['montant_ttc'], normal)
            sheet.write(i, 9, v['kilometrage'], normal)
            sheet.write(i, 10, v['point_vente'], normal)
            # for key,val in dt[r].items():
            #     for v in val:
            #         i = i+1
            #         sheet.write(i, 0, v['date'], normal)
            #         sheet.write(i, 1, v['carte_id'], normal)
            #         sheet.write(i, 2, v['carte_serie'], normal)
            #         sheet.write(i, 3, v['produit'], normal)
            #         sheet.write(i, 4, v['qte'], normal)
            #         sheet.write(i, 5, v['montant_horstaxe'], normal)
            #         sheet.write(i, 6, v['tva'], normal)
            #         sheet.write(i, 7, v['montant_ttc'], normal)
            #         sheet.write(i, 8, v['point_vente'], normal)
            
#            total = liste["form"]["total"]
#            sheet.write(i+1, 0, "Total", bold)
#            sheet.write(i+1, 4, total['qte'], bold)
#            sheet.write(i+1, 5, total['sum_montant_horstaxe'], bold)
#            sheet.write(i+1, 6, total['sum_tva'], bold)
#            sheet.write(i+1, 7, total['sum_montant_ttc'], bold)

    @api.multi
    def get_date(self,obj):
        datas = []
        res = {}
        ds=str(datetime.strptime(obj.start_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1))
        de=str(datetime.strptime(obj.end_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1))
        if not obj.product_id:
            liste_transactions = obj.env['benin_petro.carte.consommation'].search([('create_date', '>=', ds), ('create_date', '<=', de),('type_vente','=','Vente par SUBLIME CARTE')])
        else:
            liste_transactions = obj.env['benin_petro.carte.consommation'].search([('create_date', '>=', ds), ('create_date', '<=', de),('type_vente','=','Vente par SUBLIME CARTE'),('product_ids','=',obj.product_id.id)])
        if len(liste_transactions) >0:
            for tr in liste_transactions:
                if obj.client_id:
                    if tr.carte_id.owner_id.id == obj.client_id.id:
                        dat = {
                                'date':tr.create_date,
                                'carte_id':tr.carte_id.libelle.name,
                                'carte_serie':tr.carte_id.num_serie,
                                'carte_solde':tr.carte_id.solde,
                                'qte':tr.quantite,
                                'produit':tr.product_ids.name,
                                'nombre_tr':1,
                                'montant_horstaxe':tr.total_hors_taxe,
                                'tva':tr.total_tva,
                                'montant_ttc':locale.format("%d", float(tr.montant)),
                                'kilometrage':tr.kilometrage,
                                'point_vente':tr.point_vente_id.name
                                }
                        datas.append(dat)
                else:
                    dat = {
                            'date':tr.create_date,
                            'carte_id':tr.carte_id.libelle.name,
                            'carte_serie':tr.carte_id.num_serie,
                            'carte_solde':tr.carte_id.solde,
                            'qte':tr.quantite,
                            'produit':tr.product_ids.name,
                            'nombre_tr':1,
                            'montant_horstaxe':tr.total_hors_taxe,
                            'tva':tr.total_tva,
                            'montant_ttc':locale.format("%d", float(tr.montant)),
                            'kilometrage':tr.kilometrage,
                            'point_vente':tr.point_vente_id.name
                            }
                    datas.append(dat)
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if obj.client_id:
            client = obj.client_id.name
        else:
            client = "Tous"
        datas = {
            'form':
            {
                'date_debut':ds,
                'date_fin':de,
                'print_date':d1,
                'produit': obj.product_id.name,
                'client': client,
                'transactions':datas,
                'total':[],
                }
        }

        return datas


PartnerXlsx('report.res.partner.xlsx',
            'benin_petro.wizard.detail_consommation_par_carte')
