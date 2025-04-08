from odoo import fields, models


class PublisherMenu(models.Model):
    _name = "publisher.details"
    _description = 'BookStore Management System'
    _rec_name = 'publisher_name'

    publisher_name = fields.Char('Publisher Name')
    address = fields.Text('Address')
    website=fields.Char('Website')
    publisher_books=fields.One2many('book.details','books_publisher','Publisher')
