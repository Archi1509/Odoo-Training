from odoo import fields, models


class CustomerMenu(models.Model):
    _name = "customer.details"
    _description = 'BookStore Management System'
    _rec_name = 'customer_name'

    customer_name = fields.Char('Customer Name')
    email = fields.Char('Email')
    customer_address=fields.Text('Address')
    phone=fields.Char('Phone')
    customer_orders = fields.One2many('order.details', 'orders_customer', string='Orders')
