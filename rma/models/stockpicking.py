from odoo import fields,api,models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    rma_picking_id = fields.Many2one("sale.rma")
