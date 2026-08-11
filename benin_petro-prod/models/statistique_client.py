# -*- coding: utf-8 -*-

from odoo import fields, api, models,_
from datetime import date
import locale
# from swagger_client.rest import ApiException

class benin_petro_statistique(models.Model):
    _name = 'benin_petro.statistique_client'

    call_statistique_widgett = fields.Char(string="widget")


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
	client = self.env.user.partner_id.id
	print '---------------------------------------------'
	print client
	print '---------------------------------------------'
	thead = "<tr><td>Client</td><td>Solde avant</td><td>Solde aprés</td><td>Montant de la recharge</td></tr>"
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
	
    	query ="""select r.name,l.old_version,l.new_version,(CAST (l.new_version AS float)-CAST (l.old_version AS float)) as Recharge  from benin_petro_log l,res_partner r where l.client_id = r.id  and champ = 'Solde non affecte' and (CAST (l.new_version AS float) > CAST (l.old_version AS float)) """+str(critere)+""" order by  r.name"""


	print query
    	self._cr.execute(query)
	
    	for rec in self._cr.fetchall():
    		totalMontant+= float(rec[3])
    		tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td><td>"+locale.format("%d", float(rec[2]), grouping=True)+" CFA</td><td>"+locale.format("%d", float(rec[3]), grouping=True)+" CFA</td></tr>"
    	tbody += "</tbody><tfoot><tr style='color:red;font-weight:bold;'><td></td><td></td><td style='text-align:right'>Total : </td><td>"+locale.format("%d", totalMontant, grouping=True)+" CFA</td></tr></tfoot></table>"
	theade += thead
	table = theade + tbody

    	return {"table":table}	



    @api.multi
    def getResult(self,point_vente,year,month,datedebut,datefin,parProduit,parCarte):
	print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
	print point_vente
	field = ""
 	relation = ""
	client = self.env.user.partner_id.id
	critere_relation = ""
	groupbye = ""
	critere = " and gc.state='valider'"
 	query = "" 
	table = ""
 	tbody ="</thead><tbody>"
	thead = ""
	theade ="<table id='result_datatable' class='table table-striped table-bordered' cellspacing='0' width='100%'><thead>"
	tfoot = ""
	result = ""
	totalMontant = 0
	# if year != "All":
	# 	critere+= " and EXTRACT( year from gc.create_date) = "+str(year)
	# if month != "All":
	# 	critere+= " and EXTRACT( month from gc.create_date) = "+str(month)
	try:

		if (datedebut and datefin):
			critere+= " and date(gc.create_date) between '"+datedebut+"' and '"+datefin+"' "
		
		if(point_vente != "All") :
			if(parProduit == True) :
				print 'ooooooooooooooooooooo'
				thead = "<tr><th>Produit</th><th>Montant</th></tr>"
				field = "pt.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt"
				critere_relation = "pt.id = gc.product_ids"
				groupbye = " group by gc.product_ids,pt.name"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				critere+= " and gc.point_vente_id = "+point_vente
				result = "Produit"
			else:
				
				thead = "<tr><th>Carte</th><th>Montant</th></tr>"
				field = "gcu.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt,benin_petro_carte gca,benin_petro_customer gcu"
				critere_relation = "pt.id = gc.product_ids and gca.id = gc.carte_id and gcu.id = gca.libelle"
				groupbye = " group by gca.id,gcu.name order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				critere+= " and gc.point_vente_id = "+point_vente
				result = "Carte"

		if (point_vente == "All"):
			if(parProduit  == True):
				thead = "<tr><th>Produit</th><th>Montant</th></tr>"
				field = "pt.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,product_template pt"
				critere_relation = "pt.id = gc.product_ids"
				groupbye = " group by gc.product_ids,pt.name order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				result = "Produit"

			else :
				thead = "<tr><th>Carte</th><th>Montant</th></tr>"
				field = "gcu.name,sum(montant) as Montant"
				relation = " benin_petro_carte_consommation gc,benin_petro_carte gca,benin_petro_customer gcu"
				critere_relation = "gca.id = gc.carte_id and gcu.id = gca.libelle"
				groupbye = " group by gca.id,gcu.name order by sum(montant) desc"
				critere += " and carte_id in (select id from benin_petro_carte where owner_id = "+str(client)+")"
				result = "Carte"

			

			
		query = "select "+field+" from "+relation+" where "+critere_relation+critere+groupbye
		print query
		theade += thead




		self._cr.execute(query)
	except ApiException as e:
		print ("Exception when calling SmsApi->send_sms: %s\n" % e)
	
	for rec in self._cr.fetchall():
		totalMontant+= float(rec[1])
		tbody +="<tr><td>"+str(rec[0].encode('utf-8'))+"</td><td>"+locale.format("%d", float(rec[1]), grouping=True)+" CFA</td></tr>"
	tbody += "</tbody><tfoot><tr style='color:red;font-weight:bold;'><td style='text-align:right'>Total : </td><td>"+locale.format("%d", totalMontant, grouping=True)+" CFA</td></tr></tfoot></table>"
	table = theade + tbody

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
		self._cr.execute("select id,name from res_partner order by name asc") 
		data = "<select> <option value='All'>Tous</option>"
		for rec in self._cr.fetchall():
			data += "<option value='"+str(rec[0])+"'>"+str(rec[1].encode('utf-8'))+"</option>"
		return data		
	
