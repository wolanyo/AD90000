from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import locale
import dateutil.parser


class suivie_compte_client_xlsx(ReportXlsx):

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
        sheet.write(0, 3, "Releve des comptes clients", bold)
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

        sheet.write(5, 0, "")
        sheet.write(5, 1, "")
        sheet.write(5, 2, "")
        sheet.write(5, 3, "")
        sheet.write(5, 4, "")
        sheet.write(5, 5, "")

        sheet.write(6, 0, "Date d'execution", bold)
        sheet.write(6, 1, "Libelle", bold)
        sheet.write(6, 2, "Debit", bold)
        sheet.write(6, 3, "Credit", bold)
        sheet.write(6, 4, "Solde final", bold)
        i = 6
        for v in dt:
            print v['libelle']
            i = i+1
            sheet.write(i, 0, v['date_releve'], normal)
            sheet.write(i, 1, v['libelle'], normal)
            sheet.write(i, 2, v['debit'], normal)
            sheet.write(i, 3, v['credit'], normal)
            sheet.write(i, 4, v['solde'], normal)

        sheet.write(i+1, 0, "Total", bold)
        sheet.write(i+1, 1, '', bold)
        sheet.write(i+1, 2, liste["form"]["total"]["debit"], bold)
        sheet.write(i+1, 3, liste["form"]["total"]["credit"], bold)
        sheet.write(i+1, 4, liste["form"]["total"]["solde"], bold)

    @api.multi
    def get_date(self, obj):
        print 'hamadaaaaaaa'
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        ds = dateutil.parser.parse(obj.start_date).date()
        de = dateutil.parser.parse(obj.end_date).date()
        data = []
        total = {}
        if obj.client_id.id:
            liste_affectation = obj.env["benin_petro.log"].search(
                [("client_id", "=", obj.client_id.id), ('champ', '=', 'Solde non affecte')])
            libelle = ''
            debit = ''
            credit = ''
            solde = 0
            for affect in liste_affectation:
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    if float(affect.old_version) > float(affect.new_version):
                        libelle = 'Approvisionnement CARTE'
                        debit = float(affect.old_version) - float(affect.new_version)
                        credit = 0
                        solde -= float(debit)
                    else:
                        libelle = 'RECHARGE'
                        debit = 0
                        credit = float(affect.new_version) - float(affect.old_version)
                        solde += float(credit)
                    data.append({'date_releve': affect.create_date, 'libelle': libelle,
                                 'debit': locale.format("%d", float(debit), grouping=True),
                                 'credit': locale.format("%d", float(credit), grouping=True),
                                 'solde': locale.format("%d", float(solde), grouping=True)})
        data.sort(key=lambda x: x['date_releve'])

        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1, minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        debit = 0
        credit = 0
        solde = 0
        solde_initial = 0
        for v in data:
            if " " in str(v["debit"]):
                debit += float(v["debit"].replace(" ", "").replace(",", ""))
            else:
                debit += float(v["debit"])

            if " " in str(v["credit"]):
                credit += float(v["credit"].replace(" ", "").replace(",", ""))
            else:
                credit += float(v["credit"].replace(" ", "").replace(",", ""))

            if " " in str(v["solde"]):
                solde += float(v["solde"].replace(" ", "").replace(",", ""))
            else:
                solde += float(v["solde"])
        total = {"debit": locale.format("%d", float(debit), grouping=True),
                 "credit": locale.format("%d", float(credit), grouping=True),
                 "solde": locale.format("%d", float(solde), grouping=True)}

        datas = {
            'form':
                {
                    'date_debut': datetime.strptime(obj.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin': datetime.strptime(obj.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date': d1,
                    'client': obj.client_id.name,
                    'transactions': data,
                    'total': total,
                }
        }

        return datas


suivie_compte_client_xlsx('report.suivie_compte_client.xlsx',
                            'benin_petro.releve_compte')
