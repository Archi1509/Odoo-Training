from odoo import fields,api,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    pharmacy_ids = fields.Many2one('sale.pharmacy',string='Pharmacy')

