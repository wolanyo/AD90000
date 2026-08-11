# -*- coding: utf-8 -*-
from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from random import randint
# from keyid import keyid
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    @api.depends('auditeur_acc')
    def _get_auditeur_read(self):
        if self.env.user.has_group('benin_petro.group_benin_petro_auditeur'):
            self.auditeur_acc = False
        else:
            self.auditeur_acc = True

    def getContryByDefault(self):
        return self.env['res.country'].search([['code', '=', 'BJ']]).id

    @api.one
    @api.depends('compute_field')
    def _get_user(self):
        self.ensure_one()
        if not self.env.user.has_group('benin_petro.group_benin_petro_adminn') :
            self.compute_field = True
        else:
            self.compute_field = False

    @api.depends('carte_ids')
    def _getSoldeCarte(self):
        for client in self:
            for carte in client.carte_ids:
                client.solde_carte += carte.solde


    # @api.multi
    # def getClientByTest(self,qrcode):
    #     print aaaaa
    #     print 'Oooooooooooooo'

    @api.multi
    def setCodePine(self):
        if not self.supplier:
            self.ensure_one()
            codepin = randint(1111, 9999)
            self.password = codepin
            self.access.password = codepin
            body = """Merci de noter votre nouveau code PIN est : """+ str(codepin)
            Subject = "BENIN PETRO"
            mobile = self.mobile
            mailsto = self.email
            if not self.taux:
            #            try:
                if mailsto:
                    self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
    #            if mobile:
    #                self.env["benin_petro.carte"].sendWhatssap(mobile,body)
    #            except ApiException as e:
    #                print ("Exception when calling SmsApi->send_sms: %s\n" % e)




    @api.depends('carte_ids')#@api.onchange('carte_ids')
    def _getSoldeAffect(self):
        for client in self:
            # print client.id
            affectation = 0
            for carte in client.carte_ids:
                affectation += carte.montant_affecter
            client.update({
                'solde_compte': client.solde_compte_hide - affectation
            })




    name = fields.Char(size=50)
    log_ids = fields.One2many("benin_petro.log","client_id",string="Historiques", readonly=True)
    login = fields.Char(string="Nom d'utilisateur")
    password = fields.Char(string="Mot de passe",copy=False)
    phone = fields.Char(string="Phone")
    reset_password = fields.Char(string="code de validation")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=getContryByDefault)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    solde_compte = fields.Float(string='Solde non affecté', store=True, compute='_getSoldeAffect')
    solde_carte = fields.Float(string='Solde affecté aux cartes',compute='_getSoldeCarte', store=True)
    solde_compte_hide = fields.Float(string='Solde non affecté')
    carte_ids = fields.One2many("benin_petro.carte","owner_id",string="cartes", required=True)
    beneficiaires_ids = fields.One2many("benin_petro.bseneficiaire","owner_id",string="beneficiaires",limit=4)
    customers_id = fields.One2many("benin_petro.customer","partner_id",string="Consommateur",required=True,)
    #password_validate = fields.Char(string="code validate", store=True)
    access = fields.Many2one("res.users",string="user")
    sold_trenserts = fields.One2many("benin_petro.sold_transfert",'compte',string="Trensferts")
    compute_field = fields.Boolean(string="check field", compute='_get_user')
    auditeur_acc = fields.Boolean(string="auditeur access" , compute='_get_auditeur_read')
    client_type = fields.Selection([('client_normal','Non'),('client_acc','Oui')],string="Esccomptes accordés",required=True,default="client_normal")
    valuer_a_accorde=fields.Integer(string='Valeur à accordé')
    tv_ids = fields.One2many('benin_petro.ticket_valeur','client',string='Tickets')
    mysql_id = fields.Integer(string='mysql Id')
    is_tv = fields.Boolean(string='')
    commercial = fields.Many2one('benin_petro.commercial',string='Commercial',required=True)
    recharge_ids = fields.One2many("benin_petro.historique","client_id",string="Liste des recharge",domain=[('type_af','=','sublime carte'),('client_id','!=',False),('sous_chargeur','=',False)])
    recharge_tv_ids = fields.One2many("benin_petro.historique","client_id",string="Liste des recharge",domain=[('type_af','=','TV'),('client_id','!=',False),('type_op','=','Vente de tv')])
    historiqueKkiapay = fields.One2many("benin_petro.historiquekkiapay",'client_id',string="Historique")
    codeClient = fields.Char(string="Code client NAV",required=True)

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

    @api.constrains('client_type', 'valuer_a_accorde')
    def _check_participant(self):
        if self.solde_compte<0 in self.solde_compte_hide<0:
            raise ValidationError(_("Le solde du compte client devrait être supérieur ou égal à zéro"))

    # @api.constrains('solde_compte', 'solde_compte_hide')
    # def _check_client_type(self):
    #     if self.client_type=='client_acc' and self.valuer_a_accorde<=0:

    #         raise ValidationError(_("Le Valeur à accordé devrait être supérieur  à zéro"))

    def createCode(self,codeCl,codeF):
        res = self.env['res.partner'].sudo().search([])
        res.write({
            'property_account_receivable_id':codeCl,
            'property_account_payable_id':codeF
        })
    def changeCompte(self):
        self.createCode(19583,19552)

    @api.model
    def create(self, vals):
        # if  vals.get('client_type',False)  in ('client_normal','client_acc'):
        client = self.search([['codeClient', '=', vals.get('codeClient')]])
        if not vals.get('supplier',False):
            # print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            # print aaaaaaa
            if len(client) != 0  and vals.get('codeClient') != None:
                raise ValidationError(_("------------ Code client déjà existe  ----------"))
            if vals.get('mobile'):
                if not vals.get("taux"):
                    vals['solde_compte_hide'] = self.solde_compte
                    codepin = randint(1111, 9999)
                    vals['password'] = codepin
                    body = """BENIN PETRO vous remercie pour votre confiance .Merci de noter le mot de passe de l'application mobile : """+ str(codepin)
                    Subject = "BENIN PETRO"
                    mailsto = vals.get("email") #self.env['res.partner'].search([["id","=",vals.get('owner_id',False)]]).email
                    mobile = vals.get('mobile')
                p = super(res_partner, self).create(vals)
                # print 'ooooooooooooooooooooooo'
                cl = self.env["res.users"].create({
                    'display_name':vals.get('name'),
                    'password':codepin,
                    'company_id':vals.get('company_id'),
                    'name':vals['name'],
                    'signup_token':vals.get('email'),
                    'partner_id':p.id,
                    'email':vals.get('email'),
                    'owner_id':False,
                    "login":vals.get('mobile'),
                    #'in_group_22':True,
                    'active':True,
                    'share':False,
                    'groups_id': [( 4, self.env.ref('benin_petro.group_benin_petro_client').id),(4, self.env.ref('base.group_user').id)]
                })
                if not vals.get("taux"):
                    if cl:
                #                    try:
                        if mailsto:
                            print('oooooo')
                # self.env["benin_petro.carte"].SendMail(mailsto,Subject,body)
                #                    if mobile:
                #                        self.env["benin_petro.carte"].sendWhatssap(mobile,body)
                #                    except ApiException as e:
                #                        print ("Exception when calling SmsApi->send_sms: %s\n" % e)

                p.write({
                    'access':cl.id
                })
            else:
                if len(client) != 0  and vals.get('codeClient') != None:
                    raise ValidationError(_("------------ Code client déjà existe  ----------"))
                p = super(res_partner, self).create(vals)
            return p
        else:
            # print 'CREAAAAAAAATE FROURN'
            if len(client) != 0  and vals.get('codeClient') != None:
                raise ValidationError(_("------------ Code client déjà existe  ----------"))
            
            # print aaaaaaa
            return super(res_partner, self).create(vals)
    # else :
    #     raise ValidationError("Veulliez renseigner le champ comptes accordés")





    @api.multi
    def write(self, vals):
        # print "=================== write"
        # print "############################"
        #
        # print self.solde_compte
        # print "############################"
        client = self.search([['codeClient', '=', vals.get('codeClient')]])
        print("###########Clientttt")
        if len(client) != 0 and vals.get('codeClient') != None:
            raise ValidationError(_("------------ Code client déjà existe  ----------"))
        logs = []
        acteurName = self.env.user.name

        if vals.get("acteur_name",False):
            acteurName = vals.get("acteur_name",False)
        if vals.get("solde_compte_hide",False):
            vals['solde_compte'] = vals.get("solde_compte_hide",False)
            logs.append(self.log(self.id,acteurName,str(self.solde_compte),str(vals.get("solde_compte_hide",False)),"Solde non affecte"))

        if vals.get("email",False):
            logs.append(self.log(self.id,acteurName,self.email,vals.get("email",False),"Email"))

        if vals.get("mobile",False):
            logs.append(self.log(self.id,acteurName,self.mobile,vals.get("mobile",False),"Mobile"))

        if logs:
            vals['log_ids'] = logs
        if vals.get("solde_compte_hide",False):
            solde_compte_hide =  vals.get("solde_compte_hide")
            if float(self.solde_compte) > float(solde_compte_hide):
                res = self.env['benin_petro.historique'].create({
                    'type_op':'Recharge carte',
                    'client_id':self.id,
                    'type_af':'sublime carte',
                    'debit':abs(float(self.solde_compte)-float(solde_compte_hide)),
                    'credit':0,
                    'solde_carte':solde_compte_hide,
                })


        return super(res_partner, self).write(vals)


    def log(self,ObjtId,acteurName,old_version,new_version,champ):
        return (0,0, {
            "client_id" : ObjtId,
            "acteur_name" : acteurName,
            "old_version" : old_version,
            "new_version" : new_version,
            "champ" : champ,
        })


    def create_users_to_clients(self):
        data = []
        partners = self.env['res.partner'].search([])
        for p in partners:
            # print p.email
            # print '----------------------------------------------------------------'
            # print p
            user_p = self.env['res.users'].search([('partner_id','=',p.id)])
            # print len(user_p)
            if len(user_p) == 0 and p.id != 1:
                res = self.env["res.users"].search([('login',"=",p.mobile)])
                if not res.id:
                    cl = self.env["res.users"].create({
                        'display_name':p.name,
                        'password':p.password,
                        'company_id':p.company_id.id,
                        'name':p.name,
                        'signup_token':p.email,
                        'partner_id':p.id,
                        'email':p.email,
                        'owner_id':False,
                        "login":p.mobile,
                        'active':True,
                        'share':False,
                        'groups_id': [( 4, self.env.ref('benin_petro.group_benin_petro_client').id),(4, self.env.ref('base.group_user').id)]
                    })
                    # print cl
                    p.write({
                        'access':cl.id
                    })
                else:
                    if res.partner_id.name not in data:
                        data.append(res.partner_id.name)
        # print 'dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        # print data
        return True




