from odoo import fields,api,models

class StockMove(models.Model):
    _inherit = "stock.move"

    rma_line_id = fields.Many2one("sale.rma.line")