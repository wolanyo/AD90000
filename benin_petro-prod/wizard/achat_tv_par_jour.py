# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_achat_tv_par_jour(models.TransientModel):
    _name = 'benin_petro.wizard.achat_tv_par_jour'

    date = fields.Date(
         string='Date',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )
    date_debut = fields.Datetime(
         string='Date',
         required=True,
         default=lambda *a: (parser.parse((datetime.now() + timedelta(hours=1)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
         )
    date_fin = fields.Datetime(
         string='Date',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )

    @api.multi
    def print_report(self):

        #ds=datetime.strptime(self.date, '%Y-%m-%d').strftime('%d/%m/%Y')
        ds=datetime.strptime(self.date_debut, '%Y-%m-%d %H:%M:%S')
        de=datetime.strptime(self.date_fin, '%Y-%m-%d %H:%M:%S')
        ds = ds + timedelta(hours=1,minutes=0)
        ds = ds.strftime('%Y-%m-%d %H:%M:%S')
        ds=datetime.strptime(ds, '%Y-%m-%d %H:%M:%S')
        de = de + timedelta(hours=1,minutes=0)
        de = de.strftime('%Y-%m-%d %H:%M:%S')
        de=datetime.strptime(de, '%Y-%m-%d %H:%M:%S')
        
        res = {}
        i=0

        liste_recharge = self.env['benin_petro.historique'].search([('type_op','=','Vente de tv')])
        sum_vente=0
        for recharge in liste_recharge: 
            if True:
                if datetime.strptime(recharge.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(recharge.create_date, '%Y-%m-%d %H:%M:%S')<= de:
            #if datetime.strptime(recharge.create_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y') == datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%Y'):
                    if recharge.facture_num != '':
                        if recharge.client_id.name not in res:
                            res[recharge.client_id.name] = {'name':recharge.client_id.name,'sum_total_vente':locale.format("%d", float(recharge.diff), grouping=True)}
                        else:
                            res[recharge.client_id.name]['sum_total_vente'] = locale.format("%d", float(float(res[recharge.client_id.name]['sum_total_vente'].replace(",", ""))+float(recharge.diff)),grouping=True)
        
        sum_total_vente = 0
        for key,val in res.items():
            sum_total_vente += float(val['sum_total_vente'].replace(",", ""))

        total = {"sum_total_vente":locale.format("%d", float(sum_total_vente), grouping=True)}
        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")

        datas = {
                'form':
                {
                    'date_debut':ds.strftime('%Y-%m-%d %H:%M:%S'),
                    'date_fin':de.strftime('%Y-%m-%d %H:%M:%S'),
                    'print_date':d1,
                    'transactions':res,
                    'total':total,
                }
        }
        
        
        return self.env['report'].get_action(self, 'benin_petro.achat_tv_par_jour_report', data=datas)


class achat_tv_par_jour_report(models.AbstractModel):
    _name = 'report.benin_petro.achat_tv_par_jour_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.achat_tv_par_jour_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.achat_tv_par_jour_report', docargs)