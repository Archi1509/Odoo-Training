from odoo import fields,models,api

class SaleRMALine(models.Model):
    _name = "sale.rma.line"
    _description = "RMA Line"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product",string="Product")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive") #Qty User want to return
    received_qty = fields.Float(string="Received Quantity")
    sale_rma_id = fields.Many2one('sale.rma',string="Sale RMA ID")
    move_ids=fields.One2many("stock.move","rma_line_id","Delivery")











