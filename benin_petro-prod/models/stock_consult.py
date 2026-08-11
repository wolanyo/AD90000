# -- coding: utf-8 --

from odoo import fields, api, models,_
from datetime import date
import locale
class StockConsult(models.Model):
    _name = 'benin_petro.stock_consult'
    date_s = fields.Date(string="Date")
    product_id = fields.Many2one('product.product',string="Produit")
    emplacement_id = fields.Many2one('stock.location',string="Emplacement")
    detail = fields.One2many('benin_petro.stock_consult_detail','stock_consult_id',string="Detail")
    @api.onchange('date_s','product_id','emplacement_id')
    def change_date_product(self):
        query =""
        print 'uyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        if self.product_id and self.date_s and self.emplacement_id :
            print self.date_s
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id and p.id ="""+str(self.product_id.id)+""" and DATE(s.create_date) <= '"""+self.date_s+"""' and l.id = """+str(self.emplacement_id.id)+""" group by pt.name, p.id , l.id ,l.complete_name """
        elif self.product_id and self.date_s :
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id and p.id ="""+str(self.product_id.id)+""" and DATE(s.create_date) <= '"""+self.date_s+"""'  group by pt.name, p.id , l.id ,l.complete_name """

        elif self.emplacement_id and self.date_s :
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id  and DATE(s.create_date) <= '"""+self.date_s+"""' and l.id = """+str(self.emplacement_id.id)+""" group by pt.name, p.id , l.id ,l.complete_name """
        elif self.emplacement_id and self.product_id :
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id and p.id ="""+str(self.product_id.id)+"""  and l.id = """+str(self.emplacement_id.id)+""" group by pt.name, p.id , l.id ,l.complete_name """
        
        elif self.emplacement_id :
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id   and l.id = """+str(self.emplacement_id.id)+""" group by pt.name, p.id , l.id ,l.complete_name """
        elif self.product_id :
            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id and p.id ="""+str(self.product_id.id)+"""  group by pt.name, p.id , l.id ,l.complete_name """
        elif self.date_s:

            query = """select pt.name, sum(s.qty),l.complete_name,p.id from stock_quant s,stock_location l,product_product p,product_template pt
                    where s.location_id = l.id and p.id = s.product_id and p.product_tmpl_id = pt.id and DATE(s.create_date) <= '"""+self.date_s+"""'  group by pt.name, p.id , l.id ,l.complete_name """
        
        if query :
            self._cr.execute(query)
            data =  self._cr.fetchall()
            print data    
            return {'value':{'detail':[(0,0,{'emplacment_name':row[2],'qty':row[1]}) for row in data]}}
class StockConsultDetail(models.Model):
    _name = 'benin_petro.stock_consult_detail'
    emplacment_name = fields.Char(string="Emplacement")
    qty = fields.Char(string="Qty")
    stock_consult_id = fields.Many2one('benin_petro.stock_consult',string="consult")