# -*- coding: utf-8 -*-
from odoo import api, fields, models
from random import randint

class Ticket_valeur(models.Model):
    _name = 'benin_petro.ticket_valeur'
    _rec_name='num_serie'
    _order = 'create_date desc'

    def _default_serie(self):
	result = True
	serie_proposition = 0
        while result==True:
            serie_proposition = str(randint(111, 999)) + str(randint(111, 999)) + str(randint(111, 999)) + str(randint(111, 999))
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
    tv_type = fields.Many2one('benin_petro.tv_type',string='Coupure')
    client = fields.Many2one('res.partner',string='Client')
    etat = fields.Selection([('util','Utilisé'),('nonutil','Non utilisé')],default='nonutil')
    qrcode = fields.Char(string="dddd")
    num_serie = fields.Char(string=u'Numéro de serie')
    print_hestory_id = fields.Many2one('tv_print_hestory',string='hestory')
    print_id = fields.Many2one('benin_petro.tv_print',string='tv print')
    remise = fields.Many2one('benin_petro.tv_remise',string='Remise')
    num_serie_incr = fields.Char(string=u'Numéro séquentiel')
    num_incr = fields.Char(string=u'Numéro séquentiel')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    consom = fields.Many2one('benin_petro.carte.consommation',string='Ticket')
    recus = fields.Selection([('Ticket','Ticket'),('Recus','Reçus d\'avoir')],default='Ticket')
    montant_recus = fields.Integer(string='Montant')
    qrcode_img = fields.Binary('Qrcode image', readonly=True)
    point_vente = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    imported_state = fields.Boolean(string="Imported")


    @api.model
    def create(self, vals):
        if not vals.get('num_serie',False):
            vals['num_serie'] = self._default_serie()
            qrcode = self._getQrCode(str(vals.get("num_serie"))+'<:>AKAD<:>'+str(vals.get("date_expiration")))
            if qrcode=="":
                raise ValidationError(_("Merci de contacter le prestataire pour la génération du QRCODE"))
            if 'qrcode' not in vals:
                vals['qrcode'] = qrcode
            vals['etat']='nonutil'
            last_num_serie = self.search([('tv_type','=',vals.get('tv_type',False)),('imported_state','=',False)],order='id desc')
            rec = 0
            if last_num_serie:
                if str(last_num_serie[0].num_incr) == '':
                    rec = 0
                else:
                    rec = last_num_serie[0].num_incr
            else:
                rec = 0   
            pStart = 1 #adjust start value, if req'd 
            pInterval = 1 #adjust interval value, if req'd
            if (rec == 0): 
                rec = pStart 
            else: 
                rec = int(rec) + pInterval 

            vals['num_serie_incr'] = str(rec).zfill(10)
            vals['num_incr'] = rec

        
        return super(Ticket_valeur, self).create(vals)
    
