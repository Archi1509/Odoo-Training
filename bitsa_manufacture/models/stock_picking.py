from odoo import fields,api,models
from odoo.api import ValuesType, Self


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def generate_lot_ids(self):
        for product in self.move_ids:
            if product.product_id.sequence_id:
                qty = int(product.quantity)
                for rec in range(qty):
                    sequence = product.product_id.sequence_id.next_by_id()
                    lot_product_2 = self.env['stock.lot'].create({
                        'name': sequence,
                        'product_id': product.product_id.id,
                    })
                    product.lot_ids = [(4, lot_product_2.id)]

    @api.model_create_multi
    def create(self, vals_list):
        res=super().create(vals_list)
        return res

    # @api.depends('picking_type_id', 'partner_id','sale_id.order_line.location_id')
    # def _compute_location_id(self):
    #     super()._compute_location_id()
    #     for picking in self:
    #         for line in picking.sale_id.order_line:
    #             if picking.sale_id.order_line.location_id and (line.product_id in picking.move_ids.product_id):
    #                     location_src = line.location_id
    #                     picking.location_id = location_src.id





