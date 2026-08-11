# -*- coding: utf-8 -*-

from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime


class   bon_commande(models.Model):
    _inherit = "sale.order"

    # stock = fields.Many2one(comodel_name='stock.location', string='Emplacement',required=True)
    transfert = fields.Many2one(comodel_name='benin_petro.transfert')
    tax_tva = fields.Float(string='TVA',compute="_calc_taxes")
    tax_ts = fields.Float(string='TVA',compute="_calc_taxes")

    def _calc_taxes(self):
        for order in self:
            tva = 0
            ts = 0
            for line in order.order_line:
                if line.product_id.id==155:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - ESSENCE')]).amount
                    ts_l= self.env['account.tax'].search([('name','=','TS - ESSENCE')]).amount
                elif  line.product_id.id==156:
                    tva_l= self.env['account.tax'].search([('name','=','TVA - GASOIL')]).amount
                    ts_l= self.env['account.tax'].search([('name','=','TS - GASOIL')]).amount
                elif  line.product_id.id==164:
                    tva_l= self.env['account.tax'].search([('name','=','TVA-PETROLE')]).amount
                    tva_l= self.env['account.tax'].search([('name','=','Ts-PETROLE')]).amount
                else:
                    continue
                tva += tva_l * line.product_uom_qty
                ts += ts_l * line.product_uom_qty
            order.sudo().update({
                'tax_tva':tva,
                'tax_ts':ts
            })

    @api.multi
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        print 'hello'
        action = self.env.ref('benin_petro.stock_transfer_action').read()[0]
        print action

       
        action['views'] = [(self.env.ref('benin_petro.stock_transfer_view_form').id, 'form')]
        action['res_id'] = self.transfert.id
        print action 
        return action
    
    def action_confirm(self) :
        data=[]
        p= super(bon_commande,self).action_confirm()
        print self.order_line
        source=0
        destinations=0
        location_id=0
        location_id_for_view=0
        location_dest_id=0
        client=0
        # stock_picking_id=0
        # for tr in self.picking_ids:
        #     stock_picking_id=tr.stock_picking_id
        #     break
        for tr in self.picking_ids:
            source=tr.location_id.id
            destinations=tr.location_dest_id.id
            location_id_for_view=tr.location_id.id
            location_id=tr.location_id.id
            location_dest_id=tr.location_dest_id.id
            client=tr.partner_id.id
        # if len(self.picking_ids) == 1 :
        for tr in self.picking_ids:
            print tr
            tr.write({
                'boolTest':True
            })
                     
                # print 'iohnjhiihoioioiojiojo'
                # print tr.move_lines
                # for a in  tr.move_lines:
                #     print a
                #     data.append((0,0 ,{'product_id':a.product_id.id,'qty':a.product_uom_qty,'source':source,
                #     'destinations':destinations,'location_id_for_view':location_id_for_view,'booltest':True}))
        ids={}
        data=[]
        
        for tr in self.picking_ids:
            for a in  tr.move_lines:
                if a.product_id.id not in ids:
                    ids[a.product_id.id]=a.product_uom_qty
                else :
                    ids[a.product_id.id]+=a.product_uom_qty
        for key,value in ids.iteritems():
            data.append((0,0 ,{'product_id':key,'qty':value,'source':source,
                    'destinations':destinations,'location_id_for_view':location_id_for_view,'booltest':True}))
           
        # else :
        #     ids={}
        #     data=[]
        #     for tr in self.picking_ids:
        #         for a in  tr.move_lines:
        #             if tr.product_id.id not in ids:
        #                 ids[a.product_id.id]=a.product_uom_qty
        #             else :
        #                 ids[a.product_id.id]+=a.product_uom_qty
        #     for key,value in ids.iteritems():
        #         data.append((0,0 ,{'product_id':key,'qty':value,'source':source,
        #                 'destinations':destinations,'location_id_for_view':location_id_for_view,'booltest':True}))
        av= self.env['benin_petro.transfert'].create({
                    'typeDesProuduit':'autre',
                    'transfer_type':'d',
                    'Date_prevue':datetime.datetime.now().date(),
                    'location_id':location_id,
                    'move_lines':data,
                    'location_dest_depot_id':location_dest_id,
                    'client':client,
                    # 'stock_picking_id':stock_picking_id,
                    'states':'test',
                    'commande_id':self.id
                        })    
        self.transfert=av.id 
        self.delivery_count=1
        print self.transfert
        print  av.commande_id  
        for tr in self.picking_ids:
            for f in tr.pack_operation_ids:
                f.unlink()
            tr.unlink()
            print 'deleeeeete'
         
        return p
         
    @api.model
    def create(self, vals):
        print 'oooooooooooorder'
        print vals
        # flag=1
        # print 'VAAAAAAAAAAAAALS bon' de commande'
        # print vals
        # for val in  vals['order_line']:
        #     product_id= val[2]['product_id']
        #     print product_id
        #     qte_demande=val[2]['product_uom_qty']
        #     print qte_demande
        #     qte=0
        #     qte_dispo=self.env["stock.quant"].search([('location_id','=',vals['stock']),('product_id','=',product_id)])
        #     for q in qte_dispo:
        #         qte+=q.qty
        #     print 'qte dispo'
        #     print qte
        #     if qte_demande > qte:
        #         flag=0
        # if flag==1:
        #     return super(bon_commande, self).create(vals)
        # else :
        #     raise ValidationError("La quantité disponible dans l\'emplacement demandé est supérieure à la quantité disponible veuillez la vérifier  ")
        
        d= super(bon_commande, self).create(vals)
        # a=self.env["stock.picking"].search([('origin','=',d.origin)])
        # print 'sele order print'
        # print a
        # print d.partner_id.id
        # a.write({
        #     'boolTest':True,
        #     'partner_id':d.partner_id.id,
            
        #     })
        # print 'ffffffff'
        # print a.sale_id
        # print a.boolTest
        # print 'boool affect'
        return d
  
    # @api.constrains('stock','order_line')
    # def qte_check(self):
    #     flag=1
    #     print 'VAAAAAAAAAAAAALS bon de commande'
    #     for val in  self.order_line:
    #         print val
    #         product_id= val.product_id.id
    #         print product_id
    #         qte_demande=val.product_uom_qty
    #         print qte_demande
    #         qte=0
    #         qte_dispo=self.env["stock.quant"].search([('location_id','=',self.stock.id),('product_id','=',product_id)])
    #         for q in qte_dispo:
    #             qte+=q.qty
    #         print 'qte dispo'
    #         print qte
    #         if qte_demande > qte:
    #             flag=0
    #     if flag==0:
    #         raise ValidationError("La quantité disponible dans l\'emplacement demandé est supérieure à la quantité disponible veuillez la vérifier  ")
             

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    boolTest = fields.Boolean(default=False)
    client_id=fields.Many2one(comodel_name='res.partner', string='Client')
    
    @api.model
    def create(self,vals):
        print 'PIIIIIIIIIIIICKING'
        print vals
        data=[]
        vals['image1'] = 'iVBORw0KGgoAAAANSUhEUgAAAK0AAABqCAIAAABBIEYYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIISURBVHhe7djBjQJBFAPRyT/pBg5IaARUAH579cnlEtN/r+MPgXMuEBB4EuABDV4EeMADHnDgTcDvARf8HnDA7wEHPgn4LvDBd4EDvgsc8F3gwJ2A9wEnvA844H3AAe8DDngfcOAbAe9EXngncsA7kQPeiRzwTuSAdyIHfhFwL3DDvcAB9wIH3AsccC9wwL3AAfcCB/4RcDfyw93IAXcjB9yNHHA3csDdyAF3IwfcjRwoAv5/UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwtHzVfG6U/pf1sAAAAAElFTkSuQmCC'
        vals['image2'] = 'iVBORw0KGgoAAAANSUhEUgAAAK0AAABqCAIAAABBIEYYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIISURBVHhe7djBjQJBFAPRyT/pBg5IaARUAH579cnlEtN/r+MPgXMuEBB4EuABDV4EeMADHnDgTcDvARf8HnDA7wEHPgn4LvDBd4EDvgsc8F3gwJ2A9wEnvA844H3AAe8DDngfcOAbAe9EXngncsA7kQPeiRzwTuSAdyIHfhFwL3DDvcAB9wIH3AsccC9wwL3AAfcCB/4RcDfyw93IAXcjB9yNHHA3csDdyAF3IwfcjRwoAv5/UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwteVCENnIebOxcLXlQhDZyHmzsXC15UIQ2ch5s7FwtHzVfG6U/pf1sAAAAAElFTkSuQmCC'
        return super(stock_picking, self).create(vals)
    
    # @api.multi
    # def write(self,vals):
    #     print 'PIIIIIIIIIIIICKING88888888888'
    #     print vals
    #     data=[]
    #     p=super(stock_picking, self).write(vals)
    #     #location_dest_id
    #     print 'KKKKKKKKKKK'
    #     print self.sale_id
    #     # print vals['order']
    #     print self.boolTest
    #     if 'boolTest' in vals:
    #         print 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
    #         if vals['boolTest']:
    #             print 'CRAAAAAATE trans'
    #             location_id=self.location_id
    #             # prod=self.env["stock.r"].search([('id','=',self.sale_id.id)]).order_line
    #             # test=self.env["sale.order.line"].search([('id','=',prod)])
    #             data=[]
    #             for a in  self.move_lines:
    #                 print a
    #                 data.append((0,0 ,{'product_id':a.product_id.id,'qty':a.product_uom_qty,'source':location_id.id,
    #                 'destinations':self.location_dest_id.id,'location_id_for_view':location_id.id,'booltest':True}))
    #             print 'said'
    #             # print self.sale_id.pack_operation_product_ids
    #             print self.partner_id
    #             av= self.env['benin_petro.transfert'].create({
    #                 'typeDesProuduit':'autre',
    #                 'transfer_type':'d',
    #                 'Date_prevue':datetime.datetime.now().date(),
    #                 'location_id':location_id.id,
    #                 'move_lines':data,
    #                 'location_dest_depot_id':self.location_dest_id.id,
    #                 'client':self.partner_id.id,
    #                 # 'stock_picking_id':self.id,
    #                 'states':'test'
    #                     })
    #             print '-----------------*'
    #     return p



class pos_order(models.Model):
    _inherit = 'pos.order'

    transaction_id = fields.Many2one(comodel_name='benin_petro.carte.consommation', string='Transaction')
    last_id = fields.Float("Last id")


"""
class pos_session(models.Model):
    _inherit = 'pos.session'

    def _confirm_orders(self):
	super(pos_session, self)
        for session in self:
	    print '555555555555555555555555'
            company_id = session.config_id.journal_id.company_id.id
            orders = session.order_ids.filtered(lambda order: order.state == 'paid')
	    print orders
            journal_id = self.env['ir.config_parameter'].sudo().get_param(
                'pos.closing.journal_id_%s' % company_id, default=session.config_id.journal_id.id)
	    print journal_id
	   
            if not journal_id:
                raise UserError(_("You have to set a Sale Journal for the POS:%s") % (session.config_id.name,))
	    print '111111111111111111'
            move = self.env['pos.order'].with_context(force_company=company_id)._create_account_move(session.start_at, session.name, int(journal_id), company_id)
            
	    orders.with_context(force_company=company_id)._create_account_move_line(session, move)
	    print '111111111111111111111'
            for order in session.order_ids.filtered(lambda o: o.state not in ['done', 'invoiced']):
                if order.state not in ('paid'):
                    raise UserError(_("You cannot confirm all orders of this session, because they have not the 'paid' status"))
                order.action_pos_order_done()
            
            orders_to_reconcile = session.order_ids.filtered(lambda order: order.state in ['invoiced', 'done'] and order.partner_id)
            orders_to_reconcile.sudo()._reconcile_payments()

    @api.multi
    def action_pos_session_close(self):
	super(pos_session, self)
	print '88888888888888888888888888'
        for session in self:
            company_id = session.config_id.company_id.id
            ctx = dict(self.env.context, force_company=company_id, company_id=company_id)
            for st in session.statement_ids:
                
                if (st.journal_id.type not in ['bank', 'cash']):
                    raise UserError(_("The type of the journal for your payment method should be bank or cash "))
                st.with_context(ctx).sudo().button_confirm_bank()
	print '9999999999999999999'
        self.with_context(ctx)._confirm_orders()
	
        self.write({'state': 'closed'})
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Sale Menu',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('point_of_sale.menu_point_root').id},
        }
"""

from odoo import fields, api, models,_

class   stock_scrap(models.Model):
    _inherit = "stock.scrap"


    scrap_location_id = fields.Many2one(
        'stock.location', 'Scrap Location',
        domain="[]", states={'done': [('readonly', True)]})


class OrderLine(models.Model):
    _inherit = "sale.order.line"

    product_prix_ht = fields.Float(string="Prix HT",compute='_calc_prix_ht')
    def _calc_prix_ht(self):
        for line in self:
            tva_l = 0
            ts_l =0
            if line.product_id.id==155:
                tva_l= self.env['account.tax'].search([('name','=','TVA - ESSENCE')]).amount
                ts_l= self.env['account.tax'].search([('name','=','TS - ESSENCE')]).amount
            elif  line.product_id.id==156:
                tva_l= self.env['account.tax'].search([('name','=','TVA - GASOIL')]).amount
                ts_l= self.env['account.tax'].search([('name','=','TS - GASOIL')]).amount
            elif  line.product_id.id==164:
                tva_l= self.env['account.tax'].search([('name','=','TVA - PETROLE')]).amount
                tva_l= self.env['account.tax'].search([('name','=','TS - PETROLE')]).amount
            print 55555555555555555555555555555
            print line.product_id.lst_price
            line.sudo().update({
                'product_prix_ht':line.product_id.lst_price - (tva_l + ts_l)
            })
