from odoo import fields,api,models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    document_ids = fields.Many2many('document.custom',string='Documents')
