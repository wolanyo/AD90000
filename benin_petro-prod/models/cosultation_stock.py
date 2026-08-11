from odoo import api, fields, models


class Consulte(models.Model):
    _name = 'benin_petro.consulte_stock'

    name = fields.Char(string='Name')
    type_emp= fields.Selection(string="Type d'emplacement", selection=[('p', 'Point de Vent'), ('d', 'Depot'),('c', 'Camion')])
    stock = fields.One2many('benin_petro.produit_stock','con',string='Stock')
    stock_depot = fields.One2many('benin_petro.produit_stock','con',string='Stock')
    stock_camion = fields.One2many('benin_petro.produit_stock','con',string='Stock')
    product = fields.Many2one('product.template',string="Produit")
    @api.onchange('type_emp','product')
    def _onchange_type(self):
        if self.type_emp:
            if self.type_emp == 'p':
                if self.product:
                    query = self._cr.execute('select pt.name,gp.libelle,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt,benin_petro_point_vente gp where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and gp.id = l.point_vente_id and pt.id = '+str(self.product.id)+' group by pt.name,gp.libelle,pt.id')
                else:
                    query = self._cr.execute('select pt.name,gp.libelle,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt,benin_petro_point_vente gp where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and gp.id = l.point_vente_id group by pt.name,gp.libelle,pt.id')
                resutl = self._cr.fetchall()
                data = [(0,0,{'point_vente':row[1],'produit':row[0],'stock':float(row[2])}) for row in resutl ]
                print data
                return {'value':{'stock':data}}
            if self.type_emp == 'c':
                if self.product:
                    query = self._cr.execute("select l.name,pt.name,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and l.typedeemp  like 'camion' and pt.id = "+str(self.product.id)+" group by pt.name , l.name,pt.id")
                else :
                    query = self._cr.execute("select l.name,pt.name,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and l.typedeemp  like 'camion' group by pt.name , l.name,pt.id")
                resutl = self._cr.fetchall()
                data = [(0,0,{'camion':row[0],'produit':row[1],'stock':float(row[2])}) for row in resutl ]
                print data
                return {'value':{'stock_camion':data}}
            if self.type_emp == 'd':
                if self.product:
                    query = self._cr.execute("select l.name,pt.name,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and l.typedeemp  like 'depot' and pt.id = "+str(self.product.id)+" group by pt.name , l.name,pt.id")
                else :
                    query = self._cr.execute("select l.name,pt.name,sum(s.qty) from product_product p , stock_quant s ,stock_location l, product_template pt where s.product_id = p.id and pt.id = p.product_tmpl_id and l.id = s.location_id and l.typedeemp  like 'depot' group by pt.name , l.name,pt.id")
                resutl = self._cr.fetchall()
                data = [(0,0,{'depot':row[0],'produit':row[1],'stock':float(row[2])}) for row in resutl ]
                print data
                return {'value':{'stock_depot':data}}


class Produit_stock(models.Model):
    _name="benin_petro.produit_stock"
    point_vente = fields.Char(string='Point de Vente')
    produit = fields.Char(string='Produit')
    stock = fields.Float(string='En stock')
    depot = fields.Char(string='Depot')
    camion = fields.Char(string='Camion')
    
    con = fields.Many2one(comodel_name='benin_petro.consulte_stock', string='con')
    
    