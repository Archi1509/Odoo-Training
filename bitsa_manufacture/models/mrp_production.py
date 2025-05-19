from odoo import fields,api,models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    serial_ids = fields.Many2many('stock.lot')
    qty = fields.Integer('duplicate qty')#,compute='_compute_qty',store=True

    def update_product_and_serial(self):
        view_id = self.env.ref('bitsa_manufacture.update_product_serial_form_view').id
        return {
            'name': 'Update Product/Serial',
            'view_mode': 'form',
            'res_model': 'update.product.serial',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def add_serial_number(self):
        view_id = self.env.ref('bitsa_manufacture.add_serial_view_form').id
        return {
            'name': 'Add Serial Number',
            'view_mode': 'form',
            'res_model': 'add.serial',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':{'default_product_id':self.product_id.id,
                       'default_qty':self.qty,
                       }
        }

    @api.onchange('product_qty')
    def _onchange_qty(self):
        active_id = self._context.get('active_id')
        wizard_data = self.env['add.serial'].browse(active_id)
        self.qty = self.product_qty
        self.qty -= wizard_data.serial_number

    def _split_productions(self):
        res = super()._split_productions()
        current_lot = self.lot_producing_id.id
        self.serial_ids = [(3, current_lot)]
        return res




