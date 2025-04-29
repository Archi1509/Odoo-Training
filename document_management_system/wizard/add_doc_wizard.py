from odoo import fields,api,models

class AddProduct(models.TransientModel):
    _name = 'add.product'

    product = fields.Many2many('product.product',string="Products")
    sale_order = fields.Many2one('sale.order')

    def action_add_product(self):
        products = []
        for rec in self.product:
            products.append((0, 0, {
                'product_id': rec.id,
            }))
        self.sale_order.order_line = products
        print(products)


