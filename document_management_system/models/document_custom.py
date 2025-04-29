from odoo import models,fields,api

class DocumentCustom(models.Model):
    _name = 'document.custom'
    _description = "Custom Document System"

    name = fields.Char(string='Name')
    attachment_id = fields.Many2one('ir.attachment',string="Attachment")
    tag_ids = fields.Many2many(
        'doc.tag.master',
        string='Document Tags'
    )
    order_ids=fields.Many2one('sale.order')
    product_id = fields.Many2one('product.product')

