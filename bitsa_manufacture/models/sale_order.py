from odoo import fields,api,models
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def set_process_qty(self):
        for order in self.order_line:
            for picking in order.move_ids:
                picking.quantity=order.process_qty

    def action_process_all(self):
        self.action_confirm()
        self.set_process_qty()
        po = self._get_purchase_orders()
        if po:
            po.button_confirm()
            for order in po:
                for line in po.order_line:
                    for move in line.move_ids:
                        for line in self.order_line:
                            if line.product_id.id == move.product_id.id:
                                move.quantity = line.process_qty
                                break
        for purchase_view in po:
            purchase_view.action_view_picking()
            # mto lot code here
            purchase_view.picking_ids.generate_lot_ids()
            picking_vals = purchase_view.picking_ids.button_validate()
            picking_to_validate = picking_vals['context']['button_validate_picking_ids']
            pickings_to_validate = self.env['stock.picking'].browse(picking_to_validate).with_context(
                skip_backorder=True)
            pickings_to_validate.button_validate()
            purchase_view.action_create_invoice()
            purchase_view.invoice_ids.update({'invoice_date':date.today()})
            purchase_view.invoice_ids.action_post()

        # Backorder for SO
        self.set_process_qty()
        self.picking_ids.generate_lot_ids()
        picking_vals = self.picking_ids.button_validate()
        picking_to_validate = picking_vals['context']['button_validate_picking_ids']
        pickings_to_validate = self.env['stock.picking'].browse(picking_to_validate).with_context(skip_backorder=True)
        pickings_to_validate.button_validate()
        self._create_invoices()
        self.invoice_ids.action_post()
        action_context = self.invoice_ids.action_register_payment()['context']
        payment = self.env['account.payment.register'].with_context(action_context).create({})._create_payments()









