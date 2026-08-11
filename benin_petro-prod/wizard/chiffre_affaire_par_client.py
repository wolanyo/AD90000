# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_chiffre_affaire_par_client(models.TransientModel):
    _name = 'benin_petro.wizard.chiffre_affaire_par_client'

    point_vente_id=fields.Many2one('benin_petro.point.vente', string='Point de  Vente')
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

    @api.multi
    def print_report(self):
        ds= str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S'))
        de= str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S'))
        ds_format= str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        de_format= str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        print(ds)
        print(de)
        liste_produits = self.env['product.product'].search([('categories_consomable','=','Produits blancs')])
        print(liste_produits)
        data = {}
        for p in liste_produits:
            liste_transactions = self.env['benin_petro.carte.consommation'].search([('product_ids','=',p.id),('type_vente','=','Vente par SUBLIME CARTE'),('create_date','>=',ds),('create_date','<=',de)])
            res={}
            montant_total = 0
            qte_total = 0
            for tr in liste_transactions:
                client_name = tr.carte_id.owner_id.name
                montant_total = montant_total + tr.montant
                if client_name == "BENIN PETRO SA" and p.name == "GASOIL":
                    print(tr.quantite)
                qte_total = float(qte_total) + float(tr.quantite)
                if client_name not in res:
                    res[client_name] = {
                        'montant': tr.montant,
                        'qte': tr.quantite,
                    }
                else:
                    res[client_name]["montant"] = (float(res[client_name]["montant"]) + float(tr.montant))
                    res[client_name]["qte"] = round((float(res[client_name]["qte"]) + float(tr.quantite)),2)

            res["total"] = {
                'montant': round(montant_total),
                'qte': round(qte_total,2),
            }
            data[p.name] = res

        datas = {
                'form':
                {
                    'date_debut':self.start_date,
                    'date_fin':self.end_date,
                    'data':data
                    }
            }
        print(datas)
        return self.env['report'].get_action(self, 'benin_petro.chiffre_affaire_par_client_report', data=datas)

class chiffre_affaire_par_client_report(models.AbstractModel):
    _name = 'report.benin_petro.chiffre_affaire_par_client_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.chiffre_affaire_par_client_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.chiffre_affaire_par_client_report', docargs)
