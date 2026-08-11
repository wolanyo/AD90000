from odoo import api, fields, models
from num2words import num2words



class PrchesOrder(models.Model):
    _inherit = 'purchase.order'

    def getMontantWord(self):
        mnt =  self.amount_total
        text = num2words(mnt, lang='fr')
        print text
        return text
