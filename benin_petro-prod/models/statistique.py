# -*- coding: utf-8 -*-

from odoo import fields, api, models,_
from datetime import datetime
import locale
# from swagger_client.rest import ApiException

class benin_petro_statistique(models.Model):
    _name = 'benin_petro.statistique'

    call_statistique_widget = fields.Char(string="widget")


    @api.multi
    def getMyMonth(self,months):
    	moisLibel = u'Janvier'
    	try:
    		if (months==2):
    			moisLibel = u'Février'
    		elif (months==3):
    			moisLibel = u'Mars'
    		elif (months==4):
    			moisLibel = u'Avril'
    		elif (months==5):
			moisLibel = u'Mai'
    		elif (months==6):
    			moisLibel = u'Juin'
    		elif (months==7):
    			moisLibel = u'Juillet'
    		elif (months==8):
    			moisLibel = u'Août'
    		elif (months==9):
    			moisLibel = u'Septembre'
    		elif (months==10):
    			moisLibel = u'Octobre'
    		elif (months==11):
    			moisLibel = u'Novembre'
    		elif (months==12):
    			moisLibel = u'Décembre'
    	except TypeError:
    		raise osv.except_osv(_('Alerte!'),_("Merci de Contacter L'administrateur code:M00"))
    	return moisLibel
    @api.multi
    def getAllMonth(self):
    	import math
    	self._cr.execute("select distinct EXTRACT( month from create_date) as moi from benin_petro_carte_consommation")
    	resHTML = "<option value='All' selected='true'>Tous</option>"
    	for rec in self._cr.fetchall():
    		resHTML += "<option value='"+str(int(math.floor(rec[0])))+"'>"+self.getMyMonth(int(rec[0]))+"</option>" 
    	return resHTML

    @api.multi
    def getAllYear(self):
    	import math
    	self._cr.execute("select distinct EXTRACT( year from create_date) as annee from benin_petro_carte_consommation order by EXTRACT( year from create_date) desc")
    	resHTML = "<option value='All' selected='true'>Tous</option>"
    	for rec in self._cr.fetchall():
    		resHTML += "<option value='"+str(int(math.floor(rec[0])))+"'>"+str(int(math.floor(rec[0])))+"</option>" 
    	return resHTML



    @api.multi
    def getListeRechargeClient(self,client,year,month,datedebut,datefin):
	critere = ""
	table = ""
	thead = "<tr><td>Client</td><td>Solde initial</td><td style='display:none'></td><td>Montant de la recharge</td><td style='display:none'></td><td>Solde final</td><td style='display:none'></td><td>Date du recharge</td></tr>"
	theade ="<table id='result_datatable_recharge' class='table table-striped table-bordered' cellspacing='0' width='100%'><thead>"
 	tbody ="</thead><tbody>"
	tfoot = ""
	totalMontant = 0
	if year != "All":
		critere+= " and EXTRACT( year from l.create_date) = "+str(year)
	if month != "All":
		critere+= " and EXTRACT( month from l.create_date) = "+str(month)
    	if client != "All":
    		critere+= " and l.client_id = "+str(client)
    	if (datedebut and datefin):
    		critere+= " and date(l.create_date) between '"+str(datedebut)+"' and '"+str(datefin)+"' "
	
    	query ="""select r.name,l.old_version,l.new_version,(CAST (l.new_version AS float)-CAST (l.old_version AS float)) as Recharge,l.create_date  from benin_petro_log l,res_partner r where l.client_id = r.id  and champ = 'Solde non affecte' and l.acteur_name != r.name and (CAST (l.new_version AS float) > CAST (l.old_version AS float)) """+str(critere)+""" order by  r.name"""


	print query
    	self._cr.execute(query)
	
    	for rec in self._cr.fetchall():
            print rec[3]
            if float(rec[3]) != 0:
                totalMontant+= float(rec[3])
                tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[1])+"</td><td>"+locale.format("%d", float(rec[3]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[3])+"</td><td>"+locale.format("%d", float(rec[2]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[2])+"</td><td>"+str(datetime.strptime(rec[4].split('.')[0], '%Y-%m-%d %H:%M:%S'))+"</td></tr>"
    	tbody += "</tbody><tfoot><tr style='color:red;font-weight:bold;'><td></td><td></td><td style='text-align:right'>Total : </td><td>"+locale.format("%d", totalMontant, grouping=True)+" CFA</td></tr></tfoot></table>"
	theade += thead
	table = theade + tbody
	#print table
    	return {"table":table}	



    @api.multi
    def getResult(self,point_vente,client,year,month,datedebut,datefin,parProduit,parCarte,parPoint,parClient,type_vente):
	print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
	print parProduit
	print parCarte
	print client

	print "jjjjjjjjjjjjjjjjjjjjjjjiuojujijljllij"
	#company_id = self.env["res.users"].sudo().search([('id','=',self.env.user.id)]).company_id.id
	field = ""
 	relation = ""
	critere_relation = ""
	groupbye = ""
	critere=""
	try:
		if type_vente=="All":
			critere = " and gc.state='valider'"
		if type_vente!='Vente par TV non connues' and type_vente!="All" and type_vente!="":
			critere = " and gc.state='valider'  and gc.type_vente='"+str(type_vente)+"' "
		query = ""
		table = ""
		tbody ="</thead><tbody>"
		thead = ""
		theade ="<table id='result_datatable' class='table table-striped table-bordered' cellspacing='0' width='100%'><thead>"
		tfoot = ""
		result = ""
		totalMontant = 0
		if year != "All":
			critere+= " and EXTRACT( year from gc.create_date) = "+str(year)
		if month != "All":
			critere+= " and EXTRACT( month from gc.create_date) = "+str(month)

		if (datedebut and datefin):
			critere+= " and date(gc.create_date) between '"+str(datedebut)+"' and '"+str(datefin)+"' "
		

		if(point_vente != "All" ) :
			thead = "<tr><th>Produit</th><th>Montant</th><th style='display:none;'>Montant</th><th style='display:none;'>Montant</th></tr>"
			field = "pt.name,sum(montant) as Montant"
			relation = " benin_petro_carte_consommation gc,product_template pt"
			critere_relation = "pt.id = gc.product_ids"
			groupbye = " group by gc.product_ids,pt.name"
			critere += " and gc.point_vente_id = "+str(point_vente)
			result = "Produit"

		if(point_vente != "All" and client != "All") :
			if(parProduit == True) :
				print 'ooooooooooooooooooooo'
				thead = "<tr><th>Produit</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "pt.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt,product_product pp"
				critere_relation = "pp.id = gc.product_ids and pt.id = pp.product_tmpl_id"
				groupbye = " group by gc.product_ids,pt.name"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				critere+= " and gc.point_vente_id = "+str(point_vente)
				result = "Produit"
			else:
				
				thead = "<tr><th>Carte</th><th>Numéro de la carte</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "gcu.name,gca.num_serie,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt,benin_petro_carte gca,benin_petro_customer gcu,product_product pp"
				critere_relation = "pp.id = gc.product_ids and gca.id = gc.carte_id and gcu.id = gca.libelle and pt.id = pp.product_tmpl_id"
				groupbye = " group by gca.id,gcu.name,gca.num_serie order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				critere+= " and gc.point_vente_id = "+str(point_vente)
				result = "Carte"

		if (point_vente == "All" and client == "All") :
			print "hhhhhhhhhhhhhhhhhbsjdn,fbhsdfjdfnfjsdjfndjkfdn jfnds"
			if(parPoint  == True):
				thead = "<tr><th>Point de vente</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "pv.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,benin_petro_point_vente pv"
				critere_relation = " pv.id = gc.point_vente_id"
				groupbye = " group by gc.point_vente_id,pv.name  order by sum(montant) desc"
				result = "Point de vente"
			else :
				thead = "<tr><th>Client</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "pr.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,benin_petro_point_vente pv,benin_petro_carte gca,res_partner pr"
				critere_relation = " pv.id = gc.point_vente_id and gca.id = gc.carte_id and pr.id=gca.owner_id"
				groupbye = " group by pr.name order by sum(montant) desc"
				result = "Client"



		if (point_vente == "All" and client != "All"):
			if(parProduit  == True):
				thead = "<tr><th>Produit</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "pt.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt,product_product pp"
				critere_relation = "pp.id = gc.product_ids and pt.id = pp.product_tmpl_id"
				groupbye = " group by gc.product_ids,pt.name order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				result = "Produit"

			else :
				thead = "<tr><th>Carte</th><th>Numéro de la carte</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
				field = "gcu.name,gca.num_serie,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,benin_petro_carte gca,benin_petro_customer gcu"
				critere_relation = "gca.id = gc.carte_id and gcu.id = gca.libelle"
				groupbye = " group by gcu.name,gca.num_serie order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				result = "Carte"

		if type_vente=='Vente par TV non connues':
			thead = "<tr><th>Point de vente</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
			field = "pv.name,sum(montant) as Montant"
			relation = " benin_petro_ticke_non_connue gc,benin_petro_point_vente pv"
			critere_relation = " pv.id = gc.point_vente_id"
			groupbye = " group by gc.point_vente_id,pv.name  order by sum(montant) desc"
			result = "Point de vente"

		if type_vente=='Vente par TV' :
			thead = "<tr><th>Produit</th><th>Montant</th><th style='display:none;'>Montant</th></tr>"
			field = " pt.name as Produits,sum(montant) as Montant "
			relation = " benin_petro_carte_consommation gc,product_template pt,product_product pp "
			critere_relation = " pp.id=gc.product_ids and pt.id = gc.product_ids and pt.id = pp.product_tmpl_id"
			groupbye = " group by product_ids,pt.name  order by sum(montant) desc"
			result = "TV par Point de vente"
			if point_vente !="All":
				critere += " and gc.point_vente_id = " + str(point_vente)
			if client != "All":
				critere += " and gc.ticket_id in (select tv.id from benin_petro_ticket_valeur tv where tv.client= " + str(client) +")" 
				
			
	# 	select  gc.product_ids,sum(montant) as montant from benin_petro_carte_consommation gc,product_template pt 
	# where type_vente='Vente par TV' and pt.id=gc.product_ids   and gc.point_vente_id=190
	# group by product_ids

		query = "select "+field+" from "+relation+" where "+critere_relation+critere+groupbye
		print query
		print 'QUERYYYYYYYYYYYYYYYYYYYYYY'
		theade += thead




		self._cr.execute(query)
	except ApiException as e:
		print ("Exception when calling SmsApi->send_sms: %s\n" % e)
	for rec in self._cr.fetchall():
		print 'LIIIIIIIIIIINE'
		if (point_vente != "All" and client == "All"):
			totalMontant+= float(rec[1])
			tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[1])+"</td><td style='display:none;'>"+str(rec[1])+"</td></tr>"
		if (point_vente == "All" and client != "All"):
			print 'client'
			if(parProduit  != True):
				totalMontant+= float(rec[2])
				tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+str(rec[1])+"</td><td>"+locale.format("%d", float(rec[2]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[2])+"</td></tr>"
			else:
				totalMontant+= float(rec[1])
				tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[1])+"</td></tr>"
		if (point_vente != "All" and client != "All"):
			print 'client point de vente'
			if(parProduit  != True):
				totalMontant+= float(rec[2])
				tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+str(rec[1])+"</td><td>"+locale.format("%d", float(rec[2]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[2])+"</td></tr>"
			else:
				totalMontant+= float(rec[1])
				tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[1])+"</td></tr>"
		if (point_vente == "All" and client == "All"):
			print "88888888888888888888888888888888"
			totalMontant+= float(rec[1])
			tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td style='display:none;'>"+str(rec[1])+"</td></tr>"
	tbody += "</tbody><tfoot><tr style='color:red;font-weight:bold;'><td style='text-align:right'>Total : </td><td>"+locale.format("%d", totalMontant, grouping=True)+" CFA</td></tr></tfoot></table>"
	table = theade + tbody
	#print table
    	return {"table":table}





    @api.multi
    def getPointVente(self):
	self._cr.execute("select id,name from benin_petro_point_vente where name is not null order by name ASC") 
	data = "<select> <option value='All'>Tous</option>"
	for rec in self._cr.fetchall():
		data += "<option value='"+str(rec[0])+"'>"+str(rec[1].encode('utf-8'))+"</option>"

    	return data

    @api.multi
    def getClient(self):
	self._cr.execute("select id,name from res_partner where create_uid != 1 order by name asc") 
	data = "<select> <option value='All'>Tous</option>"
	for rec in self._cr.fetchall():
		data += "<option value='"+str(rec[0])+"'>"+str(rec[1].encode('utf-8'))+"</option>"

    	return data		
	
