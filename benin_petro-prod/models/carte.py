# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from datetime import date, datetime, timedelta
import dateutil.relativedelta as relativedelta
from random import randint
# from keyid import keyid
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
#from twilio.rest import Client


class benin_petro_type_carte(models.Model):
    _name = 'benin_petro.type.carte'

    _rec_name = 'libelle'
    _description = ''

    #company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    libelle = fields.Char(string="Libellé")
    front_carte = fields.Binary(string="Background du recto")
    front_carte_name = fields.Char("Background du recto")
    back_carte = fields.Binary(string="Background du verso")
    back_carte_name = fields.Char("Background du verso")
    state = fields.Selection([('activee','Actiée'),('suspendu','Suspendu'),('annule','Annulée')] , string="Statut" , default="activee")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )





class benin_petro_carte(models.Model):
    _name = 'benin_petro.carte'

    _rec_name = 'libelle'
    _description = ''


    @api.multi
    def setToBrouillon(self):
        self.ensure_one()
        self.state="brouillon"

    @api.multi
    def setToActivee(self):
        self.ensure_one()
        self.state="activee"
	self.date_activation=fields.datetime.now()

    @api.multi
    def setToGenere(self):
        self.ensure_one()
        self.state="generee"


    @api.multi
    def setToEnd(self):
        self.ensure_one()
        self.state="terminee"
	self.date_termine=fields.datetime.now()

    @api.multi
    def setToSuspendu(self):
        self.ensure_one()
        self.state="suspendu"
	self.date_suspension=fields.datetime.now()

    @api.multi
    def setToPerdu(self):
        self.ensure_one()
        self.state="perdu"
	self.date_perte=fields.datetime.now()

    @api.multi
    def setToExpire(self):
        self.ensure_one()
        self.state="expiree"
	self.date_expiration=fields.datetime.now()

    @api.multi
    def setToAnnule(self):
        self.ensure_one()
        self.state="annule"
	self.date_annulation=fields.datetime.now()



    def _default_serie(self):
	result = True
	serie_proposition = 0
        while result==True:
		serie_proposition = str(randint(111, 999)) + str(randint(111, 999)) + str(randint(111, 999))
		result = self.search([['num_serie', '=', int(serie_proposition)]]).id
        return serie_proposition

    def _getQrCode(self,string):
	import hashlib
	md5 = hashlib.md5()
	qrcode = ""
	result = True
	serie_proposition = 0
        while result==True:
		md5.update(string+str(serie_proposition))
		qrcode = md5.hexdigest()
		serie_proposition += 1 
		result = self.search([['qrcode', '=', qrcode ]]).id
	return qrcode

    @api.multi
    def setCodePine(self):
        self.ensure_one()
        codepin = randint(1111, 9999)
        self.code_pin = codepin

        body = """Cate """+self.libelle.name+""" votre code PIN est : """+str(codepin)
        Subject = "BENIN PETRO"
        mobile = self.libelle.mobile
        mailsto = self.libelle.email
        
#        try:
        if mailsto:
            self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
#        if mobile:
#            self.env["benin_petro.carte"].sendWhatssap(mobile,body)
#        except ApiException as e:
#            print ("Exception when calling SmsApi->send_sms: %s\n" % e)



    #@api.depends('num_serie_hide')
    @api.onchange('libelle')
    def _send_serie(self):
	
	i = -1  # This could have been any integer, positive or negative
	today = fields.datetime.now().date()
#(self.create_date).strftime('%Y-%m-%d %H:%M:%S')


#date.strptime(self.create_date,'%Y-%m-%d %H:%M:%S') #date.today()

	nextyear = fields.datetime.now().replace(year=fields.datetime.now().year + 2)
	#nextyear = fields.date.now().replace(year=fields.date.now().year + 2)

	

    @api.constrains('solde')
    def _check_solde(self):
        if self.solde<0:
            raise ValidationError(_("Le solde de la carte devrait rester superieur ou égal à zéro"))
	#elif self.solde>self.owner_id.solde_compte:
        #    raise ValidationError(_("------------solde < solde owner ----------"))



    @api.multi
    def getCartByQrcode(self):
	print "======================"
	print "======================"
	print "======================"
	print "======================"
	print "======================"
	print "======================"
	print "======================"
	#carte = self.search([['qrcode', '=', qrcode]])
        
        return 88
    @api.one
    @api.depends('compute_field')
    def _get_user(self):
		self.ensure_one()
		if self.env.user.has_group('benin_petro.group_benin_petro_client') or self.env.user.has_group('benin_petro.group_benin_petro_sous_chargeur') or self.env.user.has_group('benin_petro.group_benin_petro_president') or self.env.user.has_group('benin_petro.group_benin_petro_chargeur'):
			self.compute_field = True
		else:
			self.compute_field = False

    @api.one
    @api.depends('compute_admin')
    def _get_admin(self):
		self.ensure_one()
		if self.env.user.has_group('benin_petro.group_benin_petro_adminn'):
			self.compute_admin = True
		else:
			self.compute_admin = False


    # ***************************************************************************************
    
    #company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    owner_id = fields.Many2one("res.partner",string="Client")
    type_carte_id = fields.Many2one("benin_petro.type.carte",string="Type de carte", required=True)
    libelle = fields.Many2one("benin_petro.customer",string="Consommateur")
    num_serie = fields.Integer(string="Numéro de serie")
    code_pin = fields.Integer(string="code pin")
    qrcode = fields.Char(string="dddd")
    solde = fields.Float(string='Solde actuel')
    montant_affecter = fields.Float(string='Montant à affecter')
    date_activation = fields.Datetime("Date d'activation", readonly=True)
    date_perte = fields.Datetime("Date de perte", readonly=True)
    date_suspension = fields.Datetime("Date de suspension", readonly=True)
    date_expiration = fields.Date("Date d'expiration", readonly=True)
    date_termine = fields.Datetime("Date fin service", readonly=True)
    date_annulation = fields.Datetime("Date d'annulation", readonly=True)
    carte_consommation_ids = fields.One2many("benin_petro.carte.consommation","carte_id",string="Historiques", readonly=True)
    log_ids = fields.One2many("benin_petro.log","carte_id",string="Historiques", readonly=True)
    state = fields.Selection([('brouillon','Brouillon'),('generee','Générée'),('suspendu','Suspendu'),('expiree','Expirée'),('perdu','Perdue'),('terminee','Terminée'),('annule','Annulée')],string="Statut",default="generee")
    click_create = fields.Boolean("check click")
    compute_field = fields.Boolean(string="check field", compute='_get_user')
    compute_admin = fields.Boolean(string="check admin", compute='_get_admin')
    product_ids = fields.Many2many("product.product", "carte_product_relation", "carte_id", "product_id","Liste des produits")
    point_vente_ids = fields.Many2many("benin_petro.point.vente", "carte_point_vente_relation", "carte_id", "point_vente_id","Liste des points de vente")
    historique_sublim = fields.One2many(comodel_name='benin_petro.historique', inverse_name='carte_sublim', string='Historique',domain=[('type_af','=','sublime carte')])
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    type_carte = fields.Selection([('pre_imprimer','Pré imprimer'),('normal','Normal')] , string="Type de carte" , default="normal")
    carte_preimprime = fields.Many2one("benin_petro.carte.preimprime",string="Carte pre imprime")
    kilometrage = fields.Boolean("Kilométrage")
    kilometrage_ids = fields.One2many("benin_petro.kilometrage","carte_id",string="Rapport du kilométrage", readonly=True)

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
	server.login(mail_server.smtp_user.encode('utf8'),mail_server.smtp_pass.encode('utf8'))
	text = msg.as_string()
	server.sendmail(mail_server.smtp_host, mailsto.split(','), text)
	return True

    def sendWhatssap(self,to,body):
        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        # Your Account SID from twilio.com/console
        account_sid = "AC31f2645f7484c5a542ae2031a91b79ad"
        # Your Auth Token from twilio.com/console
        auth_token  = "11b37df21eb388905d730d05cf810ca8"

        client = Client(account_sid, auth_token)

        # this is the Twilio sandbox testing number
        from_whatsapp_number='whatsapp:+14155238886'
        # replace this number with your own WhatsApp Messaging number
        to_whatsapp_number='whatsapp:+'+to

        client.messages.create(body=body,
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)

    @api.model
    def create(self, vals):
        carteResult = True
        if vals.get('owner_id'):
            owner = self.env["res.partner"].search([['id', '=', int(vals.get('owner_id'))]])
            if vals.get("montant_affecter",False) > owner.solde_compte:
                raise ValidationError(_("------------ Le solde affecté à la carte > au solde du compte client  ----------"))
            if vals.get("montant_affecter",False) and vals.get("montant_affecter",False)>0:
                vals['solde'] = vals.get("montant_affecter",False)
                vals['montant_affecter'] = 0
            elif vals.get("montant_affecter",False)<0:
                raise ValidationError(_("------------solde affecter au carte > 0 ----------"))

            obj = self.env['benin_petro.customer'].browse(vals['libelle'])
            #print obj.mobile
            obj["partner_id"] = vals['owner_id']
        today = fields.datetime.now().date()
        vals['date_expiration'] = today.replace(year=today.year + 2)
        vals['num_serie'] = self._default_serie()
        codepin = randint(1111, 9999)
        vals['code_pin'] = codepin
        qrcode = self._getQrCode(str(vals.get("num_serie"))+'<:>AKAD<:>'+str(vals.get("date_expiration")))
        if qrcode=="":
            raise ValidationError(_("Merci de contacter le prestataire pour la génération du QRCODE"))
        vals['qrcode'] = qrcode
        vals['click_create'] = True
        if not vals.get('owner_id'):
            vals['type_carte'] = "pre_imprimer"
            vals['state'] = "brouillon"
        carteResult = super(benin_petro_carte, self).create(vals)
        
        if vals.get('owner_id'):
            body = """Merci de noter le code PIN de la carte : """+ str(codepin)+""" dont le consommateur : """+str(obj.name)
            Subject = "BENIN PETRO"
            mobile = obj.mobile
            mailsto = obj.email
#            try:
            if mailsto:
                self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
#            if mobile:
#                self.env["benin_petro.carte"].sendWhatssap(mobile,body)
#            except ApiException as e:
#                print ("Exception when calling SmsApi->send_sms: %s\n" % e)
        # else:
        #     carteResult = super(benin_petro_carte, self).create(vals)
	
        return carteResult





    @api.multi
    def write(self, vals):
	for carte in self:
		acteurName = self.env.user.name
		logs = []
		if vals.get("acteur_name",False):
			acteurName = vals.get("acteur_name",False)
		crt = self.search([['id', '=', carte.id]])
		if vals.get("libelle",False):
			logs.append(self.log(self.id,acteurName,self.libelle,vals.get("libelle",False),"Libellé"))
			
			
		if vals.get("montant_affecter",False):
			solde = crt.solde
			owner = crt.owner_id
			if vals.get("montant_affecter",False) <0:
			    raise ValidationError(_("------------ Le solde affecté à la carte doit être superieru à 0  ----------"))
			if vals.get("montant_affecter",False) > owner.solde_compte:
			    raise ValidationError(_("------------ Le solde affecté à la carte > au solde du compte client  ----------"))
			if vals.get("montant_affecter",False) > owner.solde_compte_hide:
				raise ValidationError(_("------------ Le solde affecté à la carte > au solde du compte client  ----------"))
			else:
				owner.solde_compte_hide = owner.solde_compte_hide - vals.get("montant_affecter",False)
			
			vals['solde'] = solde + vals.get("montant_affecter",False)
			montant_affecter = vals['montant_affecter']
			vals['montant_affecter'] = 0
			logs.append(self.log(self.id,acteurName,str(self.solde),str(vals.get("solde",False)),"Solde"))
			print "8888888888888888888"
			print montant_affecter
			res = self.env['benin_petro.historique'].create({
			'type_op':'Recharge carte',
			'carte_sublim':self.id,
			'type_af':'sublime carte',
			'debit':0,
			'credit':montant_affecter,
			'solde_carte':vals.get("solde",False),  
			})
			if vals.get('solde',False)<0:
				raise ValidationError(_("Le solde de la carte devrait rester superieur ou égal à zéro"))
		if logs:
			vals['log_ids'] = logs
	
	return super(benin_petro_carte, self).write(vals)


    def log(self,ObjtId,acteurName,old_version,new_version,champ):
	return (0,0, {
				"carte_id" : ObjtId,
				"acteur_name" : acteurName,
				"old_version" : old_version,
				"new_version" : new_version,
				"champ" : champ,
			})

class benin_petro_carte_consommation(models.Model):
    _name = 'benin_petro.carte.consommation'

    _rec_name = 'id'
    _description = ''

    #company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente", required=True)
    point_vente_id_card = fields.Many2one("benin_petro.point.vente",string="Point dehkhlk vente",compute='_getPV')
    point_vente_id_tv = fields.Many2one("benin_petro.point.vente",string="Point de vente",compute='_getPV')
    agent_id = fields.Many2one("benin_petro.agent",string="Agent")
    carte_id = fields.Many2one("benin_petro.carte",string="Carte")
    product_ids = fields.Many2one("product.product",string="Produit", required=True)
    quantite = fields.Float(string='Quantité')
    quantite_remise = fields.Float(string='Quantité remisé')
    montant = fields.Float(string='Montant TTC')
    shift_id = fields.Many2one("benin_petro.carte.shift",string="Shift")
    valider_par_agent = fields.Boolean(string ="Validé par l'agent")
    valider_par_gerant = fields.Boolean(string ="Validé par le gérant")
    verse = fields.Boolean(string ="verser par le gérant", default=False)
    state = fields.Selection([('valider','Valider'),('annuler','Annuler'),('paye','paye')] , string="Statut" , default="valider")
    hest_ben_ids = fields.One2many("benin_petro.historique_ben","hes_id",string="Historiques")
    bonus_conso = fields.Float(string="Bonus consommateur")
    total_bonus = fields.Float(string="Total bonus")
    ticket_id = fields.Many2one("benin_petro.ticket_valeur",string="Ticket")
    type_vente = fields.Selection([('Vente au comptant','Vente au comptant'),('Vente par SUBLIME CARTE','Vente par SUBLIME CARTE'),('Vente par TV','Vente par TV'),('Vente par MONO PAY','Vente par MONO PAY'),('Vente par carte tampo','Vente par carte tampo')] , string="Type de vente",default="Vente par SUBLIME CARTE")
    payement_id = fields.Many2one('benin_petro.tv_station_hestory',string='paiement')
    tv_station = fields.Many2one('benin_petro.point.vente',string='Tv Station')
    total_tva = fields.Float(string="TVA")
    total_hors_taxe = fields.Float(string="Montant hors taxes")
    immatriculation = fields.Char(string="L'immatriculation")
    reste_carte = fields.Float(string="Reste carte")
    montant_avant = fields.Float(string="Montant avant")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    ticket_ids = fields.One2many("benin_petro.ticket_valeur","consom",string="Liste des tickets")
    recus_avoir = fields.Many2one("benin_petro.ticket_valeur",string="Reçus d'avoir")
    date_consommation = fields.Datetime("Date transaction",compute='_get_date_utc')
    kilometrage = fields.Char("Kilometrage")
    
    @api.multi
    def _get_date_utc(self):
        for record in self:
            record.date_consommation = datetime.strptime(record.create_date, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
    

    @api.multi
    def _getPV(self):
        for s in self:
            s.point_vente_id_tv = s.point_vente_id
            s.point_vente_id_card = s.point_vente_id
            
    @api.model
    def create(self, vals):
        print 'creaaaaaaaaaaaaaaaaaaate'
        print vals.get('product_ids')
        product = self.env["product.product"].search([['id', '=', int(vals.get('product_ids'))]])
        product_type = product.categories_consomable
        product_tva = product.taxes_id.amount
        tva =0
        print product_type
        if product_type == 'Lubrifiants':
            tva = (float(vals.get('montant')) * float(product.taxes_id.amount))/100
            print product.taxes_id.amount
        if product_type == 'Produits blancs':
            print '88888888888'
            qte = float(vals.get('montant')) / product.lst_price
            tva = format((qte * float(product.taxes_id.amount)),'.2f')
        vals['total_tva'] = tva
        vals['total_hors_taxe'] = float(vals.get('montant')) - float(tva)

        print 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        print vals
        # if vals.get("type_vente") == "Vente par SUBLIME CARTE":
        #     catre = self.env["benin_petro.carte"].search([['id', '=', int(vals["carte_id"])]])
        #     print catre
        #     print '-------------------------------'
        #     print vals
        #     print '==============================='
        #     ben_hest = []
        #     vals["bonus_conso"] = float(float(float(catre.libelle.taux) * float(vals["montant"]))/100)
        #     #vals["total_bonus"] = float(vals["bonus_conso"])+
        #     res = super(benin_petro_carte_consommation, self).create(vals)
        #     print 'yyyyyyyyyyyyyyyffffffffffffffffyyyyyyyyyyyyyyyy'
        #     print catre.owner_id
        #     print catre.owner_id.beneficiaires_ids
        #     total = 0
        #     if catre.owner_id.beneficiaires_ids:
        #         for ben in catre.owner_id.beneficiaires_ids:
        #             print ben.name
        #             mnt = float(float(float(ben.taux) * float(vals["montant"]))/100)
        #             total += mnt
        #             print '*********************'
        #             print mnt
        #             print ben
        #             historique_vals ={
        #                 'hes_id':res.id,
        #                 'beneficiaire_id':ben.id,
        #                 'mnt':mnt
        #             }
        #             print historique_vals
        #             cal = self.env["benin_petro.historique_ben"].create(historique_vals)
        #             print cal
        #             ben_hest.append(cal)
        #     transaction = self.env["benin_petro.carte.consommation"].search([['id', '=', int(res)]])
        #     transaction.total_bonus = float(float(total) + float(transaction.bonus_conso))
        # else:
        res = super(benin_petro_carte_consommation, self).create(vals)
            #res = True
        # print ben_hest
        # vals["hest_ben_ids"] = (0, 0, ben_hest)
        return res



class benin_petro_carte_shift(models.Model):
    _name = 'benin_petro.carte.shift'

    transaction_ids = fields.One2many("benin_petro.carte.consommation","shift_id",string="Agents")
    libele = fields.Char(string="Libele")
    agent_id = fields.Many2one("benin_petro.agent",string="Agent")
    pointVente_id = fields.Many2one("benin_petro.point.vente",string="Point Vente")
    gerant_id = fields.Many2one("benin_petro.agent",string="Gerant")
    total = fields.Char(string="Total")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    @api.model
    def create(self, vals):
        print 'vaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaals'
        print vals
        
	return super(benin_petro_carte_shift, self).create(vals)


class benin_petro_log(models.Model):
    _name = 'benin_petro.log'

    _rec_name = 'carte_id'
    _description = ''

    #company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    acteur_name = fields.Char(string="Acteur")
    client_id = fields.Many2one("res.partner",string="Client")
    carte_id = fields.Many2one("benin_petro.carte",string="Carte")
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    agent_id = fields.Many2one("benin_petro.agent",string="Agent")
    old_version = fields.Char(string="Ancienne valeur")
    new_version = fields.Char(string="Nouvelle valeur")
    champ = fields.Char(string="Type modification")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )





class benin_petro_agent(models.Model):
    _name = 'benin_petro.agent'

    _rec_name = 'name'
    _description = ''


    @api.multi
    def setToActive(self):
        self.ensure_one()
        self.state="activee"
	self.date_activation=fields.datetime.now()

    @api.multi
    def setToSuspendu(self):
        self.ensure_one()
        self.state="suspendu"
	self.date_suspension=fields.datetime.now()

    @api.multi
    def setToAnnule(self):
        self.ensure_one()
        self.state="annule"
	self.date_annulation=fields.datetime.now()

    @api.multi
    def setCodePine(self):
        self.ensure_one()
        # historique = self.env["benin_petro.historique"].search([('id', '>', int(16562)),('sous_chargeur','=',2)])
        # print("#################")
        # for h in historique:
        #     h.montant_init = float(h.montant_init) + 10000000
        # print("#################")

        password = randint(1111, 9999)
        self.password = password
        body = """Merci de noter votre code PIN : """+ str(password)
        Subject = "BENIN PETRO"
        mobile = self.telephone
        """api_instance = swagger_client.SmsApi()
        smsrequest = swagger_client.SmsUniqueRequest("eb717305f6545b5ea0d57a7aba06dc54",None, None, body,mobile,Subject,None,None,None, None, None) # SMSRequest | sms request
        try:
            api_response = api_instance.send_sms(smsrequest)
        except ApiException as e:
            print ("Exception when calling SmsApi->send_sms: %s\n" % e)"""

    _sql_constraints = [('matricule_unique', 'unique(matricule)', 'Agent déja existe')]
    #company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    name = fields.Char(string="Nom")
    fonction = fields.Selection([('Gerant','Gérant'),('Pompiste','Pompiste'),('Boutiquier','Boutiquier'),('Chauffeur','Chauffeur'),('Autre','Autre')] , string="Fonction" , default="Pompiste")
    autre_fonction = fields.Char(string="Autre fonction")
    matricule = fields.Char(string="Matricule",required=True)
    password = fields.Char(string="password")
    telephone = fields.Char(string="Téléphone",required=True)
    mail = fields.Char(string="Email")
    adress = fields.Text(string="Adresse")
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    state = fields.Selection([('activee','Activé'),('suspendu','Suspendu'),('annule','Annulée') ] , string="Statut" , default="activee")
    date_activation = fields.Datetime("Date d'activation", readonly=True)
    date_suspension = fields.Datetime("Date de suspension", readonly=True)
    date_annulation = fields.Datetime("Date d'annulation", readonly=True)
    log_ids = fields.One2many("benin_petro.log","agent_id",string="Historiques", readonly=True)
    transaction_ids = fields.One2many("benin_petro.carte.consommation","agent_id",string="Historiques", readonly=True)
    camion_id = fields.Many2one('fleet.vehicle', string='Camion')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    validation_ids = fields.One2many("benin_petro.carte.preimprime.validate","agent",string="Historiques des validation", readonly=True)
    recharge_carte_ids = fields.One2many("benin_petro.historique","gerant",string="Historiques des rechatrges cartes", domain=[('type_op','=','Recharge carte'),('debit','=',0)])
    recharge_client_ids = fields.One2many("benin_petro.historique","gerant",string="Historiques des rechatrges clients", domain=[('type_op','=','Recharge client')])
    montant_plafond = fields.Float(string='Montant plafond SUBLIME CARTE',required=True)
    historique_sublim = fields.One2many(comodel_name='benin_petro.historique', inverse_name='gerant', string='Historique',domain=['|',('type_op','=','RECHARGE MONETIQUE Gérant'),('type_op','=','Recharge carte'),('montant_fin','!=',0)])

    @api.model
    def create(self, vals):
        password = randint(1111, 9999)
        vals['password'] = password
        body = """Bonjour,
        Veuillez noter votre code PIN : """+ str(password)
        Subject = "BENIN PETRO"
        mobile = self.telephone
        """api_instance = swagger_client.SmsApi()
        smsrequest = swagger_client.SmsUniqueRequest("eb717305f6545b5ea0d57a7aba06dc54",None, None, body,mobile,Subject,None,None,None, None, None) # SMSRequest | sms request
        try:
            api_response = api_instance.send_sms(smsrequest)
        except ApiException as e:
            print ("Exception when calling SmsApi->send_sms: %s\n" % e)"""
        
	return super(benin_petro_agent, self).create(vals)


    @api.multi
    def write(self, vals):
	for carte in self:
		logs = []
		acteurName = self.env.user.name
		if vals.get("acteur_name",False):
			acteurName = vals.get("acteur_name",False)
		
		if vals.get("name",False):
		   logs.append(self.log(self.id,acteurName,self.name,vals.get("name",False),"Nom"))

		if vals.get("fonction",False):
		   logs.append(self.log(self.id,acteurName,self.fonction,vals.get("fonction",False),"Fonction"))

		if vals.get("matricule",False):
		   logs.append(self.log(self.id,acteurName,self.matricule,vals.get("matricule",False),"Matricule"))

		
		if vals.get("mail",False):
		   logs.append(self.log(self.id,acteurName,self.mail,vals.get("mail",False),"Email"))

		
		if vals.get("adress",False):
		   logs.append(self.log(self.id,acteurName,self.adress,vals.get("adress",False),"Adresse"))


		if logs:
			vals['log_ids'] = logs
	
	return super(benin_petro_agent, self).write(vals)

    def log(self,ObjtId,acteurName,old_version,new_version,champ):
	return (0,0, {
				"agent_id" : ObjtId,
				"acteur_name" : acteurName,
				"old_version" : old_version,
				"new_version" : new_version,
				"champ" : champ,
			})


class ModuleName(models.Model):
    _inherit = 'account.account'

    is_true = fields.Boolean(string='is True')

