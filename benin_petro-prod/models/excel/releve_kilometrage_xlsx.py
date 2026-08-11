from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import locale
import dateutil.parser


class releve_kilometrage_xlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        # print lines.end_date
        # self.env['benin_petro.wizard.detail_consommation_par_carte'].print_report(lines)
        liste = self.get_date(lines)
        dt = liste["form"]["transactions"]

        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'border': 1, 'font_size': 16})
        normal = workbook.add_format({'bold': False, 'border': 1, 'font_size': 16})

        sheet.write(0, 0, "")
        sheet.write(0, 1, "")
        sheet.write(0, 2, "")
        sheet.write(0, 3, "Rapport de kilometrage", bold)
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

        sheet.write(4, 0, "Client : ", bold)
        sheet.write(4, 1, liste["form"]["client"], bold)
        sheet.write(4, 2, "")
        sheet.write(4, 3, "")
        sheet.write(4, 4, "")
        sheet.write(4, 5, "")
        sheet.write(4, 6, "")

        sheet.write(5, 0, "")
        sheet.write(5, 1, "")
        sheet.write(5, 2, "")
        sheet.write(5, 3, "")
        sheet.write(5, 4, "")
        sheet.write(5, 5, "")
        sheet.write(5, 6, "")

        sheet.write(6, 0, "Date", bold)
        sheet.write(6, 1, "PDV", bold)
        sheet.write(6, 2, "Operation", bold)
        sheet.write(6, 3, "Service", bold)
        sheet.write(6, 4, "Kilometrage", bold)
        sheet.write(6, 5, "Quantite", bold)
        i = 6
        for key,val in dt.items():
            i = i+1
            print "###########"
            print key 
            print i
            sheet.write(i, 0, key, bold)
            sheet.write(i, 1, "")
            sheet.write(i, 2, "")
            sheet.write(i, 3, "")
            sheet.write(i, 4, "")
            sheet.write(i, 5, "")
            for k,v in val.items():
                i = i+1
                print i
                sheet.write(i, 0, "")
                sheet.write(i, 1, k, bold)
                sheet.write(i, 2, "")
                sheet.write(i, 3, "")
                sheet.write(i, 4, v["porteur"], bold)
                for t in v["transcation"]:
                    i = i+1
                    sheet.write(i, 0, t["date_kilometrage"], normal)
                    sheet.write(i, 1, t["point_vente"], normal)
                    sheet.write(i, 2, t["produit"], normal)
                    sheet.write(i, 3, t["type_operation"], normal)
                    sheet.write(i, 4, t["kilometrage"], normal)
                    sheet.write(i, 5, t["quantite"], normal)
                # print aaaaa
        
        # print aaaaa
        #     i = i+1
        #     sheet.write(i, 0, v['date_releve'], normal)
        #     sheet.write(i, 1, v['libelle'], normal)
        #     sheet.write(i, 2, v['solde_initial'], normal)
        #     sheet.write(i, 3, v['debit'], normal)
        #     sheet.write(i, 4, v['credit'], normal)
        #     sheet.write(i, 5, v['solde'], normal)

        # sheet.write(i+1, 0, "Total", bold)
        # sheet.write(i+1, 1, '', bold)
        # sheet.write(i+1, 2, liste["form"]["total"]["solde_initial"], bold)
        # sheet.write(i+1, 3, liste["form"]["total"]["debit"], bold)
        # sheet.write(i+1, 4, liste["form"]["total"]["credit"], bold)
        # sheet.write(i+1, 5, liste["form"]["total"]["solde"], bold)

    @api.multi
    def get_date(self, obj):
        ds=dateutil.parser.parse(obj.start_date).date()
        de=dateutil.parser.parse(obj.end_date).date()
        if obj.client:
            liste_kilometrage = obj.env["benin_petro.kilometrage"].search([('client','=',obj.client.id)])
        else:
            liste_kilometrage = obj.env["benin_petro.kilometrage"].search([])
        res={}
        data = []
        for conso in liste_kilometrage:
            if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                # print conso.carte_id.owner_id.name 
                data_res_carte = []
                if conso.carte_id.owner_id.name not in res:
                    res_carte = {}
                    if 'Carte : '+str(conso.carte_id.num_serie) not in res_carte:
                        data = []
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : data
                        }
                    else:
                        data =  res_carte['Carte : '+str(conso.carte_id.num_serie)]['transcation']
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : data
                        }
                    res[conso.carte_id.owner_id.name] = res_carte
                else:
                    res_carte = {}
                    if 'Carte : '+str(conso.carte_id.num_serie) in res[conso.carte_id.owner_id.name]:
                        data =  res[conso.carte_id.owner_id.name]['Carte : '+str(conso.carte_id.num_serie)]['transcation']
                        data.append({'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite})
                    else:
                        data = []
                        # print res[conso.carte_id.owner_id.name]
                        # print 'Carte : '+str(conso.carte_id.num_serie)
                        res_carte = res[conso.carte_id.owner_id.name]
                        res_carte['Carte : '+str(conso.carte_id.num_serie)] = {
                            'porteur': 'Porteur : '+ str(conso.carte_id.libelle.name),
                            'transcation' : [{'date_kilometrage':conso.create_date,'point_vente':conso.point_vente.name,'produit':conso.produit.name,'type_operation':conso.type_operation,'kilometrage':conso.kilometrage,'quantite':conso.quantite}]
                        }

                        # print res_carte
                        res[conso.carte_id.owner_id.name] = res_carte

        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if obj.client:
            client = obj.client.name
        else:
            client = 'Tous'
        datas = {
            'form':
                {
                    'date_debut':str(datetime.strptime(obj.start_date, '%Y-%m-%d %H:%M:%S')),
                    'date_fin':str(datetime.strptime(obj.end_date, '%Y-%m-%d %H:%M:%S')),
                    'client':client,
                    'print_date':d1,
                    'transactions' : res
                }
        }

        return datas


releve_kilometrage_xlsx('report.releve_kilometrage.xlsx',
                            'benin_petro.rapport_kilometrage')
