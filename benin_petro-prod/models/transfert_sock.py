from odoo import api, fields, models


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    def a_fun(self):  
     return 5
    # delattr(odoo.addons.account.models.account_invoice.AccountInvoice, 'account_id')
    picking_type_id=fields.Many2one('stock.picking.type',string='Picking Type',required=False,default=a_fun,readonly=True)
    image1 = fields.Binary(string='image1')
    image2 = fields.Binary(string='image2')
    type = fields.Selection(string='type', selection=[('blanch', 'Blanch'), ('autre', 'Autre')])
    