from odoo import fields,models,api
from odoo.exceptions import ValidationError


class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'Wizard View'

    rma_line = fields.One2many("rma.line.wizard","line_id",string="RMA Lines")


    def action_process(self):
        picking_vals = self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)

        move_vals = self.prepare_move_vals(picking_id)
        move_id = self.env['stock.move'].create(move_vals)

        active_id = self._context.get('active_id')
        sale_order_details = self.env['sale.rma'].browse(active_id)
        for rec in self.rma_line:
            matching_line = sale_order_details.sale_rma_line.filtered(lambda l: l.product_id == rec.product_id)
            if matching_line:
                matching_line.to_receive = matching_line.to_receive + rec.quantity
                matching_line.to_be_received = rec.to_be_received

    def prepare_picking_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'incoming')],limit=1)
        active_id = self._context.get('active_id')
        sale_order_details = self.env['sale.rma'].browse(active_id)
        vals = {
            'partner_id': sale_order_details.sale_order_id.partner_id.id,
            'picking_type_id': picking_type_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            'location_id': picking_type_id.default_location_src_id.id,
            'origin': sale_order_details.display_name,
            'rma_picking_id': active_id,
        }
        return vals

    def prepare_move_vals(self,picking_id):
        move_vals = []
        for line in self.rma_line:
            vals = {
                'picking_type_id': picking_id.picking_type_id.id,
                'location_id': picking_id.location_id.id,
                'location_dest_id': picking_id.location_dest_id.id,
                'picking_id': picking_id.id,
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_uom_qty': line.quantity,
                'rma_line_id': line.rma_line_id.id
            }
            move_vals.append(vals)
        return move_vals

class RMALineWizard(models.TransientModel):
    _name = "rma.line.wizard"

    product_id = fields.Many2one('product.product', string='Product')
    rma_line_id = fields.Many2one('sale.rma.line', string="RMA Line")
    sale_order_quantity = fields.Float(string='Ordered Quantity')
    quantity = fields.Float(string='To Receive')
    line_id =fields.Many2one("rma.wizard")
    to_be_received = fields.Float("To be Received")

    @api.constrains('quantity', 'to_be_received')
    def check_avail(self):
        for line in self:
            if line.quantity < line.sale_order_quantity or line.quantity > line.to_be_received:
                raise ValidationError("You cant return more then you ordered")

    @api.onchange('quantity')
    def _onchange_quantity(self):
        self.check_avail()
        for line in self:
            line.to_be_received = line.to_be_received - line.quantity


