from odoo import fields,api,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    document_ids = fields.Many2many('document.custom',string='Document')