from odoo import api, fields, models
import csv

class StockMove(models.Model):
    _inherit = 'stock.move'

    csv_file = fields.Binary(string="select csv fle")

    @api.model
    def create(self, vals):
        p = super(StockMove, self).create(vals)
        print p.csv_file
        return p

    def get_data(self):
        d = self.env['stock.move'].search([])
        data = {}
        for c in d :
            if not c.location_dest_id in data.keys():
                if c.name[:3] == 'INV':
                    data[c.location_dest_id] = []
            if c.name[:3] == 'INV':
                data[c.location_dest_id].append(c)
        print data
        return data

    def print_report(self):
        return self.env['report'].get_action(self, 'benin_petro.report_name.xlsx')
