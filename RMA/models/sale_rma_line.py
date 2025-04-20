from odoo import fields,models,api

class SaleRMALine(models.Model):
    _name = "sale.rma.line"
    _description = "RMA Line"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product",string="Product")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive",compute="_compute_qty",store=True) #Qty User want to return
    received_qty = fields.Float(string="Received Quantity",compute="_compute_qty",store=True)
    sale_rma_id = fields.Many2one('sale.rma',string="Sale RMA ID")
    invoice_line_ids = fields.One2many("account.move.line", 'rma_line_id', string="Sale RMA Line IDS")
    move_ids=fields.One2many("stock.move","rma_line_id","Delivery")
    invoice_ids = fields.One2many("account.move",'sale_rma_invoice_id','Invoice')
    invoiced_qty = fields.Float(string="Invoiced Quantity",compute="_compute_invoiced_qty",store=True)
    qty_to_invoice = fields.Float(string="Quantity To Invoice",compute="_compute_invoiced_qty",store=True)


    @api.depends('move_ids.state', 'move_ids.product_uom_qty', 'move_ids.quantity')
    def _compute_qty(self):
        for rec in self:
            if rec._name != 'sale.order.line':  # Skip if it's from Sale Order Line
                rec.received_qty = sum(rec.move_ids.filtered(lambda m: m.state == 'done').mapped('quantity'))
                rec.to_receive = sum(rec.move_ids.filtered(lambda m: m.state == 'assigned').mapped('quantity'))

    @api.depends('invoice_line_ids.quantity', 'invoice_line_ids.move_id.state', 'received_qty')
    def _compute_invoiced_qty(self):
        for rec in self:
            posted_lines = rec.invoice_line_ids.filtered(lambda line: line.move_id and line.move_id.state == 'posted')
            rec.invoiced_qty = sum(posted_lines.mapped('quantity'))
            rec.qty_to_invoice = rec.received_qty - rec.invoiced_qty


















