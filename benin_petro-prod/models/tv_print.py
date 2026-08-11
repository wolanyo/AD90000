# -*- coding: utf-8 -*-
from odoo import api, fields, models
from random import randint
from pprint import pprint
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from datetime import date
import time
import locale
from datetime import timedelta
import math
from num2words import num2words
from odoo.exceptions import  ValidationError

class TvPrint(models.Model):
    _name = 'benin_petro.tv_print'
    _description = 'New Description'
    _rec_name = 'client'
    _order = 'create_date desc'

    client = fields.Many2one('res.partner',string='Client')
    details = fields.One2many('benin_petro.tv_print_details','tv_print',string="Détails")
    state = fields.Selection([('brouillon','Brouillon'),('valide','Validée')],string="Statut",default="brouillon")
    print_hestory_ids = fields.One2many('benin_petro.tv_print_hestory','print_id',string='Impression')
    ref = fields.Char(string='Référence')
    total_tv = fields.Integer(string='Nombre des tickets',compute='_getTotal')
    montant = fields.Float(string='Montant',compute='_getTotal')
    product= fields.Selection(string='Produit',required=True,
    selection=[(1, 'ESSENCE'), (3, 'GASOIL'),(4,'PETROLE'),(5,'DIVERS PRODUITS BENIN PETRO')])
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',required=True,selection=[('cheque', 'Chèque'), ('especes', 'Espèces'),('versement','Versement'),('virement','Virement'),('A credit','à crédit')])
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)
    hest_id = fields.Many2one('benin_petro.historique_ben_detail',string='Détail')
    historique_id = fields.Many2one('benin_petro.historique',string='Détail')
    remise_ids = fields.One2many(comodel_name='benin_petro.tv_remise', inverse_name='tv_print', string='Remise')
    quitance_tva = fields.Selection([('OUI','OUI'),('NON','NON')],string="Quittance TVA ramené?",default="NON")
    affiche_client = fields.Selection([('OUI','OUI'),('NON','NON')],string="Afficher nom client",default="OUI")
    numero_quitance_tva = fields.Char(string='Numéro de quittance')
    remise_type = fields.Selection([('Espece','Espece'),('Ticket','Ticket')],string="Remise sous forme de",default="Ticket",required=True)
    facture_number = fields.Integer(string="Nombre de Facture")
    document = fields.Binary(string='Pièce jointe')
    numero_cheque = fields.Char(string='Numéro de chèque')
    numero_virement = fields.Char(string='Numéro de l\'ordre de virement' )
    numero_versement = fields.Char(string='Numéro du bordereau')
    plage_from = fields.Char(string=u'Plage from')
    plage_to = fields.Char(string=u'Plage to')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    ref_nav = fields.Char(string=u'Référence Nav')

    def getTvaAmount(self):
        tva_l=0
        if self.product==1:
            tva_l= self.env['account.tax'].search([('name','=','TVA - ESSENCE')])
        elif  self.product==3:
                tva_l= self.env['account.tax'].search([('name','=','TVA - GASOIL')])
        elif  self.product==4:
            tva_l= self.env['account.tax'].search([('name','=','TVA - PETROLE')])
        elif  self.product==5:
            tva_l= self.env['account.tax'].search([('name','=','TVA - DIVERS PRODUIT')])
        return 28
    def getTva(self):
        return int(self.getQty()*self.getTvaAmount())

    def getMontantHorsTax(self):
        prix_init = self.getProduct().lst_price
        return int(math.ceil(self.montant/prix_init*(prix_init-self.getTvaAmount())))
    def getMontantTtc(self):
        return self.montant

    def getProduct(self):
        return  self.env['product.product'].sudo().search([('id','=',self.product)])
    def getQty(self):
        product_price = self.getProduct().lst_price
        qty = self.montant * pow(product_price,-1)
        return qty

    def kotKot(self):
        tv_print = self.env["benin_petro.ticket_valeur"].search([('print_id','=',self.id)])
        nbr = 0
        for p in self.details:
            last_num_serie = self.env["benin_petro.ticket_valeur"].search([('tv_type','=',p.tv_type.id)],order='id desc', limit=1)
            if str(last_num_serie.num_incr) == '':
                nbr = 1
            else:
                nbr = int(nbr) + 1
                        
            if p.tv_type.id == 3:
                nbr = 101
            if p.tv_type.id == 2:
                nbr = 51
            if p.tv_type.id == 1:
                nbr = 51
                            
            p.plage_from = str(nbr).zfill(10)
            p.plage_to = str(int(nbr)+int(p.nbr_tv)-1).zfill(10)
            tv_print = self.env["benin_petro.ticket_valeur"].search([('print_id','=',self.id),('tv_type','=',p.tv_type.id)])
            for v in tv_print:
                nbr = int(nbr) + 1
                v.num_serie_incr = str(int(nbr)-1).zfill(10)
                v.num_incr = int(nbr)-1

    
    def setValide(self):
        caissier=self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)])
        count_tv = 0
        if not self.historique_id:
        
            if self.montant <= caissier.montant_plafond_tv:
    #            last_num_serie = self.env["benin_petro.ticket_valeur"].search([],order='id desc', limit=1)
    #            if last_num_serie:
    #                self.plage_from = str(last_num_serie.num_incr).zfill(10)
    #            else:
    #                self.plage_from =  str(1).zfill(10)
                for d in self.details:
                    last_num_serie = self.env["benin_petro.ticket_valeur"].search([('tv_type','=',d.tv_type.id),('imported_state','=',False)],order='id desc', limit=1)
                    numero = ''
                    print(str(last_num_serie.num_incr).zfill(10))
                    if last_num_serie:
                        print("##################")
                        print(last_num_serie.num_incr)
                        print("##################")
                        if str(last_num_serie.num_incr) == '':
                            numero = 1
                            d.plage_from = str(numero).zfill(10)
                        else:
                            numero = last_num_serie.num_incr
                            d.plage_from = str(int(numero)+1).zfill(10)
                    else:
                        d.plage_from =  str(1).zfill(10)
                    if str(last_num_serie.num_incr) == '':
                        d.plage_to =  str(int(numero) + d.nbr_tv -1).zfill(10)
                    else:
                        d.plage_to =  str(int(numero) + d.nbr_tv).zfill(10)
                        
                m_init =self.montant
                last_historique = self.env['benin_petro.historique'].search([('type_op','=','T.V')],order='create_date desc')
                dt = datetime.today()
                day = dt.day
                month = '%02d' % dt.month
                year = dt.year
                date_format = str(day)+str(month)+str(year)
                if last_historique:
                    facture_num = last_historique[0].facture_num
                    print facture_num
                    facture_num = facture_num.split("/",1)[1]
                    print facture_num
                    if facture_num:
                        facture_num = int(facture_num)+1
                        facture_num = str(date_format)+str("/")+str(int(facture_num)+1)
                else:
                    facture_num = date_format+"/1"
                num_recharge = 'zzzzzzzzzz'
                laste_recharge = self.env['benin_petro.historique'].search([('type_op','in',['Recharge compte client','Vente de tv'])],order='create_date desc')
                if laste_recharge:
                    if laste_recharge[0].num_recharge:
                        num_recharge = 'V%06d' % (int(laste_recharge[0].num_recharge.split("V")[1]) + 1)
                    else:
                        num_recharge = 'V%06d' % (1)
                else:
                    num_recharge = 'V%06d' % (1)
                print 55555555555
                print facture_num
                hist=self.env['benin_petro.historique'].create({
                        'montant_init':caissier.montant_plafond_tv,
                        'montant_fin':caissier.montant_plafond_tv-m_init,
                        'sous_chargeur':caissier.id,
                        'type_op':'Vente de tv',
                        'diff':abs(m_init),
                        'client_id':self.client.id,
                        'moyen_de_paiement':self.moyen_de_paiement,
                        'document':self.document,
                        'facture_num' : facture_num,
                        'type_af':'TV',
                        'debit':abs(m_init),
                        'credit': 0,
                        'num_recharge':num_recharge
                        })
                caissier.write({
                        'montant_plafond_tv':caissier.montant_plafond_tv-self.montant
                    })
                # self.solde_sup=caissier.montant_plafond_tv-self.montant
                print 'mooooontant'
                print hist
                self.historique_id = hist
            else :
                raise ValidationError("Le montant indiqué doit être inférieur ou égale à votre solde : " +str(caissier.montant_plafond_tv))
            print '----------------------'
            print self.client.client_type
            for a in self.details:
                i = 1
                while i <= a.nbr_tv:
                    print 'llllllll'
                    print i
                    self.env['benin_petro.ticket_valeur'].create({
                        'tv_type':a.tv_type.id,
                        'client':a.tv_print.client.id,
                        'print_id' : self.id,
                        'company_id' : self.company_id.id
                    })
                    i+=1
                a.reste = a.nbr_tv
                count_tv = count_tv + a.nbr_tv
            montant_bonus = 0
            montant_a_pa = 0
            TVA=0
            montant_a_recharge_remise=0
            montant_hor_taxes=0
            qte=0
            
            m_init =self.montant
            m_init =self.montant
            montant_bonus = 0.0
            montant_a_pa = 0
            TVA=0
            montant_a_recharge_remise=0
            montant_hor_taxes=0
            qte=0
            if self.client.client_type == "client_acc":
                if self.montant >= 100000:
                    montant_bonus = self.montant *( self.client.valuer_a_accorde*pow(100,-1))
                    montant_bonus = int(montant_bonus/1000) * 1000
            montant_a_pa = self.montant - montant_bonus
            prix_init=self.env['product.product'].search([('id','=',self.product)]).lst_price
            #qte=round(self.montant/prix_init, 2)
            #qte=50
            self.env['benin_petro.tv_remise'].sudo().create({
                'montant':montant_bonus,
                'tv_print':self.id
            })
            tva_l=0
            if self.product==1:
                tva_l= self.env['account.tax'].search([('name','=','TVA - ESSENCE')])
            elif  self.product==3:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - GASOIL')])
            elif  self.product==4:
                tva_l= self.env['account.tax'].search([('name','=','TVA - PETROLE')])
            elif  self.product==5:
                tva_l= self.env['account.tax'].search([('name','=','TVA - DIVERS PRODUIT')])
            #montant_hor_taxes=int(math.ceil(self.montant/prix_init*(prix_init-tva_l.amount)))
            #montant_hor_taxes = 5269
            prix_ht = self.env['product.product'].search([('id','=',self.product)]).lst_price-tva_l.amount
            montant_hor_taxes= "{:.4f}".format(prix_ht*qte)
            TVA="{:.4f}".format(qte*tva_l.amount)

            montant_a_recharge_remise=float(montant_hor_taxes)+float(TVA)+montant_bonus
            if self.remise_type == 'Espece':
                montant_a_recharge_remise = montant_a_recharge_remise-montant_bonus
                montant_hor_taxes = float(montant_hor_taxes) - montant_bonus
        
            detail_id =self.env['benin_petro.historique_ben_detail'].sudo().create({
                'prix_init':self.env['product.product'].search([('id','=',self.product)]).lst_price,
                'qte':qte,
                'montant_hor_taxes':montant_hor_taxes,
                'tva_init':tva_l.amount,
                'tva':TVA,
                'prix_ht':prix_ht,
                'montant_a_recharge_remise':montant_a_recharge_remise,
                'montant_bonus':montant_bonus,
                'montant_ttc':self.montant,
                'type_de_recharge':self.env['product.product'].search([('id','=',self.product)]).name
                
            })
            
            historique_id = self.env['benin_petro.historique'].search([('id','=',hist.id)])
            
            if historique_id:
                historique_id.detail_id = detail_id
            self.hest_id = detail_id.id
            
            # self.env['account.account'].search([('code','=',419),('comapny_id','=',self.company_id.id)])
            # data =[(0,0 ,{'account_id':self.journal_id.default_debit_account_id.id ,'partner_id':self.client.id,'name':'montant hor taxes','debit':self.montant}),
            # (0,0 ,{'account_id':1724,'partner_id':self.client.id,'name':'ACHAT DE TICKET VALEUR','credit':self.montant})]
                
            # print '8888888888888888888888888888888888888'
            # print data
            # av= self.env['account.move'].create({
            
            # 'journal_id':self.journal_id.id,
            # 'date':datetime.now().date(),
            # 'ref': self.client.name+'-'+str(datetime.now()),
            # 'comapny_id' : self.company_id.id,
            # 'line_ids':data
            # })
            # av.post()
            self.state = 'valide'
    #        self.plage_to =  str(int(last_num_serie.num_incr) + count_tv).zfill(10)
        return True
    def _getTotal(self):
        for pr in self:
            nb_tv = 0
            mnt = 0
            for d in pr.details:
                nb_tv += d.nbr_tv
                mnt+=d.montant
            pr.update({
                'total_tv':nb_tv,
                'montant':mnt
            })
    def getMontantWords(self):
        print self.montant
        mnt = self.remise_ids.montant + self.montant
        text = num2words(mnt, lang='fr')
        print text
        return text.upper()

    def getDate(self):
        today = datetime.now()
        # dd/mm/YY
        today = today + timedelta(hours=1,minutes=0)
        d1 = today.strftime("%d/%m/%Y %H:%M:%S")
        print d1
        return d1

    def getMontantRemis(self):
        mnt = self.remise_ids.montant
        text = num2words(mnt, lang='fr')
        print text
        return text.upper()
        
    def getMontantTv(self):
        print self.montant
        mnt = self.montant
        text = num2words(mnt, lang='fr')
        print text
        return text.upper()
    
    @api.model
    def create(self, values):
        values['ref'] = str(randint(1111,9999))+str(randint(1111,9999))+str(randint(1111,9999))
        p=super(TvPrint, self).create(values)
        p.client.is_tv = True
        fact = self.env['benin_petro.facture_number'].sudo().search([])
        if len(fact) == 0 :
            fact = self.env['benin_petro.facture_number'].sudo().create({})
        
        p.facture_number = fact.num
        fact.num = fact.num +1
        return p


class TvPrintDetails(models.Model):
    _name = 'benin_petro.tv_print_details'

    tv_type = fields.Many2one('benin_petro.tv_type',string='Type')
    nbr_tv = fields.Integer(string="Nombre de T.V")
    montant = fields.Float(string='Montant à payer',readonly=True)
    imprime = fields.Integer(string='Imprimés',default=0)
    reste = fields.Integer(string='Restants')
    tv_print = fields.Many2one('benin_petro.tv_print',string='print')
    print_nb = fields.Integer(string='nbr print')
    plage_from = fields.Char(string=u'Plage from')
    plage_to = fields.Char(string=u'Plage to')


    @api.onchange('tv_type','nbr_tv')
    def _onchange_field_name(self):
        if self.tv_type and self.nbr_tv :
            self.montant = self.tv_type.montant * self.nbr_tv
    @api.one
    def sayhi(self):
        print 'hiiiiiiiiiiiiiiiiiii'

    @api.model
    def create(self, vals):
#        last_num_serie = self.env["benin_petro.ticket_valeur"].search([('tv_type','=',vals.get('tv_type',False))],order='id desc', limit=1)
#        numero = ''
#        print(str(last_num_serie.num_incr).zfill(10))
#        if last_num_serie:
#            print("##################")
#            print(last_num_serie.num_incr)
#            print("##################")
#            if str(last_num_serie.num_incr) == '':
#                numero = 1
#                vals['plage_from'] = str(numero).zfill(10)
#            else:
#                numero = last_num_serie.num_incr
#                vals['plage_from'] = str(int(numero)+1).zfill(10)
#        else:
#            self.plage_from =  str(1).zfill(10)
#        vals['plage_to'] =  str(int(numero) + vals.get('nbr_tv')).zfill(10)
#        print vals
        #2print aaaaaa
        mnt = self.env['benin_petro.tv_type'].search([('id','=',vals.get('tv_type',False))]).montant
        vals["montant"] = vals['nbr_tv'] * mnt
        if 'reste' not in vals:
            vals['reste']= vals['nbr_tv']
        tv_montant = self.env['benin_petro.tv_type'].search([('id','=',vals.get('tv_type',False))]).montant * vals.get('nbr_tv')
        vals['montant']=tv_montant
        return super(TvPrintDetails, self).create(vals)
    def print_ticket(self):
        return range(self.print_nb)
class Remise(models.Model):
    _name='benin_petro.tv_remise'

    tv_print = fields.Many2one(comodel_name='benin_petro.tv_print', string='Impression')
    montant = fields.Integer(string='Montant de la remise')
    montant_rest = fields.Integer(string="Restants")
    tv_ids = fields.One2many(comodel_name='benin_petro.ticket_valeur', inverse_name='remise', string='Tickets remise')
    montant_print = fields.Float(compute='getMontant',string="Montant des tickets")
    def getRepportData(self):
        data = {}
        for tv in self.tv_ids:
            if tv.tv_type.rec in data.keys():
                data[tv.tv_type.rec] = data[tv.tv_type.rec]+1
            else:
                data[tv.tv_type.rec] = 1
        return data

    @api.multi
    def getMontant(self):
        for r in self:
            r.sudo().update({
                'montant_print':r.montant-r.montant_rest
            })

    @api.model
    def create(self, vals):
        vals['montant_rest']=vals.get('montant',0)
        return super(Remise, self).create(vals)

    def print_tv(self):
        return self.env['report'].get_action(self,'benin_petro.repport_tv_template_remise')
    
    

class ticke_non_connue(models.Model):
    _name = 'benin_petro.ticke_non_connue'
    _order = 'create_date desc'
    date_dt =fields.Char(string='Date consommation')
    montant = fields.Integer(string='Montant')
    codebre = fields.Char(string="Code barre")
    etat = fields.Selection([('util','Utilisé'),('nonutil','Non utilisé')],default='nonutil')
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente", required=True)
    agent_id = fields.Many2one("benin_petro.agent",string="Agent")
