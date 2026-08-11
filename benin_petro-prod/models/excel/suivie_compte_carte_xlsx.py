from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import locale
import dateutil.parser


class suivie_compte_carte_xlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        # print lines.end_date
        # self.env['benin_petro.wizard.detail_consommation_par_carte'].print_report(lines)
        liste = self.get_data(lines)
        dt = liste["form"]["transactions"]

        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'border': 1, 'font_size': 16})
        normal = workbook.add_format({'bold': False, 'border': 1, 'font_size': 16})

        sheet.write(0, 0, "")
        sheet.write(0, 1, "")
        sheet.write(0, 2, "")
        sheet.write(0, 3, "Releve des comptes clients par carte", bold)
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

        sheet.write(4, 0, "Consommateur : ", bold)
        sheet.write(4, 1, liste["form"]["consommateur"], bold)
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
    def get_data(self, obj):
        ds = dateutil.parser.parse(obj.start_date).date()
        de = dateutil.parser.parse(obj.end_date).date()
        data = []
        total = {}
        reste_carte = 0
        if obj.consommateur.id:
            liste_conso = obj.env["benin_petro.carte.consommation"].search([("carte_id", "=", obj.consommateur.id)])

            for conso in liste_conso:
                print
                dateutil.parser.parse(conso.create_date).date()
                if dateutil.parser.parse(conso.create_date).date() >= ds and dateutil.parser.parse(
                        conso.create_date).date() <= de:
                    if conso.reste_carte:
                        reste_carte = conso.reste_carte
                    data.append({'date_releve': conso.create_date, 'libelle': 'CONSOMMATION',
                                 'debit': float(conso.montant), 'credit': 0,
                                 'solde': float(reste_carte)})
            liste_affectation = obj.env["benin_petro.log"].search(
                [("carte_id", "=", obj.consommateur.id), ('champ', '=', 'Solde')])
            for affect in liste_affectation:
                if dateutil.parser.parse(affect.create_date).date() >= ds and dateutil.parser.parse(
                        affect.create_date).date() <= de:
                    credit = float(affect.new_version) - float(affect.old_version)
                    data.append({'date_releve': affect.create_date, 'libelle': 'APPROVISIONNEMENT', 'debit': 0,
                                 'credit': float(credit),
                                 'solde': float(credit + float(affect.old_version))})
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
                debit += float(v["debit"])
            else:
                debit += float(v["debit"])

            if " " in str(v["credit"]):
                credit += float(v["credit"])
            else:
                credit += float(v["credit"])

            if " " in str(v["solde"]):
                solde += float(v["solde"])
            else:
                solde += float(v["solde"])
        total = {"debit": float(debit),
                 "credit": float(credit),
                 "solde": float(solde)}

        datas = {
            'form':
                {
                    'date_debut': datetime.strptime(obj.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin': datetime.strptime(obj.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date': d1,
                    'consommateur': obj.consommateur.libelle.name,
                    'transactions': data,
                    'total': total,
                }
        }

        return datas


suivie_compte_carte_xlsx('report.suivie_compte_carte.xlsx',
                            'benin_petro.releve_compte')
