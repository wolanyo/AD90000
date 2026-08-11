from odoo import api, fields, models
from lxml import etree
class Achat_order(models.Model):
    _inherit = 'purchase.order'


    @api.model
    def create(self, vals):

        print 'ordeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer'
        print vals
        return super(Achat_order, self).create(vals)


class Facture_for(models.Model):
    _inherit = 'account.invoice'
    # @api.one
    # def getTransfertDomain(self):
    #     print 'hiiiiiidfidiffififidiiiddddddddddddddddddddddddddddd'
    #     print '---------'
    #     location = self.env['stock.location'].search([('name','=','non-d')]).id
    #     transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #     print location
    #     print transferts
    #     data = [tr.id for tr in transferts]
    #     print data
    #     return data
    
    # @api.model
    # def default_get(self,fields):
    #     res =  super(Facture_for, self).default_get(fields)
    #     print 'hiiiiiidfidiffififidiiiddddddddddddddddddddddddddddd'
    #     location = self.env['stock.location'].search([('name','=','non-d')]).id
    #     transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #     data = [(4,tr.id) for tr in transferts]
    #     data_ids =  [ tr.id for tr in transferts]
    #     print transferts
    #     print location
    #     res['transfert_idss']=data
    #     print data
    #     return res
    
    # def getTransferts(self):
    #     location = self.env['stock.location'].search([('name','=','non-d')]).id
    #     transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #     data = [(4,tr.id) for tr in transferts]
    #     data_ids = [tr.id for tr in transferts]
    #     print '======'
    #     print self.transfert_idss.ids
    #     return [('id','in',self.transfert_idss)]

    # transfert_idss = fields.One2many('benin_petro.transfert',inverse_name='fact_idd',string='transferts')
    transfert_id = fields.Many2one(comodel_name='benin_petro.transfert', string='Transfert')
    # @api.one
    # @api.depends('transfert_idss')
    # def _getTren(self):
    #     location = self.env['stock.location'].search([('name','=','non-d')]).id
    #     transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #     data = [(4,tr.id) for tr in transferts]
    #     data_ids = [tr.id for tr in transferts]
    #     self.transfert_idss=[(6,False,data_ids)]
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(Facture_for, self).fields_view_get(view_id=view_id, view_type=view_type,toolbar=toolbar, submenu=submenu)
    #     if view_type == 'form':
    #         doc = etree.XML(res['arch'])
    #         nodes = doc.xpath("//field[@name='transfert_id']")
    #         location = self.env['stock.location'].search([('name','=','non-d')]).id
    #         transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #         data = [(4,tr.id) for tr in transferts]
    #         data_ids =  [tr.id for tr in transferts]
    #         d = '['
    #         for i in data_ids:
    #             d+=str(i)+','
    #         d+=']'
    #         for node in nodes:
    #             node.set('domain', "[('id', 'in',"+d+")]")
    #         res['arch'] = etree.tostring(doc)
    #     return res
    @api.model
    def create(self, vals):
        transfert = self.env['benin_petro.transfert'].search([('id','=',vals.get('transfert_id',False))])
        print transfert
        transfert.write({
            'is_done':'done'
        })
        print 'ordeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer'
        print vals
        return super(Facture_for, self).create(vals)
    # @api.onchange('id')
    # def _onchange_id(self):
    #     print '-----------------------'
    #     location = self.env['stock.location'].search([('name','=','non-d')]).id
    #     transferts = self.env['benin_petro.transfert'].search(['&',('location_id','=',location),('is_done','=',False)])
    #     data_ids =  [tr.id for tr in transferts]
    #     return {'domain':{'transfert_id':[('id', 'in',data_ids)]}}
        
