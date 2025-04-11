from odoo import fields,models,api

class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'Wizard View'

    rma_line = fields.One2many("rma.line.wizard","line_id",string="RMA Lines")
    active_id = fields.Char("ID",readonly=True)

    @api.onchange('rma_line')
    def get_active_id(self):
        self.active_id = self._context.get('active_id')

    def action_process(self):
        picking_vals = self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)

        move_vals = self.prepare_move_vals(picking_id)
        move_id = self.env['stock.move'].create(move_vals)

    def prepare_picking_vals(self):
        pass

    def prepare_move_vals(self):
        pass


class RMALineWizard(models.TransientModel):
    _name = "rma.line.wizard"

    product_id = fields.Many2one('product.product', string='Product')
    sale_order_quantity = fields.Float(string='Ordered Quantity')
    quantity = fields.Float(string='To Receive')
    line_id =fields.Many2one("rma.wizard")
