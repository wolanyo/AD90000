from odoo import api, fields, models


class TvPrintHestory(models.Model):
    _name = 'benin_petro.tv_print_hestory'
    _description = 'New Description'

    tv_ids = fields.One2many('benin_petro.ticket_valeur','print_hestory_id',string='T.V')
    print_id = fields.Many2one('benin_petro.tv_print',string='print')
    nb_tv = fields.Integer(string='Nombre des tickets')
    tv_type = fields.Many2one('benin_petro.tv_type',string="Type")
    montant = fields.Float(string="Montant")
    state = fields.Selection([('brouillon','brouillon'),('imprime','imprime')] , string="Statut" , default="brouillon")


    def print_tv(self):
        self.state = 'imprime'
        return self.env['report'].get_action(self,'benin_petro.repport_tv_template')