# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_etat_tv(models.TransientModel):
    _name = 'benin_petro.wizard.etat_tv'

    client_id =fields.Many2one('res.partner', string='Client')

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

        return self.env['report'].get_action(self, 'res.partner.xlsx')

    @api.multi
    def print_report(self):
        datas = []
        ds=datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
        de=datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
        

        if self.client_id:
            liste_tv = self.env['benin_petro.ticket_valeur'].search([('client','=',self.client_id.id)],order="create_date asc")
        else:
            liste_tv = self.env['benin_petro.ticket_valeur'].search([],order="create_date asc")
        res={}
        cpt_util = 0
        cpt_non_util = 0
        for tv in liste_tv:
            # if datetime.strptime(tv.create_date, '%Y-%m-%d %H:%M:%S')>= ds and datetime.strptime(tv.create_date, '%Y-%m-%d %H:%M:%S')<= de:
            if tv.tv_type.type_name:
                if tv.tv_type.type_name not in res:
                    if tv.etat == 'util':
                        cpt_util = 1
                    else:
                        cpt_non_util = 1
                    res[tv.tv_type.type_name] = {
                        'util':cpt_util,
                        'nonutil':cpt_non_util,
                        'total' : cpt_util + cpt_non_util
                    }
                else:
                    if tv.etat == 'util':
                        res[tv.tv_type.type_name]['util'] = res[tv.tv_type.type_name]['util'] +1
                    else:
                        res[tv.tv_type.type_name]['nonutil'] = res[tv.tv_type.type_name]['nonutil'] +1
                    res[tv.tv_type.type_name]['total'] = res[tv.tv_type.type_name]['nonutil'] + res[tv.tv_type.type_name]['util']

        tota_util = 0
        total_non_util = 0
        total = 0
        print "00000000000000000"
        print res
        for key,val in res.items():
            print '#############'
            print key
            print '#############'
            tv_type = self.env['benin_petro.tv_type'].search([('type_name','=',key)])
            tota_util += val['util'] * tv_type.montant
            total_non_util += val['nonutil'] * tv_type.montant
            total += val['total'] * tv_type.montant

        
        total = {
            'util':tota_util,
            'nonutil':total_non_util,
            'total' : total
        }
        # print res
        # print aaa
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        datas = {
                'form':
                {
                    'date_debut':self.start_date,
                    'date_fin':self.end_date,
                    'print_date':d1,
                    'client': self.client_id.name,
                    'transactions':res,
                    'total':total
                    }
            }
        #print datas["form"]["transactions"]
        return self.env['report'].get_action(self, 'benin_petro.etat_tv_report', data=datas)


class etat_tv_report(models.AbstractModel):
    _name = 'report.benin_petro.etat_tv_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_tv_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.etat_tv_report', docargs)
