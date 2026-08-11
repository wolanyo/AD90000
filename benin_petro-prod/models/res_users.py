from odoo import fields, api, models,_
from odoo.exceptions import  ValidationError
import datetime
from random import randint


class   res_users(models.Model):
    _inherit = "res.users"



    # partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade',auto_join=True,
    #     string='Related Partner', help='Partner-related data of the user')

