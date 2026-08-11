# # -*- coding: utf-8 -*-
# from odoo import fields, api, models,_
# from dateutil import parser
# from dateutil.relativedelta import relativedelta
# from datetime import datetime, timedelta
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
# from datetime import datetime
# import time
# import locale

# class benin_petro_bon_commande_monaie(models.TransientModel):
#     _name = 'benin_petro.wizard.bon_commande_monaie'


#     # @api.multi
#     # def print_report(self):
        
#     #     print 'dddddddddddddddddddddddddddddddddd'
#     #     datas = {
#     #             'form':
#     #             {
                    
#     #                 }
#     #         }
#     #     print len(data_len)
#     #     return self.env['report'].get_action(self, 'benin_petro.bon_commande_monaie_report', data=datas)

# class bon_commande_monaie_report(models.AbstractModel):
#     _name = 'report.benin_petro.bon_commande_monaie_report'

#     @api.model
#     def render_html(self, docids, data=None):
#         report_obj = self.env['report']
#         report = report_obj._get_report_from_name('benin_petro.bon_commande_monaie_report')
        
#         docargs = {
#             'doc_ids': self._ids,
#             'doc_model': report.model,
#             'docs': self,
#             'data': data,
#             }
       
#         return report_obj.render('benin_petro.bon_commande_monaie_report', docargs)