# -- coding: utf-8 --
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime




class VersementLine(models.Model):
    _name = 'benin_petro.versement_line'

    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)  
    num_versement = fields.Char(string='Numéro de versement',required=True)
    versement_id = fields.Many2one(comodel_name='benin_petro.versement', string='Versement')  
    montant=fields.Float(string='Montant',required=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )
    

class Versement(models.Model):
    _name = 'benin_petro.versement'
    _description = 'New Description'
    _order="create_date desc"

    versement_line=fields.One2many(comodel_name='benin_petro.versement_line', inverse_name='versement_id', string='Lignes de versement')
    # @api.one
    @api.depends('tresorier_acc')
    def _tresorier_read(self):
		print 'lllllllllllllllllllllllllllllllllllllll'
		if self.env.user.has_group('benin_petro.group_benin_petro_sous_chargeur'):
			self.tresorier_acc= 1
		else :
			self.tresorier_acc= 0
    
    def _montant(self):
        if self.env.user.has_group('benin_petro.group_benin_petro_sous_chargeur'):
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)])
        else :
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.access.id)])       
        montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',self.moyen_de_paiement),('verse_validate','=',False),('tres_validate','=',False)])
        montant_correct=0
        print montant_correct
        for m in montants_verse:
            montant_correct+=m.diff
        return montant_correct
    
    @api.onchange('moyen_de_paiement')
    def _onchange_moyen_de_paiement(self):
        print 'ooooooooon change'
        print self._montant()
        print '555555555555555'
        if self.moyen_de_paiement:
            self.montant=self._montant()   
          
    @api.depends('versement_line','montant')   
    def _get_montant(self):
        montant =self._montant()
        print 'lllllllllppp'
        print montant
        somme=0
        for a in self.versement_line:
            somme+=a.montant
        print montant-somme
        self.montant_saisie= montant-somme

    @api.constrains('versement_line')
    def versement(self):
        somme =0
        for a in self.versement_line:
            somme +=a.montant
        if somme > self.montant:
            raise ValidationError('Le montant versé ne doit pas etre supérieur au montant calculé')

    tresorier_acc = fields.Integer(string='zeze',compute='_tresorier_read')
    vers_par = fields.Selection(string='Type de virement',default='agent_monetique',required=True, selection=[('gerant', 'Gérant'), ('agent_monetique', 'Agent monétique'),])
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    # journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)  
    # num_versement = fields.Char(string='Numero de versement')

    montant = fields.Float(string='Montant Total',required=True,default=_montant)
    type_versement=fields.Selection([('Lubrifiants','Lubrifiants'),('Produits blancs','Produits blancs'),('Gaz et accessoire','Gaz et accessoire'),('Lavage','Lavage')],string="Catégorie des produits")
    state = fields.Selection(string='Etat', selection=[('annule', 'Annulé'),('brouillon', 'Brouillon'), ('valide', 'Validé')],default='brouillon')
    access=fields.Many2one(comodel_name='res.users')
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',default='especes',selection=[('cheque', 'Chèque'), ('especes', 'Espèces')])
    liste_payment=fields.One2many(comodel_name='benin_petro.historique', inverse_name='versement_id', string='Recharges')

    montant_saisie = fields.Float(string='Montant Manquant',compute='_get_montant',store=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    



    @api.model
    def create(self, vals):
        print 'creaaatehhhhh'
        if vals['vers_par']=='agent_monetique':
            montant_correct=0
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)])
            montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',vals['moyen_de_paiement']),('verse_validate','=',False),('tres_validate','=',False)])
            print montants_verse
            for m in montants_verse:                
                montant_correct+=m.diff         
            vals['montant']=montant_correct
            print '-----------*-* 5 *-*----------'
            if vals['montant'] <=0:
                raise ValidationError("Le montant doit être supérieur à zéro")
            else :
                vals ['access']=self.env.user.id
                vals['liste_payment']=montants_verse
                a= super(Versement, self).create(vals)
                for m in montants_verse:  
                    m.sudo().write({
                        'verse_validate':True,
                        'versement_id':a.id
                    })                
                self.write({
                    'liste_payment':montants_verse
                })
                return a
        else :
                vals ['access']=self.env.user.id
                p= super(Versement, self).create(vals)                
                return p
    
    @api.one
    def valider_versement(self):
        print 'jjjjjjjjjjjjjjjj'
        if self.vers_par=='agent_monetique':                                 
            for m in self.liste_payment:
                print m
                print m.tres_validate
                m.sudo().write({
                    'tres_validate':True
                }) 
				
        if self.moyen_de_paiement == 'versement':
            acount_id_d = 19857
            account_id_c = 20607
            for m in self.versement_line:
                data = [(0,0 ,{'account_id':account_id_d ,'partner_id':'','name':'Versement à la banque','debit':m.montant-50}),
                (0,0 ,{'account_id':account_id_c,'partner_id':'','name':'Versement à la banque','credit':m.montant})]
                av= self.env['account.move'].create({
                'journal_id':m.journal_id.id,
                'date':datetime.datetime.now().date(),
                'ref': 'sssss-'+str(datetime.datetime.now()),

                'line_ids':data
                })  
                av.post()             

        if self.moyen_de_paiement == 'cheque':
            account_id_d = 19857
            account_id_c = 19975
            for m in self.versement_line:
                data = [(0,0 ,{'account_id':account_id_d ,'partner_id':'','name':'Versement à la banque','debit':m.montant}),
                (0,0 ,{'account_id':account_id_c,'partner_id':'','name':'Versement à la banque','credit':m.montant})]
                av= self.env['account.move'].create({
                'journal_id':m.journal_id.id,
                'date':datetime.datetime.now().date(),
                'ref': 'sssss-'+str(datetime.datetime.now()),
                
                'line_ids':data
                })  
                av.post()             

        if self.moyen_de_paiement == 'especes':
            account_id_d = 19857
            account_id_c = 20607
            for m in self.versement_line:
                data = [(0,0 ,{'account_id':account_id_d ,'partner_id':'','name':'Versement à la banque','debit':m.montant-50}),
                (0,0 ,{'account_id':20143,'partner_id':'','name':'Frais de timbre','debit':50}),
                (0,0 ,{'account_id':account_id_c,'partner_id':'','name':'Versement à la banque','credit':m.montant})]
                av= self.env['account.move'].create({
                'journal_id':m.journal_id.id,
                'date':datetime.datetime.now().date(),
                'ref': 'sssss-'+str(datetime.datetime.now()),
                
                'line_ids':data
                })  
                av.post()             
        self.sudo().write({
            'state':'valide'
            })
        

    @api.one
    def annuler(self):
        print 'Anuuuuuuler'
        for m in self.liste_payment:
            print m
            print m.tres_validate
            m.sudo().write({
                    'verse_validate':False,
                    'versement_id':False
            })
        self.sudo().write({
            'state':'annule',
            'liste_payment':False
            })

    