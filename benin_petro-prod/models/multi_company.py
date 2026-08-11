# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError


class product_product(models.Model):
    _inherit = 'product.product'

    company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)
    


# class pos(models.Model):
#     _inherit = 'benin_petro.point.vente'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)
    


#     @api.model
#     def create(self, values):
#         print 'creaaaaaaaate'
#         p= super(pos, self).create(values)
#         print p.company_id
#         return p

# class carte(models.Model):
#     _inherit = 'benin_petro.carte'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class carte_consommation(models.Model):
#     _inherit = 'benin_petro.customer'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)
# class transfert(models.Model):
#     _inherit = 'benin_petro.transfert'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class transfert(models.Model):
#     _inherit = 'benin_petro.chargeur'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class transfert(models.Model):
#     _inherit = 'benin_petro.sous_chargeur'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class carte_consommation(models.Model):
#     _inherit = 'benin_petro.carte.consommation'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class tv_print(models.Model):
#     _inherit = 'benin_petro.tv_print'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)


# class type_carte(models.Model):
#     _inherit = 'benin_petro.type.carte'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# # class ticket_valeur(models.Model):
# #     _inherit = 'benin_petro.ticket_valeur'

# #     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class tv_type(models.Model):
#     _inherit = 'benin_petro.tv_type'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class agent(models.Model):
#     _inherit = 'benin_petro.agent'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class partner(models.Model):
#     _inherit = 'res.partner'

#     def test(self):
#         print 'methoooooooood'
#         """a=self.env["res.partner"].sudo().search([])
#         a.write({
#             'company_id':1
#         })
#         b=self.env["product.product"].sudo().search([])
#         b.write({
#             'company_id':1
#         })
#         b=self.env["benin_petro.point.vente"].sudo().search([])
#         b.write({
#             'company_id':1
#         })
#         b=self.env["benin_petro.carte"].sudo().search([])
#         b.write({
#             'company_id':1
#         })
#         b=self.env["benin_petro.agent"].sudo().search([])
#         b.write({
#             'company_id':1
#         })"""
#         b=self.env["product.product"].sudo().search([])
#         b.write({
#             'company_ids':[(6, 0, [1,5])]
#         })

# class productCategorie(models.Model):
#     _inherit = 'product.category'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class productTemplate(models.Model):
#     _inherit = 'product.template'   

#     @api.onchange('company_id','type')
#     def _getCateg(self):
#         res = {}
#         ids = []
#         user=self.env["res.users"].search([('id','=',self.env.user.id)])
#         print '----------------    1'
#         print user
#         comp_id= user.company_id
#         cat=self.env["product.category"].search([])
#         for c in cat:
#             if c.company_id == comp_id:  
#                 print 'jjj'                 
#                 ids.append(c.id)
#         res['domain'] = {'categ_id': [('id', 'in', ids)]}
#         return res 

# class productProduct(models.Model):
#     _inherit = 'product.product'   

#     @api.onchange('company_id','type')
#     def _getCategorie(self):
#         res = {}
#         ids = []
#         user=self.env["res.users"].search([('id','=',self.env.user.id)])
#         print '----------------    1'
#         print user
#         comp_id= user.company_id
#         cat=self.env["product.category"].search([])
#         for c in cat:
#             if c.company_id== comp_id:  
#                 print 'jjj'              
#                 ids.append(c.id)
#         res['domain'] = {'categ_id': [('id', 'in', ids)]}
#         return res

# class Vehicle(models.Model):
#     _inherit = 'fleet.vehicle'
#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class Historique(models.Model):
#     _inherit = 'benin_petro.historique'
#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

# class Versement(models.Model):
#     _inherit = 'benin_petro.versement'
#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)


# class ResCompany(models.Model):
#     _inherit = 'res.company'

#     entete = fields.Binary(string='')
#     pied = fields.Binary(string='')
#     picking_type = fields.Many2one(comodel_name='stock.picking.type', string='Type de préparation ')

# class PosSession(models.Model):
#     _inherit = 'pos.session'

#     company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda  s : s.env["res.users"].sudo().search([('id','=',s.env.user.id)]).company_id)

