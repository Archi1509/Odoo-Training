from odoo import fields,api,models

class CustomWizard(models.TransientModel):
    _name = 'custom.wizard'
    _description = 'Wizard'

    product_ids = fields.Many2many('product.product',string='Products')
    sale_order = fields.Many2one('sale.order')


    def action_add_product(self):
        products = []
        for rec in self.product_ids:
            products.append((0, 0, {
                'product_id': rec.id,
                'product_uom_qty':1,
            }))
        self.sale_order.order_line = products
