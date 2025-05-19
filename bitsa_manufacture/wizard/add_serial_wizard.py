from odoo import fields,api,models
from odoo.exceptions import ValidationError


class AddSerial(models.TransientModel):
    _name = 'add.serial'

    serial_number = fields.Integer(string="Serial Number to add")
    product_id = fields.Many2one('product.product')
    qty = fields.Integer("Quantity")

    def action_serial_number(self):
        serial_number = []
        active_id = self._context.get('active_id')
        mrp_product = self.env['mrp.production'].browse(active_id)
        for rec in range(1,self.serial_number+1):
            sequence = self.product_id.sequence_id.next_by_id()
            lot_product_2 = self.env['stock.lot'].create({
                    'name': sequence,
                    'product_id': self.product_id.id,
                })
            serial_number.append(lot_product_2.id)
            mrp_product.write({'serial_ids': [(4,lot_product_2.id )]})
        mrp_product.qty = self.qty

    @api.onchange('serial_number')
    def _onchange_qty(self):
        for rec in self:
            if self.serial_number <= self.qty:
                rec.qty -=  rec.serial_number

    @api.constrains('qty')
    def check_qty(self):
        active_id = self._context.get('active_id')
        mrp_product = self.env['mrp.production'].browse(active_id)
        if self.serial_number > mrp_product.qty:
            raise ValidationError(f'You cant produce Serial Number more then the {self.qty}')



