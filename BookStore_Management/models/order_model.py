from odoo import fields, models


class OrderMenu(models.Model):
    _name = "order.details"
    _description = 'BookStore Management System'
    _rec_name = 'orders_customer'

    order_date = fields.Date()
    # total_amount = fields.Float('Total Amount')
    orders_customer = fields.Many2one('customer.details', string='Customer')
    book_orders = fields.One2many('orderliness.details', 'order_id', string='Orders')

