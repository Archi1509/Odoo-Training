from odoo import fields,models,api

class ProductWizard(models.TransientModel):
    _name = 'productupdate.wizard'
    _description = 'Wizard View'

    quantity = fields.Float("Quantity")
    location_id = fields.Many2one("stock.location")

    def update_on_hand_quantity(self):
        loc_id = self.location_id.id
        # record = self.env['stock.location'].browse(loc_id)
        # partner.write({'email': 'new.email@example.com', })
        active_id = self.env.context.get('active_id')
        product_id = self.env['product.template'].browse(active_id)
        record = self.env['stock.quant'].search(
            [('location_id', '=', loc_id), ('product_id', '=', product_id.product_variant_id.id)])
        # record.with_context(inventory_mode=True).write({'inventory_quantity':self.quantity})
        record.write({'inventory_quantity': self.quantity})
        record._apply_inventory()







