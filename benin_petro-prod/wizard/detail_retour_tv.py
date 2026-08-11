# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_detail_retour_tv(models.TransientModel):
    _name = 'benin_petro.wizard.detail_retour_tv'

    client_id = fields.Many2one('res.partner', string='Client')

    start_date = fields.Datetime(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )
    end_date = fields.Datetime(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )


    def print_excel_report(self):
        datas={"ihoi":"ppppp"}
        return self.env['report'].get_action(self, 'detail_retour_tv.xlsx',data=datas)

    @api.multi
    def print_report(self):
        datas = []
        res = []
        ds= str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S'))
        de= str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S'))
        ds_format= str(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        de_format= str(datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
        liste_transactions = self.env['benin_petro.carte.consommation'].search([('type_vente','>=','Vente par TV'),('create_date','>=',ds),('create_date','<=',de)])
        for t in liste_transactions:
            if t.quantite != 0:
                prixProduit = int(t.montant / t.quantite)
            else:
                prixProduit = 0
            for tv in t.ticket_ids:
                if prixProduit != 0 :
                    qte = float(format((float(tv.tv_type.montant) / float(prixProduit)),'.3f'))
                else:
                    qte = 0
                ligne = {
                    'ticket_type' : tv.tv_type.libelle,
                    'numTicket' : tv.num_serie,
                    'client':tv.client.codeClient,
                    'codeClient':tv.client.name,
                    'produit' : t.product_ids.name,
                    'quantite' : qte,
                    'prixProduit' : prixProduit,
                    'montant' : tv.tv_type.montant,
                    'station' : t.point_vente_id.libelle,
                    'stationName' : t.point_vente_id.name,
                    'numIncremen' : tv.num_serie_incr,
                    'dateDebut' : ds_format,
                    'dateFin' : de_format,
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
        return self.env['report'].get_action(self, 'benin_petro.detail_retour_tv_report', data=datas)


class detail_retour_tv_report(models.AbstractModel):
    _name = 'report.benin_petro.detail_retour_tv_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.detail_retour_tv_report')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }

        return report_obj.render('benin_petro.detail_retour_tv_report', docargs)
