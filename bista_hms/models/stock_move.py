from odoo import fields,api,models

class StockMove(models.Model):
    _inherit = "stock.move"

    prescription_line_id=fields.Many2one("prescription.line",string="Prescription")