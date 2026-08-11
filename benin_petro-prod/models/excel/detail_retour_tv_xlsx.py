from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time


class detail_retour_tv_xlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        # print lines.end_date
        # self.env['benin_petro.wizard.detail_consommation_par_carte'].print_report(lines)
        liste = self.getdata(lines)
        dt = liste["form"]["transaction"]

        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'border': 1, 'font_size': 16})
        normal = workbook.add_format({'bold': False, 'border': 1, 'font_size': 16})

        sheet.write(0, 0, "")
        sheet.write(0, 1, "")
        sheet.write(0, 2, "")
        sheet.write(0, 3, "Detail retour TV", bold)
        sheet.write(0, 4, "")
        sheet.write(0, 5, "")

        sheet.write(1, 0, "")
        sheet.write(1, 1, "")
        sheet.write(1, 2, "")
        sheet.write(1, 3, "")
        sheet.write(1, 4, "")
        sheet.write(1, 5, "")

        sheet.write(2, 0, "Date debut : ", bold)
        sheet.write(2, 1, liste["form"]["date_debut"], bold)
        sheet.write(2, 2, "")
        sheet.write(2, 3, "")
        sheet.write(2, 4, "Date fin", bold)
        sheet.write(2, 5, liste["form"]["date_fin"], bold)

        sheet.write(3, 0, "")
        sheet.write(3, 1, "")
        sheet.write(3, 2, "")
        sheet.write(3, 3, "")
        sheet.write(3, 4, "")
        sheet.write(3, 5, "")

        sheet.write(4, 0, "")
        sheet.write(4, 1, "")
        sheet.write(4, 2, "")
        sheet.write(4, 3, "")
        sheet.write(4, 4, "")
        sheet.write(4, 5, "")

        sheet.write(5, 0, "TYPE", bold)
        sheet.write(5, 1, "NUMERO TICKET", bold)
        sheet.write(5, 2, "NUMERO INCREMENTER", bold)
        sheet.write(5, 3, "CODE CLIENT", bold)
        sheet.write(5, 4, "NOM CLIENT", bold)
        sheet.write(5, 5, "PRODUIT", bold)
        sheet.write(5, 6, "QTE", bold)
        sheet.write(5, 7, "COUT UNITAIRE", bold)
        sheet.write(5, 8, "MONTANT", bold)
        sheet.write(5, 9, "CODE STATION", bold)
        sheet.write(5, 10, "NOM STATION", bold)
        sheet.write(5, 11, "DATE D'EDITION", bold)
        sheet.write(5, 12, "DATE DE CONSOMMATION", bold)

        i = 5
        for v in dt:
            i = i+1
            sheet.write(int(i), 0, v['ticket_type'], normal)
            sheet.write(int(i), 1, v['numTicket'], normal)
            sheet.write(int(i), 2, v['numIncremen'], normal)
            sheet.write(int(i), 3, v['client'], normal)
            sheet.write(int(i), 4, v['codeClient'], normal)
            sheet.write(int(i), 5, v['produit'], normal)
            sheet.write(int(i), 6, v['quantite'], normal)
            sheet.write(int(i), 7, v['prixProduit'], normal)
            sheet.write(int(i), 8, v['montant'], normal)
            sheet.write(int(i), 9, v['station'], normal)
            sheet.write(int(i), 10, v['stationName'], normal)
            sheet.write(int(i), 11, v['dateDebut'], normal)
            sheet.write(int(i), 12, v['dateFin'], normal)

#        sheet.write(int(i+1), 0, "Total", bold)
#        sheet.write(int(i+1), 1, liste["form"]["total"]["sum_nombre_tv"], bold)
#        sheet.write(int(i+1), 2, liste["form"]["total"]["qte"], bold)
#        sheet.write(int(i+1), 3, liste["form"]["total"]["sum_montant_horstaxe"], bold)
#        sheet.write(int(i+1), 4, liste["form"]["total"]["sum_tva"], bold)
#        sheet.write(int(i+1), 5, liste["form"]["total"]["sum_montant_ttc"], bold)

    @api.multi
    def getdata(self,obj):
        datas = []
        res = []
        ds= str(datetime.strptime(obj.start_date, '%Y-%m-%d %H:%M:%S'))
        de= str(datetime.strptime(obj.end_date, '%Y-%m-%d %H:%M:%S'))
        ds_format= str(datetime.strptime(obj.start_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        de_format= str(datetime.strptime(obj.end_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        liste_transactions = obj.env['benin_petro.carte.consommation'].search([('type_vente','>=','Vente par TV'),('create_date','>=',ds),('create_date','<=',de)])
        for t in liste_transactions:
            if t.quantite != 0:
                prixProduit = int(round(t.montant / t.quantite))
            else:
                prixProduit = 0
            for tv in t.ticket_ids:
                if prixProduit != 0 :
                    qte = float(format((float(tv.tv_type.montant) / float(prixProduit)),'.3f'))
                else:
                    qte = 0
                if tv.client.codeClient:
                    codeClient = tv.client.codeClient
                else:
                    codeClient = ''
                ligne = {
                    'ticket_type' : tv.tv_type.libelle,
                    'numTicket' : tv.num_serie,
                    'numIncremen' : tv.num_serie_incr,
                    'client':codeClient,
                    'codeClient':tv.client.name,
                    'produit' : t.product_ids.name,
                    'quantite' : qte,
                    'prixProduit' : prixProduit,
                    'montant' : tv.tv_type.montant,
                    'station' : t.point_vente_id.libelle,
                    'stationName' : t.point_vente_id.name,
                    'dateDebut' : str(datetime.strptime(tv.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')),
                    'dateFin' : str(datetime.strptime(t.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
                }
                res.append(ligne)
        # print(datas)
        datas = {
            'form':
                {
                    'date_debut': ds_format,
                    'date_fin': de_format,
                    'transaction' : res
                }
        }
        return datas


detail_retour_tv_xlsx('report.detail_retour_tv.xlsx',
                            'benin_petro.wizard.detail_retour_tv')
