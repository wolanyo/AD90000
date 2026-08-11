# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_point_jour(models.TransientModel):
    _name = 'benin_petro.wizard.point_jour'


    date = fields.Date(
         string='Date',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )

    @api.multi
    def print_report(self):

        ds=datetime.strptime(self.date, '%Y-%m-%d').strftime('%d/%m/%Y')

        liste_agents_monetique = self.env['benin_petro.sous_chargeur'].search([],order="create_date asc")
        res = {}
        for agent_monetique in liste_agents_monetique:
            historiques = self.env['benin_petro.historique'].search([('sous_chargeur','=',agent_monetique.id)],order="create_date asc")
            total_tv =0
            total_carte =0
            for his in historiques:
                print his.sous_chargeur
                if datetime.strptime(his.create_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y') == datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%Y'):
                    print his.sous_chargeur
                    if not his.chargeur:
                        if his.type_op == 'T.V':
                            total_tv += his.diff
                        if his.type_op == 'Recharge SUBLIME CARTE':
                            total_carte += his.diff 
            res[agent_monetique.access.name]={'name':agent_monetique.access.name,'vente_tv':locale.format("%d", float(total_tv), grouping=True),'vente_sbc':locale.format("%d", float(total_carte), grouping=True),'total':locale.format("%d", float(float(total_tv)+float(total_carte)), grouping=True)}
        sum_total_vente = 0
        sum_total_sbc = 0
        sum_total = 0
        for key,val in res.items():
            sum_total_vente += float(val["vente_tv"].replace(" ", ""))
            sum_total_sbc += float(val["vente_sbc"].replace(" ", ""))
            sum_total += float(val["total"].replace(" ", ""))
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")

        total = {"sum_total_vente":locale.format("%d", float(sum_total_vente), grouping=True),"sum_total_sbc":locale.format("%d", float(sum_total_sbc), grouping=True),"sum_total":locale.format("%d", float(sum_total), grouping=True)}
        datas = {
                'form':
                {
                    'date':ds,
                    'print_date':d1,
                    'transactions':res,
                    'total':total,
                }
        }
        #print datas
        return self.env['report'].get_action(self, 'benin_petro.point_jour_report', data=datas)


class point_jour_report(models.AbstractModel):
    _name = 'report.benin_petro.point_jour_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.point_jour_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.point_jour_report', docargs)