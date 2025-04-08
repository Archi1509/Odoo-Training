from odoo import fields, models
from odoo.api import ondelete


class OrderLinesMenu(models.Model):
    _name = "orderliness.details"
    _description = 'BookStore Management System'
    _rec_name = 'order_id'

    quantity = fields.Integer()
    price_per_unit=fields.Float()
    order_id = fields.Many2one('order.details', string='Order',ondelete='cascade')
    books_order = fields.Many2one('book.details', string='Book')


