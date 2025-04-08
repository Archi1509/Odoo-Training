from odoo import fields,models,api

class SaleRMALine(models.Model):
    _name = "sale.rma.line"
    _description = "RMA Line"
    _rec_name = "product_id"

    product_id = fields.Many2one("sale.order.line",string="Product")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive")
    received_qty = fields.Float(string="Received Quantity")
    sale_rma_id = fields.Many2one('sale.rma',string="Sale RMA ID")

    @api.model_create_multi
    def create(self,vals):
        res = super().create(vals)
        for rec in res:
            if rec.product_id:
                sale_order_details = self.env['sale.order.line'].search(
                    [('product_template_id', '=', rec.product_id.product_template_id.id)],limit=1)
                if sale_order_details:
                    rec.quantity = sale_order_details.product_uom_qty
                    rec.unit_price = sale_order_details.price_unit
        return res