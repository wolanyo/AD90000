# -- coding: utf-8 --
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Versement(models.Model):
    _name = 'benin_petro.versement'
    _description = 'New Description'
    _order="create_date desc"

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
        montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',self.moyen_de_paiement),('verse_validate','=',False)])
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
        self.montant=self._montant()     
        
    
    tresorier_acc = fields.Integer(string='zeze',compute='_tresorier_read')
    vers_par = fields.Selection(string='Type de virement',default='caissier',required=True, selection=[('gerant', 'Gérant'), ('caissier', 'Caissier'),])
    num_versement = fields.Char(string='Numero de versement')
    point_vente_id = fields.Many2one("benin_petro.point.vente",string="Point de vente")
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal des règlements',required=True)  
    montant = fields.Float(string='Montant',required=True,default=_montant)
    type_versement=fields.Selection([('Lubrifiants','Lubrifiants'),('Produits blancs','Produits blancs'),('Gaz et accessoire','Gaz et accessoire'),('Lavage','Lavage')],string="Catégorie des produits")
    state = fields.Selection(string='Etat', selection=[('brouillon', 'Brouillon'), ('valide', 'Validé')],default='brouillon')
    access=fields.Many2one(comodel_name='res.users')
    moyen_de_paiement = fields.Selection(string='Moyen de paiement',default='cheque',selection=[('cheque', 'Chèque'), ('especes', 'Espèces'),('versement','Versement')])

    @api.model
    def create(self, vals):
        print vals
        print 'creaaatehhhhh'
        if vals['vers_par']=='caissier':
            montant_correct=0
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.env.user.id)])
            montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',vals['moyen_de_paiement']),('verse_validate','=',False)])
            print montants_verse
            for m in montants_verse:                
                montant_correct+=m.diff
            print montant_correct
            vals['montant']=montant_correct
            print vals['montant']
            print '-----------*-* 5 *-*----------'
            if vals['montant'] <=0:
                raise ValidationError("Le montant doit être supérieur à zéro")
            else :
                vals ['access']=self.env.user.id
                # p.montant=montant_correct                
                return super(Versement, self).create(vals)
        else :
                vals ['access']=self.env.user.id
                p= super(Versement, self).create(vals)                
                return p
    
    @api.multi
    def write(self, values):
        if  self.state !='valide':
            if 'state' in values.keys():
                return super(Versement, self).write(values)
            if self.vers_par=='caissier':
                if 'moyen_de_paiement' in values.keys():
                    po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.access.id)])
                    montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',values['moyen_de_paiement']),('verse_validate','=',False)])
                    montant_correct=0
                    for m in montants_verse:
                        montant_correct+=m.diff
                    if montant_correct >0:
                        values['montant']=montant_correct
                    else :
                        raise ValidationError("Le montant doit être supérieur à zéro ")
            return super(Versement, self).write(values)    
        else :
            raise ValidationError("Vous ne pouvez pas modifier un versement  déjà validé")

    #             if 'moyen_de_paiement' in values.keys():
    #                 montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',values['moyen_de_paiement']),('verse_validate','=',False)])
    #             # elif 'montant' in values:
    #             #     montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',self.moyen_de_paiement),('verse_validate','=',False)])

    #             else :
    #                 montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',self.moyen_de_paiement),('verse_validate','=',False)])
    #                 print montants_verse
    #                 print '222222222222'
    #             montant_correct=0
    #             for m in montants_verse:
    #                 montant_correct+=m.diff
    #             values['montant']=montant_correct
    #             if values['montant'] <=0:
    #                 raise ValidationError("Le montant doit être supérieur à zéro aaaaaaaaaaa")                    
    #             else :
    #                 return super(Versement, self).write(values)
                    
    #     else : 
    #         raise ValidationError("Vous ne pouvez pas modifier un versement  déjà validé")

   


    @api.one
    def valider_versement(self):
        print 'uuuuuuuuuuuuuuuuuuu'
        aze= self.env["benin_petro.historique"].search([('verse_validate','=',False)])
        print aze
        print 'jjjjjjjjjjjjjjjj'
        if self.vers_par=='caissier':                                 
            print self.access.id
            po=self.env["benin_petro.sous_chargeur"].search([('access','=',self.access.id)])                 
            print po.id            
            montants_verse=self.env["benin_petro.historique"].search([('sous_chargeur','=',po.id),('moyen_de_paiement','=',self.moyen_de_paiement),('verse_validate','=',False)])
            print 'VAAAAAAAAAAAAAAALIDER'
            montant_correct=0
            print 'VAAAAAAAAAAAAAAALIDER'
            print montants_verse
            for m in montants_verse:
                print m.diff
                montant_correct+=m.diff
                print 'hhhhhhhhhh'
            print self.montant
            print '================'
            print montant_correct
            if montant_correct==self.montant:
                self.write({
                'state':'valide'
                })
                for m in montants_verse:
                    m.write({
                        'verse_validate':True
                    })
            else :
                raise ValidationError("Le montant indiqué n'est pas correct") 
        else :
            self.write({
                'state':'valide'
                })


        
        

    