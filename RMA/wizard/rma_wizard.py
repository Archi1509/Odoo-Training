from odoo import fields,models,api
from odoo.exceptions import ValidationError


class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'Wizard View'

    rma_line = fields.One2many("rma.line.wizard","line_id",string="RMA Lines")


    def action_process(self):
        self.action_create_delivery()
        active_id = self._context.get('active_id')
        sale_order_details = self.env['sale.rma'].browse(active_id)

    def action_create_delivery(self):
        picking_vals = self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)

        move_vals = self.prepare_move_vals(picking_id)
        move_id = self.env['stock.move'].create(move_vals)

        move_id._action_confirm(merge=False)
        # picking_id.action_confirm()
        picking_id.action_assign()
        # picking_id.button_validate()


    @api.model
    def default_get(self, fields_list):
        res = super(RMAWizard, self).default_get(fields_list)
        if 'default_rma_line' in self.env.context:
            res['rma_line'] = self.env.context.get('default_rma_line')
        return res

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
    sale_order_quantity = fields.Float(string='Ordered Quantity' ,readonly=True)
    quantity = fields.Float(string='To Receive',store=True, compute = "_compute_to_receive",readonly= False )
    line_id =fields.Many2one("rma.wizard")

    @api.depends('rma_line_id.to_receive','rma_line_id.received_qty','rma_line_id.quantity')
    def _compute_to_receive(self):
        for line in self:
            line.quantity = self.rma_line_id.quantity - (self.rma_line_id.to_receive + self.rma_line_id.received_qty)

    @api.constrains('quantity')
    def check_to_receive(self):
        for line in self:
            current_to_receive = line.rma_line_id.quantity - (line.rma_line_id.to_receive + line.rma_line_id.received_qty)
            if line.quantity > line.rma_line_id.quantity  or line.quantity > current_to_receive:
                raise ValidationError(f"You cant return more then {current_to_receive}.")








