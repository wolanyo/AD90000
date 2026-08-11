# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import locale

class benin_petro_etat_gouverneur(models.TransientModel):
    _name = 'benin_petro.wizard.etat_gouverneur'


    start_date = fields.Date(
         string='Date Début',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )
    end_date = fields.Date(
         string='Date Fin',
         required=True,
         default=lambda *a: (parser.parse(datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
         )

    @api.multi
    def print_report(self):
        res = {}
        total = {}
        ds=datetime.strptime(self.start_date, '%Y-%m-%d').date()
        de=datetime.strptime(self.end_date, '%Y-%m-%d').date()
        liste_tresorier = self.env['benin_petro.chargeur'].search([],order="create_date asc")
        for tresorier in liste_tresorier:
            historiques = self.env['benin_petro.historique'].search([('chargeur','=',tresorier.id)],order="create_date asc")
            
            data = {}
            total_recus_carte = 0
            total_recus_tv = 0
            total_transferer_carte = 0
            total_transferer_tv = 0
            montant_init_carte = 'False'
            montant_init_tv = 'False'
            for his in historiques:

                if datetime.strptime(his.create_date, '%Y-%m-%d %H:%M:%S').date()>= ds and datetime.strptime(his.create_date, '%Y-%m-%d %H:%M:%S').date()<= de:
                #if True: 
                    print '8888888888888888888888888888888888'
                    print his.type_op
                    print his.montant_init
                    if his.type_op == 'Approvisionnement SUBLIME CARTE':
                        if montant_init_carte == 'False':
                            montant_init_carte = his.montant_init
                        if his.chargeur.id and not his.sous_chargeur:
                            total_recus_carte += his.diff
                        else:
                            total_transferer_carte += his.diff
                    
                    if his.type_op == 'Approvisionnement TV':
                        if montant_init_tv == 'False':
                            montant_init_tv = his.montant_init
                        if his.chargeur.id and not his.sous_chargeur:
                            total_recus_tv += his.diff 
                        else:
                            total_transferer_tv += his.diff 
                    if his.type_op == 'Diminuer':
                        if his.chargeur.id and not his.sous_chargeur:
                             total_recus_carte -= his.diff
                    if his.type_op == 'Rappel de fonds SUBLIME CARTE':
                        if his.sous_chargeur.id and his.chargeur.id:
                            total_transferer_carte -= his.diff
            if  montant_init_tv == 'False':
                montant_init_tv = 0
            if montant_init_carte  == 'False':
                montant_init_carte =0
             
            
            solde_final_sbc = float(montant_init_carte) + float(total_recus_carte) - float(total_transferer_carte)
            solde_final_tv = float(montant_init_tv) + float(total_recus_tv) - float(total_transferer_tv)

            sum_tv_sbc = solde_final_sbc+solde_final_tv


            data["1"] = {"solde_initial":locale.format("%d", float(float(montant_init_carte)+float(montant_init_tv)), grouping=True),"montant_recu":locale.format("%d", float(float(total_recus_carte)+float(total_recus_tv)), grouping=True),"montant_transferer":locale.format("%d", float(float(total_transferer_carte)+float(total_transferer_tv)), grouping=True),"sold_final":locale.format("%d", float(sum_tv_sbc), grouping=True)}
            data["Approvisionnement SUBLIME CARTE"] = {"solde_initial":locale.format("%d", float(montant_init_carte), grouping=True),"montant_recu":locale.format("%d", float(total_recus_carte), grouping=True),"montant_transferer":locale.format("%d", float(total_transferer_carte), grouping=True),"sold_final":locale.format("%d", float(solde_final_sbc), grouping=True)}
            data["Approvisionnement TV"] = {"solde_initial":locale.format("%d", float(montant_init_tv), grouping=True),"montant_recu":locale.format("%d", float(total_recus_tv), grouping=True),"montant_transferer":locale.format("%d", float(total_transferer_tv), grouping=True),"sold_final":locale.format("%d", float(solde_final_tv), grouping=True)}
            res[tresorier.access.name] = data
        print res
                
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        datas = {
                'form':
                {
                    'date_debut':datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'date_fin':datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'print_date':d1,
                    'transactions':res,
                    'total':total,
                }
        }
        #print datas
        return self.env['report'].get_action(self, 'benin_petro.etat_gouverneur_report', data=datas)


class etat_gouverneur_report(models.AbstractModel):
    _name = 'report.benin_petro.etat_gouverneur_report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('benin_petro.etat_gouverneur_report')
        
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            }
       
        return report_obj.render('benin_petro.etat_gouverneur_report', docargs)
