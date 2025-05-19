from odoo import fields,models,api

class ReplaceProductReadFile(models.TransientModel):
    _name = 'replace.product.read.file'
    _description = 'Replace Product Read File'

    mo_number_id = fields.Many2one('mrp.production',string='MO Number')
    current_product = fields.Many2one('product.product',string='Current Product')
    new_product = fields.Many2one('product.product',string='New Product')
    state = fields.Char('State')
    update_product_serial_id = fields.Many2one('update.product.serial','Update Product')