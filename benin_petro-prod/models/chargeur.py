# -*- coding: utf-8 -*-
from odoo import fields, models,api

class chargeur(models.Model):

    _name="benin_petro.chargeur"
    _rec_name='access'

    montant_plafond = fields.Float(string='Montant plafond')
    rest=fields.Float(string='Montant actuel')
    sous_chargeur = fields.One2many("benin_petro.sous_chargeur","superv",string="Les caissiers")
    access = fields.Many2one("res.users",string="Trésorier",required=True)
    historique = fields.One2many(comodel_name='benin_petro.historique', inverse_name='chargeur', string='Historique')
    historique_tv = fields.One2many(comodel_name='benin_petro.historique', inverse_name='chargeur_tv', string='Historique',domain=[('type_af','=','TV')])
    historique_sublim = fields.One2many(comodel_name='benin_petro.historique', inverse_name='chargeur_sublim', string='Historique',domain=[('type_af','=','sublime carte')])
    montant_plafond_tv = fields.Float(string='Montant plafond')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )


    @api.onchange('access')
    def _getCharger(self):
     res = {}
     ids = []
     chargeur=self.env["benin_petro.chargeur"].search([])
     for c in chargeur:
         ids.append(c.access.id)
     res['domain'] = {'access': [('id', 'not in', ids),('groups_id','=',self.env.ref('benin_petro.group_benin_petro_chargeur').id)]}
     print res
     return res

    @api.model
    def create(self, vals):
     vals['rest']=vals['montant_plafond']
     p = super(chargeur, self).create(vals)
     self.env['benin_petro.historique'].create({
        'montant_init':self.montant_plafond,
        'montant_fin':self.montant_plafond+vals['montant_plafond'],
        'chargeur':p.id,
        'type_op':'Approvisionnement',
        'type_af':'sublime carte',
        'diff':abs(p.montant_plafond-p.montant_plafond-vals['montant_plafond']),
        'debit':0,
        'credit':abs(p.montant_plafond-p.montant_plafond-vals['montant_plafond'])
        })
     self.env['benin_petro.historique'].create({
            'montant_init':self.montant_plafond_tv,
            'montant_fin':self.montant_plafond_tv+vals['montant_plafond_tv'],
            'chargeur':p.id,
            'type_op':'Approvisionnement',
            'type_af':'TV',
            'diff':abs(p.montant_plafond_tv-p.montant_plafond_tv-vals['montant_plafond_tv']),
            'debit':0,
            'credit':abs(p.montant_plafond_tv-p.montant_plafond_tv-vals['montant_plafond_tv'])
                    
                })
    #  chargeur_group = self.env.ref('benin_petro.group_benin_petro_chargeur')
    #  chargeur_group.write({'users': [(4, vals['access'])]})    
     return p

    @api.multi
    def write(self,vals):
        print ' whriteeeeeeeeeeeeeeee,'
        print vals
        po=self.env["benin_petro.sous_chargeur"].search([('superv','=',self.id)])
        cl=super(chargeur,self).write(vals)
        if 'montant_plafond' in vals.keys():
            po.write({
                'montant_super':vals['montant_plafond']
            })
            print 'UPDATED ------------------->>'
        if 'montant_plafond_tv' in vals.keys():
            po.write({
                'montant_super_tv':vals['montant_plafond_tv']
            })
            print 'UPDATED TV ------------------->>'    
        return cl
	
    # @api.multi
    # def write(self,vals):
    #     print ' whriteeeeeeeeeeeeeeee,'
    #     print vals
        
    #     return super(chargeur,self).write(vals)

	#  cl = self.env["res.users"].create({
	# 			'display_name':vals.get('name'),
	# 			'password':1111,
	# 			'name':vals['name'],
	# 			'signup_token':vals.get('email'),
	# 			'email':vals.get('email'),
	# 			'owner_id':False,
	# 			"login":vals.get('email'),
	# 			'active':True,
	# 			'share':False
	# 	})
	#  p.write({

	# 	'access':cl.id
		
	#      })
	#  print cl.id
	#  print 'HHHHHHHHHHHHHHHHHHHHuuu'
	#  print p.id
	




