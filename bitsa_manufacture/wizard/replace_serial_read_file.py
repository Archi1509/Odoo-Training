from odoo import fields,models,api

class ReplaceSerialReadFile(models.TransientModel):
    _name = 'replace.serial.read.file'
    _description = 'Replace Serial Read File'

    mo_number_id = fields.Many2one('mrp.production',string='MO Number')
    product_code = fields.Many2one('product.product',string='Current Product')
    old_serial = fields.Many2one('stock.lot',string='Old Serial')
    new_serial = fields.Many2one('stock.lot',string='New Serial')
    update_product_serial_id = fields.Many2one('update.product.serial','Update Product')