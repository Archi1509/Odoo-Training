from odoo import fields,models,api
from odoo.api import depends

class StockPicking(models.Model):
    _inherit = "stock.picking"

    lead_reference=fields.Char(string="Lead Reference",related="sale_id.lead_reference",
                               depends=['sale_id.lead_reference'],store=True)
    prescription_id=fields.Many2one("hms.prescription",string="Prescription")

    # @api.model_create_multi
    # def create(self, val_lists):
    #     res = super().create(val_lists)
    #     return res