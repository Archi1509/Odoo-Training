from odoo import fields,api,models

class StockMove(models.Model):
    _inherit = 'stock.move'

    # @api.depends('picking_id.location_dest_id','sale_line_id.location_id')
    # def _compute_location_dest_id(self):
    #     super()._compute_location_dest_id()
    #     for move in self:
    #         if move.sale_line_id.location_id:
    #             location_dest = move.sale_line_id.location_id
    #             move.location_dest_id = location_dest
    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        if self.sale_line_id.location_id:
            res.update({'location_dest_id': self.sale_line_id.location_id.id})
        return res
