from odoo import api, fields, models


class TvFactureNumbers(models.Model):
    _name = 'benin_petro.facture_number'
    _description = 'New Description'

    num = fields.Integer(string='Gasoil',default=1)
   

    
    
