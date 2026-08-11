from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import fields, api, models, _
import xlsxwriter
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time


class retour_bon_consomation_xlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        # print lines.end_date
        # self.env['benin_petro.wizard.detail_consommation_par_carte'].print_report(lines)
        liste = self.get_date(lines)
        dt = liste["form"]["transactions"]
        print '############'
        print dt

        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'border': 1, 'font_size': 16})
        normal = workbook.add_format({'bold': False, 'border': 1, 'font_size': 16})

        sheet.write(0, 0, "")
        sheet.write(0, 1, "")
        sheet.write(0, 2, "")
        sheet.write(0, 3, "Etat recapitulatif de retour des bons de consommation de Produit", bold)
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


        sheet.write(5, 0, "GERANT : ", bold)
        sheet.write(5, 1, liste["form"]["gerant"], bold)
        sheet.write(5, 2, "")
        sheet.write(5, 3, "")
        sheet.write(5, 4, "Email", bold)
        sheet.write(5, 5, liste["form"]["email"], bold)


        sheet.write(6, 0, "ADRESSE : ", bold)
        sheet.write(6, 1, liste["form"]["adresse"], bold)
        sheet.write(6, 2, "")
        sheet.write(6, 3, "")
        sheet.write(6, 4, "Telephone", bold)
        sheet.write(6, 5, liste["form"]["telephone"], bold)


        sheet.write(7, 0, "Reference : ", bold)
        sheet.write(7, 1, liste["form"]["point_vente"], bold)
        sheet.write(7, 2, "")
        sheet.write(7, 3, "")
        sheet.write(7, 4, "")
        sheet.write(7, 5, "")


        sheet.write(8, 0, "PRODUIT : ", bold)
        sheet.write(8, 1, liste["form"]["produit"], bold)
        sheet.write(8, 2, "")
        sheet.write(8, 3, "")
        sheet.write(8, 4, "")
        sheet.write(8, 5, "")

        sheet.write(9, 0, "")
        sheet.write(9, 1, "")
        sheet.write(9, 2, "")
        sheet.write(9, 3, "")
        sheet.write(9, 4, "")
        sheet.write(9, 5, "")

        sheet.write(10, 0, "")
        sheet.write(10, 1, "")
        sheet.write(10, 2, "")
        sheet.write(10, 3, "")
        sheet.write(10, 4, "")
        sheet.write(10, 5, "")

        sheet.write(11, 0, "Client", bold)
        sheet.write(11, 1, "Nombre de bon", bold)
        sheet.write(11, 2, "Quantite", bold)
        sheet.write(11, 3, "Prix HT", bold)
        sheet.write(11, 4, "TVA", bold)
        sheet.write(11, 5, "MONTANT TTC", bold)
        i = 11
        for key,v in dt.items():
            i = i+1
            print(int(i))
            print(v)
            sheet.write(int(i), 0, v['type'], normal)
            sheet.write(int(i), 1, v['nombre_tv'], normal)
            sheet.write(int(i), 2, v['qte'], normal)
            sheet.write(int(i), 3, v['montant_horstaxe'], normal)
            sheet.write(int(i), 4, v['tva'], normal)
            sheet.write(int(i), 5, v['montant_ttc'], normal)

#        sheet.write(int(i+1), 0, "Total", bold)
#        sheet.write(int(i+1), 1, liste["form"]["total"]["sum_nombre_tv"], bold)
#        sheet.write(int(i+1), 2, liste["form"]["total"]["qte"], bold)
#        sheet.write(int(i+1), 3, liste["form"]["total"]["sum_montant_horstaxe"], bold)
#        sheet.write(int(i+1), 4, liste["form"]["total"]["sum_tva"], bold)
#        sheet.write(int(i+1), 5, liste["form"]["total"]["sum_montant_ttc"], bold)

    @api.multi
    def get_date(self, obj):
        import pytz
        user_tz = obj.env.user.tz or pytz.utc
        print(user_tz)
        local = pytz.timezone(user_tz)
        print(local)
        ds = datetime.strftime(pytz.utc.localize(datetime.strptime(obj.start_date,DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        de = datetime.strftime(pytz.utc.localize(datetime.strptime(obj.end_date,DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        ds=datetime.strptime(ds, '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)
        de=datetime.strptime(de, '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)
        
        res={}
        data = {}
        if obj.type_vente:
            if obj.product_id.id:
                liste_transactions = obj.env['benin_petro.carte.consommation'].search([('point_vente_id','=',obj.point_vente_id.id),('type_vente','=',obj.type_vente),('product_ids','=',obj.product_id.id)])
            else:
                liste_transactions = obj.env['benin_petro.carte.consommation'].search([('point_vente_id','=',obj.point_vente_id.id),('type_vente','=',obj.type_vente)])

        else:
            if obj.product_id.id:
                liste_transactions = obj.env['benin_petro.carte.consommation'].search([('point_vente_id','=',obj.point_vente_id.id),('product_ids','=',obj.product_id.id)])
            else:
                liste_transactions = obj.env['benin_petro.carte.consommation'].search([('point_vente_id','=',obj.point_vente_id.id)])
        
        for tr in liste_transactions:
            if datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tr.create_date, '%Y-%m-%d %H:%M:%S')<= de:
                print(tr)
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
        gerant = obj.env['benin_petro.agent'].search([('point_vente_id','=',obj.point_vente_id.id),('fonction','=','Gerant')])
        if gerant:
            gerant = gerant[0].name
        else:
            gerant = ""
        adresse = obj.env['benin_petro.agent'].search([('point_vente_id','=',obj.point_vente_id.id),('fonction','=','Gerant')])
        if adresse:
            adresse = adresse[0].adress
        else:
            adresse = ""
        email = obj.env['benin_petro.agent'].search([('point_vente_id','=',obj.point_vente_id.id),('fonction','=','Gerant')])
        if email:
            email = email[0].mail
        else:
            email = ""
        telephone = obj.env['benin_petro.agent'].search([('point_vente_id','=',obj.point_vente_id.id),('fonction','=','Gerant')])
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
        if obj.type_vente == 'Vente par SUBLIME CARTE':
            type_vente = 'SUBLIME CARTE'
        if obj.type_vente == 'Vente par TV':
            type_vente = 'TV'
        
        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        if obj.product_id:
            produit = obj.product_id.name
        else:
            produit = "Tous"
        datas = {
                 'form':
                    {
                        'date_debut':str(datetime.strptime(str(ds + timedelta(hours=1)) , '%Y-%m-%d %H:%M:%S')),
                        'date_fin':str(datetime.strptime(str(de + timedelta(hours=1)) , '%Y-%m-%d %H:%M:%S')),
                        'print_date':d1,
                        'point_vente': obj.point_vente_id.name,
                        'produit': produit,
                        'type_vente': type_vente,
                        'gerant': gerant,
                        'adresse': obj.point_vente_id.promoteur.street,
                        'telephone': telephone,
                        'email':email,
                        'promoteur':obj.point_vente_id.promoteur.name,
                        'transactions':res,
                        'test':test
                        
                     }
                }

        return datas


retour_bon_consomation_xlsx('report.retour_bon_consommation.xlsx',
                            'benin_petro.wizard.retour_bon_consommation')
