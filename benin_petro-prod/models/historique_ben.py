from odoo import fields, api, models

class historique_ben(models.Model):
    _name="benin_petro.historique_ben"

    hest_ben_id = fields.Integer("id")
    beneficiaire_id = fields.Many2one("benin_petro.bseneficiaire",string="Beneficiaire")
    hes_id = fields.Many2one("benin_petro.carte.consommation",string="historique")
    mnt = fields.Float(string="Montant")
