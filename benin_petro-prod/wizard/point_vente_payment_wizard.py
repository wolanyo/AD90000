# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import time
import datetime
from pprint import pprint


class point_vente_payment_wizard(models.TransientModel):

    _name="benin_petro.point_vente_payment_wizard"
    _rec_name='id'

    def _getStationId(self):
        print '55555555555555'
        print self._context.get('active_ids',False)[0]
        return self._context.get('active_ids',False)[0]

    tv_station = fields.Many2one('benin_petro.point.vente',string='Station',default=_getStationId)
    type_payment = fields.Selection([('Espece','Espece'),('cheque','Cheque'),('Note de credit','Note de crédit')],string="Type de payment",required=True)
    montant = fields.Float(string='Montant',compute="montantt")
    montant_paye = fields.Float(string='Montant payé')
    datec=fields.Date(string='Date',default=fields.Date.today,required=True)
    type_vente=fields.Selection([('Vente par SUBLIME CARTE','Vente par SUBLIME CARTE'),('Vente par TV','Vente par TV')],string="Type de vente",required=True)
    type_commission = fields.Selection([('Avec commission','Avec commission'),('Sans commission','Sans commission')],string="Avec ou sans commission",required=True,default='Sans commission')
    montant_commission = fields.Float(string='Montant commission')
    numero_cheque = fields.Char(string='Numéro de chèque')
    produit = fields.Many2one('product.product',string='Product')
    def calc(self,dateR):
        print 'fuuuuuuuuuuuuuuuuunction'
        print self.type_vente 
        id = self._context.get('active_ids',False)[0]
        point_vente = self.env['benin_petro.point.vente'].search([['id', '=', id]])
        montant =0
        if self.type_vente == "Vente par SUBLIME CARTE":
            montant = point_vente.total_vente_easy_card
        if self.type_vente == "Vente par TV":
            montant = point_vente.total_vente_tv
        if self.produit:
            if self.produit.lst_price !=0 and self.montant_paye !=0:
                self.montant_commission = (self.montant_paye / self.produit.lst_price)*3
            else:
                self.montant_commission = 0
        # montant=0
        # id =self._context.get('active_ids',False)[0]
        # tv_station=self.env["benin_petro.carte.consommation"].search([('point_vente_id','=',id)])
        data=[]
        # montant_tv=0
        # montant_momo=0
        # montant_carte=0

        # dt=datetime.strptime(dateR, '%Y-%m-%d')
        # tm2=datetime.strptime('08:00:00', '%H:%M:%S').time()
        # datee=str(datetime.combine(dt, tm2))
        # print tv_station
        # for a in tv_station:  
        #     print a.montant  
        #     print a.state    
        #     print a.create_date
        #     print   datee  
        #     if a.state=='valider' and a.create_date< datee:
        #         if a.type_vente == 'Vente par TV':
        #             montant_tv+=a.montant
        #         if a.type_vente == 'Vente par SUBLIME CARTE':
        #             montant_carte+=a.montant
        

        # montant=montant_tv+montant_momo+montant_carte
        # data.append({
        #     'montant_total':montant,
        #     'montant_tv':montant_tv,
        #     'montant_carte':montant_carte,
        # })
        # print data
        data.append({'montant_total':montant})
        print data
        return data

    @api.depends('montant','type_vente','datec','produit','montant_paye')
    def montantt(self):
        print 'compuuuuuuuute '
        a= self.calc(self.datec)
        self.montant= a[0]['montant_total']
        return 1

    def savePayment(self):
        print "cliiiiiick"
        if self.montant_paye <= 0 :
            raise ValidationError("Le montant indiqué doit être supérieur à zero ")
        if self.montant_paye > self.montant :
            raise ValidationError("Le montant payé doit être inferieur ou égale au montant total ")
        id =self._context.get('active_ids',False)[0]
        point_vente = self.env['benin_petro.point.vente'].search([['id','=', id]])
        tv_station = self.env["benin_petro.carte.consommation"].search([('point_vente_id','=',id)])
        last_historique = self.env['benin_petro.tv_station_hestory'].search([],order='create_date desc')
        dt = datetime.datetime.today()
        day = dt.day
        month = '%02d' % dt.month
        year = dt.year
        date_format = str(day)+str(month)+str(year)
        if last_historique:
            facture_num = last_historique[0].facture_num
            if facture_num:
                print facture_num
                facture_num = facture_num.split("/",1)[1]
                print facture_num
                if facture_num:
                    facture_num = int(facture_num)+1
                    facture_num = str(date_format)+str("/")+str(int(facture_num)+1)
            else:
                facture_num = date_format+"/1"
        else:
            facture_num = date_format+"/1"
        az=self.env["benin_petro.tv_station_hestory"].create({
            'type_payment':self.type_payment,
            'montant':self.montant_paye,
            'tv_station':point_vente.id,
            'type_vente':self.type_vente,
            'montant_commission':format(float(self.montant_commission),'.2f'),
            'montant_net':format(float(self.montant_paye)-float(self.montant_commission), '.2f'),
            'facture_num':facture_num,
            #'datec':self.datec
            })
        if az:
            if self.type_commission == 'Sans commission':
                if self.type_vente == "Vente par SUBLIME CARTE":
                    point_vente.total_vente_easy_card -= self.montant_paye
                    data = [(0,0 ,{'account_id':1830 ,'name':'Promoetur de station','debit':self.montant_paye}),
                    (0,0 ,{'account_id': 1833,'name':'Bénin pétro','credit':self.montant_paye})]
                if self.type_vente == "Vente par TV":
                    point_vente.total_vente_tv -= self.montant_paye
                    data = [(0,0 ,{'account_id':1830 ,'name':'Promoetur de station','debit':self.montant_paye}),
                    (0,0 ,{'account_id': 1833,'name':'Bénin pétro','credit':self.montant_paye})]
            else:
                if self.type_vente == "Vente par SUBLIME CARTE":
                    point_vente.total_vente_easy_card -= self.montant_paye
                    data = [(0,0 ,{'account_id':1830 ,'name':'Promoetur de station','debit':self.montant_paye}),
                    (0,0 ,{'account_id': 2046,'name':'Produits accessoires','credit':self.montant_commission}),
                    (0,0 ,{'account_id': 1833,'name':'Bénin pétro','credit':float(self.montant_paye)-float(self.montant_commission)})]
                if self.type_vente == "Vente par TV":
                    point_vente.total_vente_tv -= self.montant_paye
                    data = [(0,0 ,{'account_id':1830 ,'name':'Promoetur de station','debit':self.montant_paye}),
                    (0,0 ,{'account_id': 2046,'name':'Produits accessoires','credit':self.montant_commission}),
                    (0,0 ,{'account_id': 1833,'name':'Bénin pétro','credit':float(self.montant_paye)-float(self.montant_commission)})]
            
            av= self.env['account.move'].create({
            
                'journal_id':6,
                'date':datetime.datetime.now().date(),
                'ref': '-'+str(datetime.datetime.now()),
                'line_ids':data

                })
            av.post()
        print az
        print 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'
        # self.tv_station.sudo().write({
        #     'hestory_ids':[(0,0,{'type_payment':self.type_payment,'montant':self.montant})]
        # })

        # dt=datetime.strptime(self.datec, '%Y-%m-%d')
        # tm2=datetime.strptime('08:00:00', '%H:%M:%S').time()
        # datee=str(datetime.combine(dt, tm2))


        # for a in tv_station:            
        #     if a.state=='valider' and a.create_date < datee:
        #         a.sudo().write({
        #             'state':'paye',
        #             'payement_id':az.id,
        #         })
        
        #data = [(0,0 ,{'account_id':31554 ,'partner_id':'','name':'Demande de consommation','debit': self.montant}),
        #    (0,0 ,{'account_id':19583,'partner_id':'','name':'Demande de consommation','credit':self.montant})]
        # av= self.env['account.move'].create({
        # 'journal_id':141,
        # 'date':datetime.now().date(),
        # 'ref': 'sssss-'+str(datetime.now()),
        # 'line_ids':data
        # })  
        # av.post()
        # self.tv_station.sudo().write({
        #     'hestory_ids':[(0,0,{'type_payment':self.type_payment,'montant':self.montant})]
        # })
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        

        
        
    


        
