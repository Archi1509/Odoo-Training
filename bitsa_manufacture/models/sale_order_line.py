from odoo import fields,api,models
from datetime import datetime

from odoo.api import readonly


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    process_qty = fields.Float('Process Quantity',readonly=False)
    location_id = fields.Many2one('stock.location')

    # def _get_procurement_group(self):
    #     self.ensure_one()
    #     if self.location_id:
    #         return self.env['procurement.group'].search([
    #             ('sale_id', '=', self.order_id.id),
    #             ('location_id', '=', self.location_id.id),
    #         ], limit=1)
    #     return self.order_id.procurement_group_id
    #
    # def _prepare_procurement_group_vals(self):
    #     res = super()._prepare_procurement_group_vals()
    #     if self.location_id:
    #         res.update({'location_id': self.location_id.id})
    #     return res

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id)
        # if self.location_id:
        res.update({'location_id': self.location_id.id})
        return res



