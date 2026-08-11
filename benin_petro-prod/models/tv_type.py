from odoo import api, fields, models


class TvType(models.Model):
    _name = 'benin_petro.tv_type'
    _rec_name="rec"

    type_name = fields.Char(string='Nom')
    montant = fields.Integer(string='Montant')
    rec = fields.Char(string='rec')
    mysql_id = fields.Integer(string='mysql id')
    libelle = fields.Selection([('classique','CLASSIQUE'),('privilege','PRIVILEGE'),('noblesse','NOBLESSE')] , string="Libelle" , default="classique")
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id )

    @api.model
    def create(self, vals):
        vals['rec'] = vals['type_name'] + '-'+str(vals['montant']) + 'CFA'
        return super(TvType, self).create(vals)
    
