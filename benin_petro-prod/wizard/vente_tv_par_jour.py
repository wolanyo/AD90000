# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_vente_tv_par_jour(models.TransientModel):
    _name = 'benin_petro.wizard.vente_tv_par_jour'

    point_vente_id=fields.Many2one('benin_petro.point.vente', string='Point de  Vente')
    date = fields.Date(
         string='Date',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )

    @api.multi
    def print_report(self):
        liste_client = self.env['res.partner'].search([('create_uid','!=',1)],order="name asc")
        res = {}
        i=0
        if not self.point_vente_id:
            liste_transaction = self.env['benin_petro.carte.consommation'].search([('type_vente','=','Vente par TV'),('create_date', '>=', self.date), ('create_date', '<=', self.date)])
        else:
            liste_transaction = self.env['benin_petro.carte.consommation'].search([('point_vente_id','=',self.point_vente_id.id),('type_vente','=','Vente par TV'),('create_date', '>=', self.date), ('create_date', '<=', self.date)])
        print(liste_transaction)
        for client in liste_client:
            sum_vente=0
            for transaction in liste_transaction:
                # if datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y') == datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%Y'):
                # print(transaction.create_date)
                for to in transaction.ticket_ids:
                    if to.client.id == client.id:
                        if client.name not in res:
                            res[client.name] = {'name':client.name,'sum_total_vente':float(to.tv_type.montant)}
                        else:
                            res[client.name]['sum_total_vente'] = float(float(res[client.name]['sum_total_vente'])+float(to.tv_type.montant))
                        #sum_vente = sum_vente+transaction.montant

            
        
        print res

        
        # for agent_monetique in liste_agents_monetique:
        #     historiques = self.env['benin_petro.historique'].search([('sous_chargeur','=',agent_monetique.id)],order="create_date asc")
        #     total_tv =0
        #     total_carte =0
        #     for his in historiques:
        #         print his.sous_chargeur
        #         if datetime.strptime(his.create_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y') == datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%Y'):
        #             print his.sous_chargeur
        #             if not his.chargeur:
        #                 if his.type_op == 'T.V':
        #                     total_tv += his.diff
        #                 if his.type_op == 'Recharge SUBLIME CARTE':
        #                     total_carte += his.diff 
        #     res[agent_monetique.access.name]={'name':agent_monetique.access.name,'vente_tv':locale.format("%d", float(total_tv), grouping=True),'vente_sbc':locale.format("%d", float(total_carte), grouping=True),'total':locale.format("%d", float(float(total_tv)+float(total_carte)), grouping=True)}
        sum_total_vente = 0
        # sum_total_sbc = 0
        # sum_total = 0
        for key,val in res.items():
            sum_total_vente += float(val['sum_total_vente'])

        total = {"sum_total_vente": float(sum_total_vente)}
        if self.point_vente_id:
            point_vente = self.point_vente_id.name
        else:
            point_vente = "Tous"
        today = datetime.now()
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        datas = {
                'form':
                {
                    'date':self.date,
                    'print_date':d1,
                    'point_vente':point_vente,
                    'transactions':res,
                    'total':total,
                }
        }
        print datas
        
        return self.env['report'].get_action(self, 'benin_petro.vente_tv_par_jour_report', data=datas)


class vente_tv_par_jour_report(models.AbstractModel):
    _name = 'report.benin_petro.vente_tv_par_jour_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.vente_tv_par_jour_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.vente_tv_par_jour_report', docargs)