from odoo import models,fields,api

class DocumentLine(models.Model):
    _name = 'sale.order.document.line'
    _description = "Custom Document System"

    product_ids = fields.Many2many('product.product',string='Products')
    document_id = fields.Many2one('document.custom',string='Documents')
    sale_order_doc_line = fields.Many2one('sale.order')



