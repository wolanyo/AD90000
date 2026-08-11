from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import locale
import dateutil.parser


class releve_tresorier_xlsx(ReportXlsx):

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
        sheet.write(0, 3, "Releve des operations par tresoriers", bold)
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

        sheet.write(4, 0, "Tresorier : ", bold)
        sheet.write(4, 1, liste["form"]["tresorier"], bold)
        sheet.write(4, 2, "")
        sheet.write(4, 3, "")
        sheet.write(4, 4, "Type : ", bold)
        sheet.write(4, 5, liste["form"]["type"], bold)
        sheet.write(4, 6, "")

        sheet.write(5, 0, "")
        sheet.write(5, 1, "")
        sheet.write(5, 2, "")
        sheet.write(5, 3, "")
        sheet.write(5, 4, "")
        sheet.write(5, 5, "")
        sheet.write(6, 6, "")

        sheet.write(6, 0, "Date d'execution", bold)
        sheet.write(6, 1, "Libelle", bold)
        sheet.write(6, 2, "Solde initial", bold)
        sheet.write(6, 3, "Debit", bold)
        sheet.write(6, 4, "Credit", bold)
        sheet.write(6, 5, "Solde final", bold)
        i = 6
        for v in dt:
            i = i+1
            sheet.write(i, 0, v['date_releve'], normal)
            sheet.write(i, 1, v['libelle'], normal)
            sheet.write(i, 2, v['solde_initial'], normal)
            sheet.write(i, 3, v['debit'], normal)
            sheet.write(i, 4, v['credit'], normal)
            sheet.write(i, 5, v['solde'], normal)

        sheet.write(i+1, 0, "Total", bold)
        sheet.write(i+1, 1, '', bold)
        sheet.write(i+1, 2, liste["form"]["total"]["solde_initial"], bold)
        sheet.write(i+1, 3, liste["form"]["total"]["debit"], bold)
        sheet.write(i+1, 4, liste["form"]["total"]["credit"], bold)
        sheet.write(i+1, 5, liste["form"]["total"]["solde"], bold)

    @api.multi
    def get_date(self, obj):
        ds=dateutil.parser.parse(obj.start_date).date()
        de=dateutil.parser.parse(obj.end_date).date()
        data = []
        total = {}
        reste_carte = 0
        if obj.tresorier.id:
            liste_conso = obj.env["benin_petro.historique"].search([("chargeur","=",obj.tresorier.id),('type_af',"=",obj.type_affect)])
            print liste_conso
            for conso in liste_conso:
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(conso.create_date).date()<= de:
                    debit = 0
                    credit = 0
                    if conso.montant_init > conso.montant_fin:
                        debit = conso.diff
                        credit = 0
                    else:
                        credit = conso.diff
                        debit = 0
                    if conso.diff !=0 :
                        data.append({'date_releve':conso.create_date,'libelle':conso.type_op,'debit': float(debit),'credit': float(credit),'solde': float(conso.montant_fin),'solde_initial': float(conso.montant_init),'type_affect':conso.type_af})
            #print data
        data.sort(key = lambda x:x['date_releve'])
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            debit += float(v["debit"])
            credit += float(v["credit"])
            solde += float(v["solde"])
            solde_initial += float(v["solde_initial"])
        total = {"debit":float(debit),"credit": float(credit),"solde": float(solde),"solde_initial": float(solde_initial)}
        print total
        datas = {
                'form':
                {
                    'date_debut':datetime.strptime(obj.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin':datetime.strptime(obj.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date':d1,
                    'tresorier':obj.tresorier.access.name,
                    'type':obj.type_affect,
                    'transactions':data,
                    'total':total,
                }
        }

        return datas


releve_tresorier_xlsx('report.releve_tresorier.xlsx',
                            'benin_petro.releve_cassier_tresorier')
