from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = "sale order line inheritance"

    extra_note=fields.Text(string="Extra Note")
    previous_price=fields.Float(string="Previous Price",compute="_compute_previous_price")
    warehouse_quantity=fields.Integer(string="WareHouse Quantity",compute='_compute_quantity_available_at_locations')
    quantity_location_sum=fields.Float("Total Quantity",compute='_compute_quantity_available_at_locations')
    location_ids = fields.Many2many('stock.location', string="Locations")



    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_partner_id.extra_discount')
    def _compute_discount(self):
        res = super(SaleOrderLine, self)._compute_discount()
        for order in self:
            order.discount += order.order_partner_id.extra_discount
        return res

    @api.depends('product_template_id')
    def _compute_previous_price(self):
        for rec in self:
            product = self.env['product.product'].search([('id', '=', rec.product_id.id)])
            rec.previous_price= product.lst_price

    def _compute_quantity_available_at_locations(self):
        for rec in self:
            rec.quantity_location_sum = rec.product_id.with_context(
                location=rec.location_ids.ids).qty_available
            rec.warehouse_quantity = rec.product_id.with_context(
                warehouse_id= rec.order_id.warehouse_id.id).qty_available










