# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
from datetime import date, datetime, timedelta
import datetime
from collections import OrderedDict
import collections
from unidecode import unidecode
from random import randint
# from keyid import keyid
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
import pyqrcodeng
import base64

import pyqrcode
import io
import base64
# import qrcode
# import StringIO
# import base64
#from kkiapay import Kkiapay

class api(models.Model):




    @api.multi
    def getCartByQrcode(self,qrcode):
        data = []
        carte = self.env['benin_petro.carte'].search([['qrcode', '=', qrcode.get("qrcode")]])
        print carte.num_serie

        data = [("id",carte.id),("client",unidecode(carte.owner_id.name)),("serie",carte.num_serie),("qrcode",carte.qrcode),("solde",carte.solde),("state",carte.state),("consomateur",carte.libelle.name)]
        #data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
        return data

    @api.multi
    def checkCartByQrcode(self,qrcode):

        carte = self.env['benin_petro.carte'].search([['qrcode', '=', qrcode.get("qrcode")]])
        if not carte.id:
            result = 0
        else: result = 1

        return result

    @api.multi
    def checkAgentByMatricule(self,qrcode):
        agent = self.env['benin_petro.agent'].search([['matricule', '=', qrcode.get("matricule")],['password', '=', qrcode.get("password")]])
        if not agent.id:
            result = 0
        else: result = 1

        return result

    @api.multi
    def getAgentByMatricule(self,qrcode):
        data = []
        print qrcode
        agent = self.env['benin_petro.agent'].search([['matricule', '=', qrcode.get("matricule")]])
        print '555555555555555555555555'
        print agent
        if agent.fonction == 'Chauffeur':
            point_vente = agent.camion_id.id
        else:
            point_vente = agent.point_vente_id.id

        data = [("id",agent.id),("matricule",unidecode(agent.matricule)),("name",unidecode(agent.name)),("fonction",unidecode(agent.fonction)),("point_vente",point_vente),("point_vente_name",agent.point_vente_id.name),("PlafondDotation",agent.montant_plafond),("company",agent.company_id.id)]
        #data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
        print data
        return data


    @api.multi
    def getListeAgentBypointVente(self,qrcode):
        data = []
        print qrcode.get("point_vente_id")
        agents = self.env['benin_petro.agent'].search([['point_vente_id', '=', int(qrcode.get("point_vente_id"))],['id', '!=',qrcode.get("id")]])
        for agent in agents:
            data.append([("id",agent.id),("matricule",unidecode(agent.matricule)),("name",unidecode(agent.name)),("fonction",unidecode(agent.fonction)),("point_vente",agent.point_vente_id.id)])
        #data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
        return data


    @api.multi
    def checkCodePinByQrcode(self,param):

        carte = self.env['benin_petro.carte'].search([['qrcode', '=', param.get("qrcode")]])
        if carte.code_pin == int(param.get("code_pin")):
            result =  1
        else: result = 0
        print result
        return result

    @api.multi
    def checkCodePinByAgentId(self,param):

        agent = self.env['benin_petro.agent'].search([['id', '=', param.get("id")]])
        print agent.password
        print int(param.get("password"))
        if int(agent.password) == int(param.get("password")):
            result =  1
        else: result = 0
        print result
        return result

    @api.multi
    def getListeProduit(self):
        data = []
        produits  = self.env['product.product'].search(['company_id','=',self.env.user.company_id])

        for produit in produits:
            print produit.name
            data.append([("id",produit.id),("name",unidecode(produit.name)),("prix",produit.lst_price),("barcode",produit.barcode)])
        print data
        return data

    @api.multi
    def getProduitByBarcode(self,barcode):
        data = []
        produit = self.env['product.product'].search([['barcode', '=', barcode.get("barcode")]])
        data = [("id",produit.id),("name",unidecode(produit.name)),("prix",produit.lst_price),("barcode",produit.barcode)]

        return data

    @api.multi
    def getProduitByType(self,type_produit):
        data = []
        produits = ""
        print 66666666666
        print type_produit.get("company")
        if type_produit.get("categorie") == str("conso"):
            produits  = self.env['product.product'].search([['categories_consomable', '=', type_produit.get("type")],['sale_ok', '=', True],['company_id','=',int(type_produit.get("company"))]],order='create_date asc')

        if type_produit.get("categorie") == "service":
            produits = self.env['product.product'].search([['categories_service', '=', 'Lavage'],['sale_ok', '=', True],['company_id','=',int(type_produit.get("company"))]],order='create_date asc')

        for produit in produits:
            print produit.name
            print produit.company_id
            data.append([("id",produit.id),("name",unidecode(produit.name)),("prix",produit.lst_price),("barcode",produit.barcode)])
        print produits
        return data


    @api.multi
    def InsertTransaction(self,param):
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print param["company_id"]

        carte_id = param.get("carte_id")
        res = 0
        data = []
        solde_carte=0
        solde = 0
        prix_produit = self.env["product.product"].search([("id","=",param.get("product_ids"))]).lst_price
        type_produit = self.env["product.product"].search([("id","=",param.get("product_ids"))]).categories_consomable
        qteRemise = 0
        #param['quantite'] = param.get("montant") / prix_produit
        #param['quantite'] = float(float(param['quantite']) - float(0.01))
        montant_total = param.get("montant")
        if param.get("type_vente") == "Vente par EASY CARD" or param.get("type_vente") =="Vente par carte tampo":
            param["type_vente"]="Vente par SUBLIME CARTE"
            carte = self.env['benin_petro.carte'].search([['id', '=', param.get("carte_id")]])
            # qteSansRemise = float(float(montant_total) / float(prix_produit))
            # qteSansRemise = format(qteSansRemise, '.2f')
            # prix_produit = self.getPrixProduitParClient(carte.id,param.get("product_ids"))
            if type_produit == "Produits blancs":
                qte = float(float(montant_total) / float(prix_produit))
                qte =  format(qte, '.2f')
                param["quantite"] = qte
            #     qteRemise = float(float(qte) - float(qteSansRemise))
            #     qteRemise = format(qteRemise, '.2f')
            else:
                param["quantite"] = 0
            # param["quantite_remise"] = qteRemise
            # montant_total = param["montant"]
            carte = self.env['benin_petro.carte'].search([['id', '=', carte.id]])
            param["ticket_id"] = ''
            param["reste_carte"] = float(float(carte.solde) - float(montant_total))
            param["montant_avant"] = float(carte.solde)
            res = self.env['benin_petro.carte.consommation'].create(param)
            val_kilometrage = {
                "carte_id" : carte.id,
                "client" : carte.owner_id.id,
                "point_vente" : param.get("point_vente_id"),
                "produit" : param.get("product_ids"),
                "type_operation" : "Servi",
                "kilometrage" : param.get("kilometrage"),
                "quantite" : param.get("quantite"),
                "company_id" : param.get("company_id"),
            }

            self.env['benin_petro.kilometrage'].create(val_kilometrage)
            if res:
                point_vente = self.env['benin_petro.point.vente'].search([['id', '=', param.get("point_vente_id")]])
                point_vente.total_vente_easy_card += float(param["montant"])
                carte = self.env['benin_petro.carte'].search([['id', '=', carte.id]])
                carte.libelle.bonus += float(float(float(montant_total) * float(carte.libelle.taux))/100)
                for benefice in carte.owner_id.beneficiaires_ids:
                    benefice.bonus += float(float(float(montant_total) * float(benefice.taux))/100)

                solde_carte = float(float(carte.solde) - float(montant_total))
                carte.solde = solde_carte
                client = self.env['res.partner'].search([['id', '=', carte.owner_id.id]])
                for carte in client.carte_ids:
                    solde += carte.solde
                    client.solde_carte = solde
                point_vente = self.env['benin_petro.point.vente'].search([['id', '=', param.get("point_vente_id")]]).name
                produit = self.env['product.product'].search([['id', '=', param.get("product_ids")]]).name
                carte = self.env['benin_petro.carte'].search([['id', '=', carte.id]])
                self.env['benin_petro.historique'].create({
                    'carte_sublim':carte_id,
                    'type_op':'ACHAT '+produit,
                    'type_af':'sublime carte',
                    'diff':montant_total,
                    'debit':montant_total,
                    'credit':0,
                    'company_id':param["company_id"],
                    'solde_carte':solde_carte
                })
                body = """Merci pour votre passage chez BENIN PETRO.
            Details transaction :
            Point de vente : """+point_vente+"""
            Produit : """+produit+"""
            Montant : """+str(montant_total)+""" FCFA
            Cartte : """+str(carte.libelle.name)+"""
            Solde carte :"""+str(carte.solde)+""" FCFA"""
                #Montant : ZZZZZZZZ  ,         Date et heure : XXXXXXXXXXXXXXXX
                #Nouveau solde de la carte : """+str(carte.solde)
                Subject = "BENIN PETRO"
                mobile = client.mobile
                mailsto = client.email
            # try:
            #     if mailsto:
            #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
            # except ApiException as e:
            #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)
        else:

            if param.get("type_vente") != "":
                if type_produit == "Produits blancs":
                    qte = float(float(montant_total) / float(prix_produit))
                    qte =  format(qte, '.2f')
                    param["quantite"] = qte
                else:
                    param["quantite"] = 0
                print '3232323232223'

                tvs = ''
                total_ticket = 0
                if param.get('ticket_ids') :
                    tvs = [(4,int(n)) for n in param.get('ticket_ids').split(',')]

                for ticket in  param.get('ticket_ids').split(','):
                    t = self.env['benin_petro.ticket_valeur'].search([['id', '=', int(ticket)]])
                    total_ticket += t.tv_type.montant
                    client_recus = t.client

                vals = {
                    'type_vente':param["type_vente"],
                    'agent_id':param["agent_id"],
                    'quantite':param["quantite"],
                    'montant':param["montant"],
                    'point_vente_id':param["point_vente_id"],
                    'ticket_id':param["ticket_id"],
                    'ticket_ids':tvs,
                    'product_ids':param["product_ids"],
                    'immatriculation':param["immatriculation"],
                    'company_id':param["company_id"],
                }
                # print vals
                # print aaaa
                res = self.env['benin_petro.carte.consommation'].create(vals)
                if res:
                    point_vente = self.env['benin_petro.point.vente'].search([['id', '=', param.get("point_vente_id")]])
                    point_vente.total_vente_tv += float(param["montant"])


            else:
                montant_total = param.get("montant")
                carte = self.env['benin_petro.carte'].search([['id', '=', param.get("carte_id")]])
                #montant_total = float(prix_produit)*float(param.get("quantite"))
                res = self.env['benin_petro.carte.consommation'].create(param)
                if res:
                    point_vente = self.env['benin_petro.point.vente'].search([['id', '=', param.get("point_vente_id")]])
                    point_vente.total_vente_tv += float(param["montant"])
                    #carte = self.env['benin_petro.carte'].search([['id', '=', param.get("carte_id")]])
                    carte.libelle.bonus += float(float(float(montant_total) * float(carte.libelle.taux))/100)
                    for benefice in carte.owner_id.beneficiaires_ids:
                        benefice.bonus += float(float(float(montant_total) * float(benefice.taux))/100)

                    solde_carte = float(float(carte.solde) - float(montant_total))
                    carte.solde = solde_carte
                    client = self.env['res.partner'].search([['id', '=', carte.owner_id.id]])
                    for carte in client.carte_ids:
                        solde += carte.solde
                        client.solde_carte = solde
                    point_vente = self.env['benin_petro.point.vente'].search([['id', '=', param.get("point_vente_id")]]).name
                    produit = self.env['product.product'].search([['id', '=', param.get("product_ids")]]).name
                    body = """Merci pour votre passage chez BENIN PETRO.
                Details transaction :
                Point de vente : """+point_vente+"""
                Produit : """+produit+"""
                Montant : """+str(montant_total)+""" FCFA"""
                    #Montant : ZZZZZZZZ  ,         Date et heure : XXXXXXXXXXXXXXXX
                    #Nouveau solde de la carte : """+str(carte.solde)
                    mailsto = client.email
                    Subject = "BENIN PETRO"
                    mobile = client.mobile
                    mailsto = client.email
                # try:
                #     if mailsto:
                #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
                # except ApiException as e:
                #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)
            #elf.env["benin_petro.carte"].SendMail(mailsto,Subject,bodyEmail)
        print 'Qteeeeeeeeeeeeeeee remise'
        print qteRemise
        return 1

    @api.multi
    def getPrixProduitParClient(self,carte_id,product_id):
        carte = self.env['benin_petro.carte'].search([('id','=',carte_id)])
        product = self.env['product.product'].search([('id','=',product_id)])
        price_list = carte.owner_id.property_product_pricelist
        product_price = product.lst_price
        is_sp_price_list = False
        if price_list:
            for item in price_list.item_ids:
                if item.applied_on == '1_product':
                    if item.product_tmpl_id.product_variant_id.id == product.id:
                        is_sp_price_list = True
                        if item.compute_price == 'formula':
                            product_price = product.lst_price + item.price_surcharge
                        elif item.compute_price == 'percentage':
                            product_price = product.lst_price - (product.lst_price*(item.percent_price/100))
                if item.applied_on == '2_product_category':
                    if not is_sp_price_list :
                        if item.categ_id.id == product.categ_id.id:
                            if item.compute_price == 'fixed':
                                product_price = product.lst_price+item.price_surcharge
                            elif item.compute_price == 'percentage':
                                product_price = product.lst_price - (product.lst_price*(item.percent_price/100))
        else:
            product_price=product.lst_price
        print product_price
        #--------end oussama's code
        return float(product_price)


    @api.multi
    def checkQteEmplacement(self,param):
        """quantite = 0
        type_produit = self.env['product.product'].search([('id','=', int(param.get('product_id')))]).type
        if type_produit == "product":
            location_id = self.env['stock.location'].search([('point_vente_id','=', int( param.get("point_vente")) )]).id
            #location_id = self.env['benin_petro.point.vente'].search([('id','=', int( param.get("point_vente")  ))]).emplacement_id
            qtes =self.env['stock.quant'].search([('location_id','=', int( location_id  )),('product_id','=',int(param.get('product_id')))])
            for qte in qtes:
                quantite += qte.qty
        else:
            quantite = 1"""
        return 5000

    @api.multi
    def AnnulerTransaction(self,param):
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

        res = 0
        data = []
        solde_carte=0
        solde = 0
        transaction = self.env['benin_petro.carte.consommation'].search([['id', '=', int(param.get("id"))]])
        print transaction.type_vente
        if transaction.type_vente == "Vente par SUBLIME CARTE" or transaction.type_vente == "Vente par carte tampo":
            if transaction:
                transaction.state = "annuler"
                point_vente = self.env['benin_petro.point.vente'].search([['id', '=', transaction.point_vente_id]])
                point_vente.total_vente_easy_card -= float(transaction.montant)
                carte = self.env['benin_petro.carte'].search([['id', '=', transaction.carte_id.id]])

                if transaction.carte_id:
                    solde_carte = float(float(carte.solde) + float(transaction.montant))
                    carte.solde = solde_carte
                    client = self.env['res.partner'].search([['id', '=', carte.owner_id.id]])
                    for carte in client.carte_ids:
                        solde += carte.solde
                        client.solde_carte = solde
                    body = """Bonjour,<br/>
                Transaction effectue """+str(param.get("montant"))
                    Subject = "Carte SUBLIME CARTE"
                    mailsto = client.email #self.env['res.partner'].search([["id","=",vals.get('owner_id',False)]]).email
                res = 1
        if transaction.type_vente == "Vente au comptant":
            if transaction:
                transaction.state = "annuler"
                carte = self.env['benin_petro.carte'].search([['id', '=', transaction.carte_id.id]])
                #stock_location_id = self.env['stock.location'].search([('point_vente_id','=', int(transaction.point_vente_id.id) )])
                # order_id = self.env['pos.order'].search([('transaction_id', '=', int(transaction.id))])
                # order_id.state = "draft"
                # order_id.unlink()
                #self.env['pos.order'].unlink(order_id)
                #if param.get("type_vente") != "":
                #self.alimentation_stock(stock_location_id,transaction.product_ids,transaction.quantite)
                res = 1
            #self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)

        return res

    @api.multi
    def alimentation_stock(self,location_id,product_id,qte):
        print 'stooooooooooooooooooooocj55555555555555555'
        self.env["stock.quant"].create({ 'location_id':int(location_id),'product_id':int(product_id),'qty':float(qte),'in_date':datetime.datetime.now()
                                         })


        return 1

    @api.multi
    def getListeTransaction(self,param):

        data = []
        if not param.get("user") == '0' and param.get("fonction") != "Gerant":
            transactions = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],'|',['valider_par_agent', '=', False],'&',['valider_par_agent', '=', True],['valider_par_gerant', '=', False]],order='create_date desc')
        elif not param.get("user") == '0' and param.get("fonction") == "Gerant":
            transactions = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],['valider_par_gerant', '=', False]],order='create_date desc')
        else:
            transactions = self.env['benin_petro.carte.consommation'].search([])
        for transaction in transactions:

            data.append([("id",transaction.id),("point_de_vente",transaction.point_vente_id.libelle),("agent",transaction.agent_id.id),("carte",transaction.carte_id.num_serie),("produit",transaction.product_ids.name),("montant",transaction.montant),("date_creation",datetime.datetime.strftime((datetime.datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1)),'%d-%m-%Y %H:%M:%S')),("qte",transaction.quantite),("Agent",transaction.valider_par_agent),("gerant",transaction.valider_par_gerant),("state",transaction.state),("quantite_remise",transaction.quantite_remise),("produit_id",transaction.product_ids.id)])

        return data

    @api.multi
    def getMontantTransactions(self,param):
        print 'montaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaant'
        data_montant = []
        total =0
        qte = 0
        qteGasoilRemise =0
        qteEssenceRemise =0
        qtePetroleRemise =0
        mntGasoilRemise =0
        mntEssenceRemise =0
        mntPetroleRemise =0
        datas = self.getListeTransaction(param)
        for data in datas:
            print 'ooooooooooooooooooooooooooooooooo'
            product_montant = self.env['product.product'].search([("id","=",int(data[12][1]))]).lst_price
            if data[10][1] == "valider":
                total += float(data[5][1])
                qte += float(data[11][1])
                if data[12][1] == 156:
                    print data[12][1]
                    qteGasoilRemise = qteGasoilRemise + float(data[11][1])
                    mntGasoilRemise = float(float(qteGasoilRemise)*float(product_montant))
                if data[12][1] == 155:
                    qteEssenceRemise += float(data[11][1])
                    mntEssenceRemise = float(float(qteEssenceRemise)*float(product_montant))
                if data[12][1] == 164:
                    qtePetroleRemise += float(data[11][1])
                    mntPetroleRemise = float(float(qtePetroleRemise)*float(product_montant))
        data_montant.append([("total",total),("qteGasoilRemise",qteGasoilRemise),("qteEssenceRemise",qteEssenceRemise),("qtePetroleRemise",qtePetroleRemise)])
        data_montant.append([("total",total),("qteGasoilRemise",mntGasoilRemise),("qteEssenceRemise",mntEssenceRemise),("qtePetroleRemise",mntPetroleRemise)])
        print data_montant
        print qte
        return total

    @api.multi
    def getMontantTransactionsNew(self,param):
        print 'montaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaant'
        data_montant = []
        total =0
        qte = 0
        qteGasoilRemise =0
        qteEssenceRemise =0
        qtePetroleRemise =0
        mntGasoilRemise =0
        mntEssenceRemise =0
        mntPetroleRemise =0
        datas = self.getListeTransaction(param)
        for data in datas:
            print 'ooooooooooooooooooooooooooooooooo'
            product_montant = self.env['product.product'].search([("id","=",int(data[12][1]))]).lst_price
            if data[10][1] == "valider":
                total += float(data[5][1])
                qte += float(data[11][1])
                if data[12][1] == 156:
                    print data[12][1]
                    qteGasoilRemise = qteGasoilRemise + float(data[11][1])
                    mntGasoilRemise = float(float(qteGasoilRemise)*float(product_montant))
                if data[12][1] == 155:
                    qteEssenceRemise += float(data[11][1])
                    mntEssenceRemise = float(float(qteEssenceRemise)*float(product_montant))
                if data[12][1] == 164:
                    qtePetroleRemise += float(data[11][1])
                    mntPetroleRemise = float(float(qtePetroleRemise)*float(product_montant))
        data_montant.append([("total",total),("qteGasoilRemise",qteGasoilRemise),("qteEssenceRemise",qteEssenceRemise),("qtePetroleRemise",qtePetroleRemise)])
        data_montant.append([("total",total),("qteGasoilRemise",mntGasoilRemise),("qteEssenceRemise",mntEssenceRemise),("qtePetroleRemise",mntPetroleRemise)])
        print data_montant
        print qte
        return data_montant

    @api.multi
    def getTransactionById(self,param):

        data = []
        transaction = self.env['benin_petro.carte.consommation'].search([['id', '=', param.get("id")]])
        print transaction
        if transaction.point_vente_id.name:
            point_vente = unidecode(transaction.point_vente_id.name)
        else:
            point_vente = ""
        if transaction.carte_id.libelle.name:
            client_name = unidecode(transaction.carte_id.libelle.name)
        else:
            client_name = ""#unidecode(transaction.ticket_id.client.name)
        #if transaction
        qrcode_recus = ""
        if(transaction.recus_avoir):
            qrcode_recus = transaction.recus_avoir.id
        immatriculation = ""
        if(transaction.immatriculation):
            if transaction.immatriculation != 'undefined':
                immatriculation = transaction.immatriculation

        kilometrage = ""
        if(transaction.kilometrage):
            kilometrage = transaction.kilometrage
        data.append([("id",transaction.id),("point_de_vente",unidecode(point_vente)),
        ("agent",unidecode(transaction.agent_id.name)),
        ("carte",client_name),
        ("serie",transaction.carte_id.num_serie),
        ("produit",unidecode(transaction.product_ids.name)),
        ("montant",transaction.montant),
        ("date_transaction", datetime.datetime.strftime((datetime.datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1)),'%d-%m-%Y %H:%M:%S')),
        ("qte",transaction.quantite),
        ("state",transaction.state),
        ("quantite_remise",transaction.quantite_remise),
        ("type_vente",transaction.type_vente),
        ("tva",transaction.total_tva),
        ("hor_taxe",transaction.total_hors_taxe),
        ("immatriculation", immatriculation),
        ("kilometrage", kilometrage),
        ("prix_unit",transaction.product_ids.lst_price),
        ("solde_avant",transaction.montant_avant),
        ("solde_apres",transaction.reste_carte),
        ("qrcode_recus",qrcode_recus)])
        print data
        return data

    @api.multi
    def getLavageByCat(self,type_produit):

        data = []
        produit = self.env['product.product'].search([['categories_lavage', '=', type_produit.get("type")]])

        data.append([("id",produit.id),("name",unidecode(produit.name)),("prix",produit.lst_price),("barcode",produit.barcode)])
        return data

    @api.multi
    def getPointVente(self):
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        data = []
        point_ventes  = self.env['benin_petro.point.vente'].search([])
        print point_ventes
        for point_vente in point_ventes:
            print 'hhhhhhhhhhhhhhhhhh'
        print data
        return data

    @api.multi
    def valideTransactionsByAgent(self,param):
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

        print param.get("total")
        data = []
        if param.get("typeValidation") != "Gerant":
            transactions  = transactions = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],['valider_par_agent', '=', False]],order='create_date desc')
            for transaction in transactions:
                transaction.valider_par_agent = True
        if param.get("typeValidation") == "Gerant":
            transactions  = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],['valider_par_gerant', '=', False]],order='create_date desc')
            agent = self.env['benin_petro.agent'].search([['id', '=', int(param.get("user"))]])
            vals = {u'transaction_ids': [], u'libele': u''+agent.name,u'agent_id': int(param.get("user")),u'gerant_id':  int(param.get("gerant_id")),u'pointVente_id': agent.point_vente_id.id,u'total': param.get("total")}
            shift = self.env['benin_petro.carte.shift'].create(vals)
            data = {"agent_id":int(param.get("user")),"point_vente_id":agent.point_vente_id.id}
            print data
            data_shift =  self.ventParTypeVente(data)
            for v in data_shift:
                if v[0][1] == "Vente par TV":
                    data = [(0,0 ,{'account_id':1724 ,'name':'TV','debit':v[1][1]}),
                            (0,0 ,{'account_id': 1830,'name':'Promoetur de station','credit':v[1][1]})]
                if v[0][1] == "Vente par SUBLIME CARTE":
                    data = [(0,0 ,{'account_id':1724,'name':'Caisse recette SUBLIME CARTE (Recharge)','debit':v[1][1]}),
                            (0,0 ,{'account_id': 1830,'name':'Promoetur de station','credit':v[1][1]})]
                av= self.env['account.move'].create({
                    'journal_id':6,
                    'date':datetime.datetime.now().date(),
                    'ref': '-'+str(datetime.datetime.now()),
                    'line_ids':data

                })
                av.post()

            for transaction in transactions:
                print transaction.shift_id
                transaction.valider_par_gerant = True
                transaction.shift_id = shift

        print 'hhhhhhhhhhhhhhhhhhhhhhhhhhh'
        #transactions  = transactions = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],['valider_par_agent', '=', False]],order='create_date desc')
        #print transactions
        return 1


    @api.multi
    def checkValideAgent(self,param):
        result = 0
        transaction = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param.get("user"))],['valider_par_agent', '=', False]])
        print 'oooooooooooooooooooooooooooo'
        print transaction
        if len(transaction) == 0:
            result = 0
        else: result = 1

        return result

    @api.multi
    def getListeShift(self,param):

        data = []
        shifts = self.env['benin_petro.carte.shift'].search([['pointVente_id', '=', int(param.get("pointVente_id"))]],order='create_date desc')
        for shift in shifts:
            data.append([("id",shift.id),("libele",unidecode(shift.libele)),("date",shift.create_date),("agent",unidecode(shift.agent_id.name)),("gerant",unidecode(shift.gerant_id.name)),("total",shift.total)])
        return data

    @api.multi
    def getListeTransactionByshift(self,param):

        data = []
        shift = self.env['benin_petro.carte.shift'].search([['id', '=', param.get("id")]])
        print shift.transaction_ids
        for transaction in shift.transaction_ids:
            data.append([("id",transaction.id),("point_de_vente",transaction.point_vente_id.libelle),("agent",transaction.agent_id.id),("carte",transaction.carte_id.num_serie),("produit",unidecode(transaction.product_ids.name)),("montant",transaction.montant),("date_creation",datetime.datetime.strftime((datetime.datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1)),'%d-%m-%Y %H:%M:%S')),("qte",transaction.quantite),("Agent",transaction.valider_par_agent),("gerant",transaction.valider_par_gerant),("state",transaction.state)])

        return data


    @api.multi
    def getCientByTelephone(self,param):
        data = []
        liste_cartes = []
        client = self.env['res.partner'].search([['mobile', '=', param.get("mobile")],['password', '=', param.get("password")]])
        print 'pppppppppppppppppppppppppppp'
        print client.id
        if client.id:
            for carte in client.carte_ids:
                carte = self.env['benin_petro.carte'].search([['qrcode', '=', carte.qrcode]])
                liste_cartes.append([("id",carte.id),("client",carte.owner_id.name),("serie",carte.num_serie),("qrcode",carte.qrcode),("solde",carte.solde)])
            data = [("id",client.id),("name",unidecode(client.name)),("mobile",client.mobile),("adresse",client.street),("solde_non_affecte",client.solde_compte),("solde_affecte",client.solde_carte)]
        print data
        return data

    @api.multi
    def listeCartesByClient(self,param):
        data = []
        liste_cartes = []
        client = self.env['res.partner'].search([['id', '=', param.get("id")]])
        liste_cartes.append([("id",'0_'+str(client.id)),("libelle",unidecode(client.name)),("libelle",unidecode(client.name)),("libelle",unidecode(client.name)),("libelle",unidecode(client.name)),("solde",client.solde_compte)])
        if client.id:
            for carte in client.carte_ids:
                carte = self.env['benin_petro.carte'].search([['qrcode', '=', carte.qrcode]])
                if carte.libelle.name:
                    consomateur = unidecode(carte.libelle.name)
                else:
                    consomateur = ""
                liste_cartes.append([("id",carte.id),("client",unidecode(carte.owner_id.name)),("libelle",consomateur),("serie",carte.num_serie),("qrcode",carte.qrcode),("solde",carte.solde),("state",carte.state)])
        liste_cartes.sort(key=lambda tup: tup[2])

        return liste_cartes

    @api.multi
    def checkClientByTelephone(self,param):

        client = self.env['res.partner'].search([['mobile', '=', param.get("mobile")],['password', '=', param.get("password")]])
        if not client.id:
            result = 0
        else: result = 1
        print "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
        print result
        return result

    @api.multi
    def getClientById(self,param):
        data = []
        print param.get("id")
        client = self.env['res.partner'].search([['id', '=', param.get("id")]])

        if client.id:
            if client.street:
                street = unidecode(client.street)
            else:
                street = ""
            data = [("id",client.id),("name",unidecode(client.name)),("mobile",client.mobile),("adresse",street),("solde_non_affecte",client.solde_compte),("solde_affecte",client.solde_carte)]
        print data
        return data


    @api.multi
    def getListeTransactionByCarte(self,param):
        print param.get("carte_id")
        data = []
        if not param.get("carte_id") == '0':
            transactions = self.env['benin_petro.carte.consommation'].search([('carte_id', '=', int(param.get("carte_id"))),('state', '!=', "annuler")],order='create_date desc')
        print transactions
        for transaction in transactions:
            data.append([("id",transaction.id),("point_de_vente",transaction.point_vente_id.libelle),("agent",transaction.agent_id.id),("carte",transaction.carte_id.num_serie),("produit",unidecode(transaction.product_ids.name)),("montant",transaction.montant),("date_creation",datetime.datetime.strftime((datetime.datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1)),'%d-%m-%Y %H:%M:%S')),("qte",transaction.quantite)])
        return data


    @api.multi
    def getListeTransactionByClient(self,param):
        liste = []
        data = []
        client = self.env['res.partner'].search([['id', '=', param.get("id")]])
        print 'hhhhhhhhhhhhhhhhhhhhhhhhhhh'
        print client.carte_ids
        for carte in client.carte_ids:
            liste.append(carte.id)
        transactions = self.env['benin_petro.carte.consommation'].search([['carte_id','in',liste],['state', '!=', "annuler"]],order='create_date desc',limit=100)
        for transaction in transactions:
            data.append([("id",transaction.id),("point_de_vente",transaction.point_vente_id.libelle),("agent",transaction.agent_id.id),("carte",transaction.carte_id.num_serie),("produit",unidecode(transaction.product_ids.name)),("montant",transaction.montant),("date_creation",datetime.datetime.strftime((datetime.datetime.strptime(transaction.create_date, '%Y-%m-%d %H:%M:%S')+timedelta(hours=1)),'%d-%m-%Y %H:%M:%S')),("qte",transaction.quantite)])

        return data

    @api.multi
    def chargerCarte(self,param):
        liste = []
        data = []
        result = 0
        solde_carte = 0
        carteDebit = param.get("carteDebit")
        carteCredit = param.get("carteCredit")
        typeOperation = param.get("typeOperation")
        montant = param.get("montant")
        client_id = "0_"+str(param.get("client_id"))
        #try:
        if carteDebit == client_id:
            typeOperation = "compteTocarte"
        elif carteCredit == client_id :
            typeOperation = "carteTocompte"
        else:
            typeOperation = "carteTocarte"

        print "chargeeeeeeeeeeeeeeeeeeeeeeeeeee"
        print typeOperation
        if typeOperation == "compteTocarte":
            solde = 0
            carteDebit = carteDebit.split("_")[1]
            client = self.env['res.partner'].search([['id', '=', carteDebit]])
            carte = self.env['benin_petro.carte'].search([['id', '=', carteCredit]])
            if float(client.solde_compte) > 0:
                solde_carte = float(carte.solde) + float(montant)
                carte.solde = float(carte.solde) + float(montant)
                client.solde_compte = float(client.solde_compte) - float(montant)
                client.solde_compte_hide = client.solde_compte
                print 'ttttttttttttttttttttttttttt'
                vals = {
                    "client_id" : param.get("client_id"),
                    "libelle" : client.name+" ==> "+carte.libelle.name,
                    "montant" : montant
                }
                self.env['benin_petro.historique.dispatch'].create(vals)
                self.env['benin_petro.historique'].create({
                    'carte_sublim':carte.id,
                    'type_op':'RECHARGE',
                    'type_af':'sublime carte',
                    'diff':montant,
                    'debit':0,
                    'credit':montant,
                    'solde_carte':solde_carte
                })
                self.env['benin_petro.historique'].create({
                    'client_id':client.id,
                    'type_op':'APPROVISIONNEMENT CARTE',
                    'type_af':'sublime carte',
                    'diff':montant,
                    'debit':montant,
                    'credit':0,
                    'solde_carte':client.solde_compte_hide
                })
                for carte in client.carte_ids:
                    solde += carte.solde
                    client.solde_carte = solde
                result = 1
            else:
                result = 0
        if typeOperation == "carteTocompte":
            solde = 0
            carteCredit = carteCredit.split("_")[1]
            client = self.env['res.partner'].search([['id', '=', carteCredit]])
            carte = self.env['benin_petro.carte'].search([['id', '=', carteDebit]])
            client.solde_compte = float(client.solde_compte)  + float(montant)
            client.solde_compte_hide = client.solde_compte
            solde_carte = float(carte.solde) - float(montant)
            carte.solde = float(carte.solde) - float(montant)
            result = 1
            vals = {
                "client_id" : param.get("client_id"),
                "libelle" : carte.libelle.name+" ==> "+client.name,
                "montant" : montant
            }
            self.env['benin_petro.historique.dispatch'].create(vals)
            self.env['benin_petro.historique'].create({
                'carte_sublim':carte.id,
                'type_op':'RAPPEL DE FONDS',
                'type_af':'sublime carte',
                'diff':montant,
                'debit':montant,
                'credit':0,
                'solde_carte':solde_carte
            })
            self.env['benin_petro.historique'].create({
                'client_id':client.id,
                'type_op':'RAPPEL DE FONDS',
                'type_af':'sublime carte',
                'diff':montant,
                'debit':0,
                'credit':montant,
                'solde_carte':client.solde_compte_hide
            })
            for carte in client.carte_ids:
                solde += carte.solde
                client.solde_carte = solde
        if typeOperation == "carteTocarte":
            solde = 0
            carte_debit = self.env['benin_petro.carte'].search([['id', '=', carteDebit]])
            carte_credit = self.env['benin_petro.carte'].search([['id', '=', carteCredit]])
            print "caaaaaaaaaaaaarte"
            print carte_debit
            print carteDebit
            carte_credit.solde = float(carte_credit.solde)  + float(montant)
            carte_debit.solde = float(carte_debit.solde) - float(montant)
            result = 1
            client = self.env['res.partner'].search([['id', '=', carte_credit.owner_id.id]])
            vals = {
                "client_id" : param.get("client_id"),
                "libelle" : carte_debit.libelle.name+" ==> "+carte_credit.libelle.name,
                "montant" : montant
            }
            self.env['benin_petro.historique.dispatch'].create(vals)
            for carte in client.carte_ids:
                solde += carte.solde
                client.solde_carte = solde


        #except Exception as inst:
        #    print inst
        #    result = 0

        print result
        return result

    @api.multi
    def getListeHistoriqueByClient(self,param):
        liste = []
        data = []
        print param.get("id")
        historiques = self.env['benin_petro.historique.dispatch'].search([["client_id", '=',int(param.get("id"))]],order='create_date desc')
        for historique in historiques:
            data.append([("id",historique.id),("client",historique.client_id.id),("libelle",historique.libelle),("montant",historique.montant),("date",historique.create_date)])

        return data

    @api.multi
    def changeCodePinCarte(self,param):
        liste = []
        result =""
        carte = self.env['benin_petro.carte'].search([["id", '=',int(param.get("carte_id"))]])
        if carte:
            # codepin = randint(1111, 9999)
            carte.code_pin = param.get("codepin")
            body = """Merci de noter le code PIN de la carte : """+ str(param.get("codepin"))
            Subject = "BENIN PETRO"
            mobile = carte.libelle.mobile
            mailsto = carte.libelle.email
            # try:
            #     if mailsto:
            #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
            # except ApiException as e:
            #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)
            result = 1
        else:
            result = 0
        return result

    @api.multi
    def changePasswordClient(self,param):
        print 'chaaaaaaange'
        print param.get("type")
        result = ""
        client = self.env['res.partner'].search([["mobile", '=',param.get("mobile")]])
        if client:
            if param.get("type") == "codevalidate":
                validation_code = randint(1111, 9999)
                client.reset_password = validation_code
                client = self.env['res.partner'].search([["mobile", '=',param.get("mobile")]])
                print client.reset_password
                body = """Le code de validation est : """+str(validation_code)
                result = client.reset_password
                Subject = "BENIN PETRO"
                mobile = client.mobile
                mailsto = carte.libelle.email
            # try:
            #     if mailsto:
            #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
            # except ApiException as e:
            #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)

            if param.get("type") == "changepassword":
                new_password = randint(1111, 9999)
                client.password = new_password
                client = self.env['res.partner'].search([["mobile", '=',param.get("mobile")]])
                body = """Votre nouveau mot de passe est : """+str(new_password)
                Subject = "BENIN PETRO"
                mobile = client.mobile
                mailsto = carte.libelle.email
                # try:
                #     if mailsto:
                #         self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
                # except ApiException as e:
                #     print ("Exception when calling SmsApi->send_sms: %s\n" % e)
                result = 1
        else:
            result = -1



        return result


    def SendMail(self,mailsto,Subject,body):
        import smtplib
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        mail_server = self.env['ir.mail_server'].search([["name","=","localhost"]])

        #self.pool.get('ir.mail_server').browse(cr,uid,self.pool.get('ir.mail_server').search(cr, uid, [('name','=','Contencia-SOFT')])[0])
        msg = MIMEMultipart()
        msg.set_charset("utf-8")
        msg['From']    = mail_server.smtp_user
        msg['To']      = mailsto
        msg['Subject'] = Subject
        body = body
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP(mail_server.smtp_host, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mail_server.smtp_user,mail_server.smtp_pass)
        text = msg.as_string()
        server.sendmail(mail_server.smtp_host, mailsto.split(','), text)
        return True



    ########################################################################



    @api.multi
    def getTransfereParEmplacement(self,param):

        state = ""
        source_name = ""
        destination_name = ""
        data = []
        if param.get('fonction') == 'Chauffeur':
            emplacement_id = self.env['stock.location'].search([('camion_id','=', int( param.get("id")) )]).id
        else:
            emplacement_id = self.env['stock.location'].search([('point_vente_id','=', int( param.get("id")) )]).id

        #emplacement_id = self.env['benin_petro.point.vente'].search([('id','=', int( param.get("id")))]).emplacement_id
        if param.get("state") == "done":
            state = "done"
        else:
            state = "assigned"
        if param.get("state") == "done":
            emps = self.env['stock.picking'].search(['|',('location_id','=', int(emplacement_id)),('location_dest_id','=', int(emplacement_id)),'|',('state','=',param.get("state")),('state','=',state)],order='create_date desc')
        else:
            emps = self.env['stock.picking'].search(['|',('location_id','=', int(emplacement_id)),('location_dest_id','=', int(emplacement_id)),'|',('state','=',param.get("state")),('state','=',state)],order='create_date asc')
        for emp in emps:
            type_emplacement_dest = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).typedeEmp
            type_emplacement_source = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).typedeEmp
            if type_emplacement_source == 'camion':
                source_name = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).camion_id.name
            if type_emplacement_dest == 'camion':
                destination_name = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).camion_id.name
            if type_emplacement_source == 'depot':
                source_name = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).name
            destination_name = emp.location_dest_id.name
            #print emps.client_id
            if destination_name == "Customers":
                destination_name = "Client"
            date_transfert =  str(datetime.datetime.strptime(emp.min_date, '%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y'))
            data.append([('transfere_id',emp.id),('source_name',unidecode(emp.location_id.name)),('source_id',emp.location_id.id),('destination_name',destination_name),("destination_id",emp.location_dest_id.id), ('Date_prevue',date_transfert), ('Delivery_Type',emp.move_type),('state',emp.state)])
        #print data
        return data

    @api.multi
    def getTransfereById(self,param):
        data = []
        emps = self.env['stock.picking'].search([('id','=', int( param.get("id")  ) )])
        source_name = ""
        source_id = ""
        name_destination = ""
        destination_id = ""
        for emp in emps:
            name_destination = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).name
            type_emplacement_dest = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).typedeEmp
            type_emplacement_source = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).typedeEmp
            print name_destination
            if type_emplacement_dest == 'depot':
                print 'des_depot'
                destination_id = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).id
                name_destination = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).name
            if type_emplacement_dest == 'camion':
                print 'des_camion'
                destination_id = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).camion_id.id
                name_destination = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).camion_id.name
            if type_emplacement_dest == 'point':
                print 'des_point'
                destination_id = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).point_vente_id.id
                name_destination = self.env['stock.location'].search([('id','=', int( emp.location_dest_id.id  ) )]).point_vente_id.name
            if type_emplacement_source == 'camion':
                print 'source_camion'
                source_id = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).camion_id.id
                source_name = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).camion_id.name
            #+' / '+self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).camion_id.license_plate
            if type_emplacement_source == 'depot':
                print 'source_depot'
                source_id = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).id
                source_name = self.env['stock.location'].search([('id','=', int( emp.location_id.id  ) )]).name
            if emps.partner_id:
                name_destination = emps.partner_id.name
            if emp.image1:
                image1 = emp.image1
            else:
                image1 = ""
            if emp.image2:
                image2 = emp.image2
            else:
                image2 = ""
            if emp.chauffeur_nom != "undefined":
                chauffeur_nom = emp.chauffeur_nom
            else:
                chauffeur_nom = ""
            if emp.recepteur_nom != "undefined":
                recepteur_nom = emp.recepteur_nom
            else:
                recepteur_nom = ""
            if name_destination == "Customers":
                name_destination = emps.client_id.name
            print 'ooooooooooooooooooooooooooooo'
            if emps.client_id.id:
                source_id = '1aa1'
            else:
                print 'nnnnnnnnnnnnnnn'
            date_transfert =  str(datetime.datetime.strptime(emp.min_date, '%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y'))
            data.append([('transfere_id',emp.id),('source_name',unidecode(source_name)),('source_id',emp.location_id.id),('destination_name',unidecode(name_destination)),("destination_id",emp.location_dest_id.id), ('Date',date_transfert), ("image1",image1),("image2",image2),('Delivery_Type',emp.move_type),('state',emp.state),('livreur',chauffeur_nom),('receptioniaire',recepteur_nom),('source_idd',source_id),('destination_idd',destination_id),('observation',emp.observation)])

        return data

    @api.multi
    def getListeDesProduitsParTransfere(self,param):

        data = []
        emps = self.env['stock.picking'].search([('id','=', int( param.get("id")  ) )])
        for emp in emps:
            for em in emp.move_lines:
                data.append([("product_id",em.product_id.id),('name',em.product_id.name),('qte',em.product_uom_qty)])

        return data

    @api.multi
    def produitsParEmplacement(self,param):

        data = []
        p=[]
        if param.get('fonction') == 'Chauffeur':
            emplacement_id = self.env['stock.location'].search([('camion_id','=', int( param.get("id")) )]).id
        else:
            emplacement_id = self.env['stock.location'].search([('point_vente_id','=', int( param.get("id")) )]).id
        #emplacement_id = self.env['benin_petro.point.vente'].search([('id','=', int( param.get("id")))]).emplacement_id
        emps = self.env['stock.quant'].search([('location_id','=', int( emplacement_id ) )])
        for emp in emps:
            res =emp.search([('location_id','=', int( emplacement_id )),('product_id','=',emp.product_id.id)])
            if len(res)>1:
                if not emp.product_id.id in p:
                    qty=0
                    for r in res:
                        qty +=r.qty
                    data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",qty)])
                    p.append(emp.product_id.id)
            else:
                data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",emp.qty)])
        return data



    @api.multi
    def produitsParEmplacementCategorie(self,param):

        data = []
        p=[]
        #emplacement_id = self.env['stock.location'].search([('point_vente_id','=', int( param.get("id")) )]).id
        if param.get('fonction') == 'Chauffeur':
            emplacement_id = self.env['stock.location'].search([('camion_id','=', int( param.get("id")) )]).id
        else:
            emplacement_id = self.env['stock.location'].search([('point_vente_id','=', int( param.get("id")) )]).id
        #emplacement_id = self.env['benin_petro.point.vente'].search([('id','=', int( param.get("id")))]).emplacement_id
        emps = self.env['stock.quant'].search([('location_id','=', int( emplacement_id  ) ),('product_id.categories_consomable','=' ,param.get("categorie")) ])
        for emp in emps:
            res =emp.search( [('location_id','=', int( emplacement_id  )),('product_id','=',emp.product_id.id)  ] )
            print res
            if len(res)>1:
                if not emp.product_id.id in p:
                    qty=0
                    for r in res:
                        qty +=r.qty
                    data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",qty)])
                    p.append(emp.product_id.id)
            else:
                data.append([('produit_name',emp.product_id.name),('produit_id',emp.product_id.id),("produit_qty",emp.qty)])

        return data

    @api.multi
    def addSignature(self,qrcode):
        print 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        data = []
        emp = self.env['stock.picking'].search([('id','=', int( qrcode.get("id")  ) )])
        emp.image1= qrcode.get("image1")
        emp.image2= qrcode.get("image2")
        emp.chauffeur_nom = qrcode.get("chauffeur")
        emp.recepteur_nom = qrcode.get("recepteur")
        emp.observation = qrcode.get("observation")
        #data.append([('transfere_id',emp.id),('source_name',emp.location_id.name),('source_id',emp.location_id.id),('destination_name',emp.location_dest_id.name),("destination_id",emp.location_dest_id.id), ('Date',emp.min_date), ("image1",image1),("image2",image2),('Delivery_Type',emp.move_type)])
        #data.append([('transfere_id',emp.id),('source_name',emp.location_id.name),('source_id',emp.location_id.id),('destination_name',emp.location_dest_id.name),("destination_id",emp.location_dest_id.id), ('Date_prevue',emp.min_date), ('Delivery_Type',emp.move_type)])
        #data = {"id":carte.id,"serie":carte.num_serie,"qrcode":carte.qrcode,"solde":carte.solde}
        if(qrcode.get("type") == "valider"):
            print 'validerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
            self.TransfereValider(qrcode)
        data = self.getTransfereById(qrcode)
        return data

    @api.multi
    def TransfereValider(self,qrcode):
        data = []
        emp = self.env['stock.picking'].search([('id','=', int( qrcode.get("id") ))])
        print 'valider TESSSSSSSSSSSSSSSSSSSSSST'
        print  emp
        if emp.id and emp.state!='done':
            emp.do_transfer()
            return 1
        elif emp.id and emp.state=='done' :
            return 0
        else:
            return -1

    @api.multi
    def InsertVersement(self,qrcode):
        dataa=[]
        dataa.append((0,0 ,{'journal_id':int( qrcode.get("journal_id") ),'num_versement':qrcode.get("num_versement"),'montant':int( qrcode.get("montant") )}))
        versement=self.env['benin_petro.versement'].create({
            'point_vente_id':int( qrcode.get("point_vente_id") ),
            'versement_line':dataa,
            'montant':int( qrcode.get("montant") ),
            'type_versement': qrcode.get("type_versement"),
            'vers_par': qrcode.get("vers_par"),
            'montant_saisie':0,
        })
        tt = self.env['benin_petro.versement'].search([('id','=',versement.id)])
        tt.montant_saisie = 0
        if versement:

            transactions = self.env['benin_petro.carte.consommation'].search([('valider_par_gerant','=',True),('point_vente_id','=', int( qrcode.get("point_vente_id")  )),('verse','=',False)])
            for transaction in transactions:
                if qrcode.get("type_versement") == "Gaz et accessoire":
                    if transaction.product_ids.categories_consomable in ('Gaz','Accessoire'):
                        transaction.verse = True
                if qrcode.get("type_versement") == transaction.product_ids.categories_consomable:
                    transaction.verse = True
                if qrcode.get("type_versement") == "Lavage":
                    if transaction.product_ids.categories_service == "Lavage":
                        transaction.verse = True
        return 1

    @api.multi
    def getListeVersement(self,qrcode):
        data = []

        versements = self.env['benin_petro.versement'].search([('point_vente_id','=', int( qrcode.get("point_vente_id") ))])

        for versement  in versements:
            if versement.type_versement:
                for t in versement.versement_line:
                    journal_id = t.journal_id.id
                    num_versement = t.num_versement
                data.append([('point_vente_id',versement.point_vente_id.id)
                                ,('journal_id',journal_id),("montant",versement.montant),("type_versement",versement.type_versement),("vers_par",versement.vers_par),("num_versement",num_versement),("date_versement",versement.create_date)])
            else:
                for t in versement.versement_line:
                    journal_id = t.journal_id.id
                    num_versement = t.num_versement
                data.append([('point_vente_id',versement.point_vente_id.id)
                                ,('journal_id',journal_id),("montant",versement.montant),("type_versement",'noting'),("vers_par",versement.vers_par),("num_versement",num_versement),("date_versement",versement.create_date)])

        print data
        return data

    @api.multi
    def getListeAllJournal(self):
        data = []
        journals = self.env['account.journal'].search([("type","=","bank")],order="name asc")
        for journal in journals:
            data.append([('id',journal.id),('name',journal.name)])
        print data
        return data

    @api.multi
    def ventParProduit(self,qrcode):
        data = []
        res={}
        resname={}
        consommations = self.env['benin_petro.carte.consommation'].search([('valider_par_gerant','=',False),('point_vente_id','=', int( qrcode.get("point_vente_id")  )),('agent_id','=', int( qrcode.get("agent_id")  )),('state', '!=', "annuler")])
        for consommation in consommations:
            if  consommation.product_ids.id in res:
                res[consommation.product_ids.id]+=consommation.montant

            else :
                res[consommation.product_ids.id]=consommation.montant
                resname[consommation.product_ids.id]=consommation.product_ids.name
        for key,value in res.iteritems():
            data.append([('produit_name',resname[key]),('produit_id',key),("montant",value)])
        return data

    @api.multi
    def ventParTypeVente(self,qrcode):
        data = []
        res={}
        resname={}
        consommations = self.env['benin_petro.carte.consommation'].search([('valider_par_gerant','=',False),('point_vente_id','=', int( qrcode.get("point_vente_id")  )),('agent_id','=', int( qrcode.get("agent_id")  )),('state', '!=', "annuler")])
        for consommation in consommations:
            if  consommation.type_vente in res:
                res[consommation.type_vente]+=consommation.montant

            else :
                res[consommation.type_vente]=consommation.montant

        for key,value in res.iteritems():
            data.append([('type_vente',key),("montant",value)])
        return data


    @api.multi
    def ventParCategories(self,qrcode):
        data = []
        res={}
        res['Gaz et accessoire']=0.0
        res['Lavage']=0.0
        res['Auter services']=0.0
        resname={}
        print ' pay cate'
        print 'hhhhhhhhhhhhhhhhhhhh'
        print qrcode.get("choix")
        if qrcode.get("agent_id"):
            consommations = self.env['benin_petro.carte.consommation'].search([('valider_par_gerant','=',False),('point_vente_id','=', int( qrcode.get("point_vente_id"))),('agent_id','=', int( qrcode.get("agent_id")  )),('state', '!=', "annuler")])
        else:
            consommations = self.env['benin_petro.carte.consommation'].search([('valider_par_gerant','=',True),('point_vente_id','=', int( qrcode.get("point_vente_id"))),('verse','=',False),('state', '!=', "annuler")])
        print consommations
        for consommation in consommations:
            print consommation.product_ids.type
            if  consommation.product_ids.type=='product':

                print consommation.product_ids.categories_consomable
                if consommation.product_ids.categories_consomable in  ('Gaz','Accessoire'):
                    res['Gaz et accessoire']+=consommation.montant
                elif  consommation.product_ids.categories_consomable in res:
                    res[consommation.product_ids.categories_consomable]+=consommation.montant

                else :
                    res[consommation.product_ids.categories_consomable]=consommation.montant
            elif consommation.product_ids.type=='service':
                if consommation.product_ids.categories_service== 'Lavage':
                    res['Lavage']+=consommation.montant
                else:
                    res['Auter services']+=consommation.montant
        #print res
        #sort=sorted(res, key=res._getitem_, reverse=True)

        sort = res
        if  qrcode.get("choix")=="All":
            for key in sort:
                data.append([('categorie',key),("montant",res[key])])
        else:
            for key in sort:
                if qrcode.get("choix")==key:
                    data.append([('categorie',key),("montant",res[key])])



        return data


    @api.multi
    def checkStateTicket(self,qrcode):
        data = []
        res={}

        if self.env['benin_petro.ticket_valeur'].search([('qrcode','=',qrcode.get("qrcode"))]).etat=='nonutil':
            return 1
        return 0

    @api.multi
    def getInfoParTicket(self,qrcode):
        data=[]
        tck=self.env['benin_petro.ticket_valeur'].search(['|',('qrcode','=',qrcode.get("qrcode")),('num_serie','=',qrcode.get("qrcode"))])
        if len(tck) > 0:
            print 'oooooooooooo'
            montant = 0
            if(tck[0].recus == 'Ticket'):
                montant = tck[0].tv_type.montant
            else:
                montant = tck[0].montant_recus
            if tck[0].client.name:
                client_name =  unidecode(tck[0].client.name)
            else:
                client_name = ""
            data.append([('id',tck[0].id),('client',client_name),('etat',tck[0].etat),("num_serie",tck[0].num_serie),('montant',montant),('qrcode',tck[0].qrcode),('recus',tck[0].recus),('point_vente',tck[0].point_vente.id)])
        else:
            print 'nnnnnnnnnnnnnnnnnn'
            tck=self.env['benin_petro.ticke_non_connue'].search([('codebre','=',qrcode.get("qrcode"))])[0]
            data.append([('id',tck.id),('client','hhihi'),('etat',tck.etat),("num_serie",'5464'),('montant',tck.montant),('qrcode',tck.codebre),('recus',tck.recus),('point_vente',tck.point_vente.id)])
        print data
        return data
    @api.multi
    def valideTicket(self,qrcode):
        print '8888888888888888888888888888888888888888888888888'
        tt = qrcode.get("qrcode").split(",")
        print tt
        for ticket in tt:
            tck=self.env['benin_petro.ticket_valeur'].search([('id','=',ticket)])
            print 'pppppppppppppppppppp'
            print tck
            if len(tck) > 0:
                if tck[0].id:
                    tck[0].etat='util'
        return 1


    @api.multi
    def existTicket(self,qrcode):
        print '666666666666666666666666666666666'
        print qrcode.get("user")
        company_id = 1
        #if qrcode.get("user"):
        #    company_id = self.env['benin_petro.agent'].search([('id','=',int(qrcode.get("user")))]).company_id.id
        print company_id
        print qrcode.get("qrcode")
        tck=self.env['benin_petro.ticket_valeur'].search(['|',('qrcode','=',qrcode.get("qrcode")),('num_serie','=',qrcode.get("qrcode"))])
        print tck
        if(len(tck) == 0):
            tt = self.env['benin_petro.ticket_valeur'].search([('num_serie','=',qrcode.get("qrcode"))])
            if(len(tt) == 0):
                if not tt.id:
                    print 'hhhhhhhhhhhhhhhaaaaaaaaaaaaalalmlk'
                    tck=self.env['benin_petro.ticke_non_connue'].search([('codebre','=',qrcode.get("qrcode"))])
                    print tck
                    if tck.id:
                        print 'ouiiiiiiiiiiiiiiii'
                        return  1
                    else:
                        print 'nonnnnnnnnnnnnnnnnn'
                        return 0
                else:
                    return  1
            return 1
        else:
            return 1

    @api.multi
    def checkValidateProduct(self,qrcode):
        carte = self.env['benin_petro.carte'].search([('qrcode','=',qrcode.get("qrcode"))])
        result_produit = 0
        result_point_vente = 0
        data = []
        if len(carte.product_ids) != 0:
            for p in carte.product_ids:
                if int(p.id) == int(qrcode.get("produit")):
                    result_produit = result_produit+1
        else:
            result_produit = 1
        if len(carte.point_vente_ids) != 0:
            for pv in carte.point_vente_ids:
                if int(pv.id) == int(qrcode.get("point_vente")):
                    result_point_vente = result_point_vente+1
        else:
            result_point_vente = 1
        data = [("result_produit",result_produit),("result_point_vente",result_point_vente)]
        print data
        return data

    @api.multi
    def getCarteByNum(self,param):
        carte = self.env['benin_petro.carte'].search([['num_serie', '=', param.get("qrcode")]])
        data = []
        if carte.id:
            data = [("id",carte.id),("serie",carte.num_serie),("qrcode",carte.qrcode),("solde",carte.solde),("state",carte.state),("consomateur",carte.libelle.name)]
        return data

    @api.multi
    def getClientByMobile(self,param):
        print param.get("mobile")
        client = self.env['res.partner'].search([['mobile', '=', param.get("mobile")]])
        print client
        data = []
        if client.id:
            data = [("id",client.id),("name",client.name),("solde",client.solde_compte),("mobile",client.mobile)]
        return data

    @api.multi
    def validateRecharge(self,param):
        client = self.env['res.partner'].search([['id', '=', param.get("client")]])
        client.solde_compte = float(client.solde_compte)  + float(param.get("montant"))
        client.solde_compte_hide = client.solde_compte

        self.env['benin_petro.historiquekkiapay'].create({
            'client_id':client.id,
            'amount':param.get("montant"),
            'source_common_name':param.get("source_common_name"),
            'country':param.get("country"),
            'transactionId':param.get("transactionId"),
            'performedAt':param.get("client")
        })
        res = self.env['benin_petro.historique'].create({
            'type_op':'Recharge compte client',
            'client_id':client.id,
            'moyen_de_paiement':"Par Kkiapay",
            'type_af':'sublime carte',
            'debit':0,
            'credit':float(param.get("montant")),
            'solde_carte':client.solde_compte_hide,
            'state':'valide'
        })
        return 1
    # print param
    # print aaaa

    @api.multi
    def getListeKkiapay(self,param):
        liste = []
        data = []
        print param.get("id")
        historiques = self.env['benin_petro.historiquekkiapay'].search([["client_id", '=',int(param.get("client_id"))]],order='create_date desc')
        for historique in historiques:
            data.append([("id",historique.id),("client",historique.client_id.name),("transactionId",historique.transactionId),("amount",historique.amount),("country",historique.country),("date_operation",historique.create_date)])

        return data

    @api.multi
    def validateCarte(self,param):
        print "######################"
        print param
        vals = {
            "company_id": param.get("company_id"),
            "name": param.get("client_name"),
            "mobile": param.get("telephone"),
            "email": param.get("email"),
            "street": param.get("adresse")
        }
        print vals
        res = self.env['res.partner'].search([['mobile', '=', param.get("telephone")]])
        if not res:
            res = self.env['res.partner'].create(vals)
        print res
        vals_costomer = {
            "name": param.get("client_name"),
            "mobile": param.get("telephone"),
            "taux": 0,
        }
        costomer = self.env['benin_petro.customer'].create(vals_costomer)
        carte = self.env['benin_petro.carte'].search([['num_serie', '=', param.get("num_serie")]])
        print carte
        carte.owner_id = res.id
        carte.state = "generee"
        carte.libelle = costomer.id
        vals_historique = {
            "carte": carte.id,
            "agent": param.get("agent_id")
        }
        self.env['benin_petro.carte.preimprime.validate'].create(vals_historique)
        return 1


    @api.multi
    def recharge(self,param):
        gerant = self.env['benin_petro.agent'].search([['id', '=', param.get("agent_id")]])
        if param.get("type") == "recharge_carte":
            carte = self.env['benin_petro.carte'].search([['num_serie', '=', param.get("num_serie")]])
            if carte.id:
                carte.solde = carte.solde  + float(param.get("solde"))
                self.env['benin_petro.historique'].create({
                    'type_op':'Recharge carte',
                    'carte_sublim':carte.id,
                    'type_af':'sublime carte',
                    'debit':0,
                    'credit':float(param.get("solde")),
                    'solde_carte':carte.solde,
                    'gerant': param.get("agent_id")
                })
                print "pppppppppppp"
                nv_montant_gerant= gerant.montant_plafond-float(param.get("solde"))
                self.env['benin_petro.historique'].create({
                    'montant_init':gerant.montant_plafond,
                    'montant_fin':nv_montant_gerant,
                    'gerant':param.get("agent_id"),
                    'type_op':'Recharge carte',
                    'type_af':'sublime carte',
                    'diff':abs(float(gerant.montant_plafond)-float(param.get("solde"))),
                    'debit':float(param.get("solde")) ,
                    'credit':0
                })

                nv_m = gerant.montant_plafond-float(param.get("solde"))
                gerant.write({
                    'montant_plafond':nv_m,
                })
        # self.env['benin_petro.historique'].create(vals)
        else:
            client = self.env['res.partner'].search([['mobile', '=', param.get("mobile")]])
            data = []
            if client.id:
                client.solde_compte = client.solde_compte + float(param.get("solde"))
                self.env['benin_petro.historique'].create({
                    'type_op':'Recharge client',
                    'client_id':client.id,
                    'type_af':'sublime carte',
                    'debit':0,
                    'credit':float(param.get("solde")),
                    'solde_carte':client.solde_compte,
                    'gerant': param.get("agent_id")
                })

                nv_montant_gerant= gerant.montant_plafond-float(param.get("solde"))
                self.env['benin_petro.historique'].create({
                    'montant_init':gerant.montant_plafond,
                    'montant_fin':nv_montant_gerant,
                    'gerant':param.get("agent_id"),
                    'type_op':'Recharge carte',
                    'type_af':'sublime carte',
                    'diff':abs(float(gerant.montant_plafond)-float(param.get("solde"))),
                    'debit':float(param.get("solde")) ,
                    'credit':0
                })
                nv_m = gerant.montant_plafond-float(param.get("solde"))
                gerant.write({
                    'montant_plafond':nv_m,
                })
        return 1


    @api.multi
    def getHistoriqueValidateByAgent(self,qrcode):
        print '##############'
        print qrcode.get("agent_id")
        historique_validation = self.env['benin_petro.carte.preimprime.validate'].search([['agent', '=', int(qrcode.get("agent_id"))]])
        print historique_validation
        data = []
        if historique_validation:
            for historique in historique_validation:
                data.append([('id',historique.id),('carte',historique.carte.num_serie),('client',historique.carte.owner_id.name),('date_validation',historique.create_date)])
        return data

    @api.multi
    def getHistoriqueRechargeByAgent(self,param):
        print '##############'
        if param.get("type_op") == "recharge_carte":
            historique_recharge = self.env['benin_petro.historique'].search([('gerant', '=', int(param.get("agent_id"))),('type_op','=','Recharge carte'),('debit','=',0)])
        else:
            historique_recharge = self.env['benin_petro.historique'].search([('gerant', '=', int(param.get("agent_id"))),('type_op','=','Recharge client')])

        print historique_recharge
        data = []
        if historique_recharge:
            for historique in historique_recharge:
                print historique.carte_sublim
                data.append([('id',historique.id),('carte',historique.carte_sublim.num_serie),('client',historique.client_id.name),('date_validation',historique.create_date),('solde',historique.credit)])
        return data


    @api.multi
    def getRecusById(self,param):
        recus = self.env['benin_petro.ticket_valeur'].search([('id', '=', int(param["id"]))])
        print recus
        data = [("id",recus.id),("num_serie",recus.num_serie),("client",recus.client.name),("montant",recus.montant_recus),("qrcode_image",recus.qrcode_img)]
        return data


    @api.multi
    def InsertRecus(self,param):
        print 'ooooooooooooooooooooooo'
        total_ticket = 0
        transaction = self.env['benin_petro.carte.consommation'].search([['agent_id', '=', int(param["agent"])]],order='create_date desc')[0]
        print '111111111'
        print  param.get('ticket_ids').split(',')
        for ticket in  param.get('ticket_ids').split(','):
            t = self.env['benin_petro.ticket_valeur'].search([['id', '=', int(ticket)]])
            if t.recus == 'Recus':
                total_ticket += t.montant_recus
            else:
                total_ticket += t.tv_type.montant
            client_recus = t.client
        vals_ticket = {
            "client": client_recus.id,
            "recus":"Recus",
            "montant_recus": float(total_ticket) - float(param["montant"]),
            "point_vente": param["point_vente"]
        }
        res = self.env['benin_petro.ticket_valeur'].create(vals_ticket)
        # qr = pyqrcodeng.create(res.qrcode, error='L', version=27, mode='binary')
        # big_code = pyqrcodeng.create('0987654321', error='L', version=27, mode='binary')
        # message_bytes = qr.text():q
        # base64_bytes = base64.b64encode(message_bytes)
        # res.qrcode_img = base64_bytes
        c = pyqrcode.create(res.qrcode)
        s = io.BytesIO()
        c.png(s,scale=6)
        encoded = base64.b64encode(s.getvalue()).decode("ascii")
        res.qrcode_img = encoded
        print 'ooooooooooooo'
        print transaction
        print transaction.id
        print 'oooooooooooo'
        transaction.recus_avoir = res
        # qr = qrcode.QRCode(
        # version=5,
        # error_correction=qrcode.constants.ERROR_CORRECT_L,
        # box_size=8,
        # border=4
        # )
        # qr.add_data(res.qrcode)
        # qr.make(fit=True)
        # img = qr.make_image()
        # img_buffer = StringIO.StringIO()
        # img.save(img_buffer, 'png')
        # res = img_buffer.getvalue()
        # img_buffer.close()
        # res.qrcode_img = base64.b64encode(res)
        data = [("qrcode",res.qrcode),("client",res.client.name),("montant",res.montant_recus),("num_serie",res.num_serie),("date",res.create_date),("qrcode_img",res.qrcode_img)]
        print res
        return data

    @api.multi
    def checkClient(self,param):

        client = self.env['res.partner'].search([['mobile', '=', param.get("mobile")]])
        print client
        data = []
        if client.id:
            data = [("id",client.id),("name",client.name),("email",client.email),("mobile",client.mobile)]

        return data
    # @api.multi
    # def getCarteByNum(self,qrcode):
    #     data = []
#     print qrcode
#     carte = self.env['benin_petro.carte'].search([['num_serie', '=', qrcode.get("qrcode")]])
#     if not carte.id:
#         result = 0
#     else:
#         result = 1
#     return result

# @api.multi
# def validateCarte(self,param):
#     print "######################"
#     print param

#     return 1



