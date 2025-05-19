from odoo import fields,models

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    location_id = fields.Many2one('stock.location')