from odoo import fields,models,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model_create_multi
    def create(self, vals_list):
        res =  super().create(vals_list)
        return res


    def _get_action_view_picking(self, pickings):
        res = super()._get_action_view_picking(self.picking_ids)
        print(res)
        res['context'].update({'default_location_dest_id': self.order_line.sale_line_id.location_id.id})
        return res