from odoo import fields, models


class AuthorMenu(models.Model):
    _name = "author.details"
    _description = 'BookStore Management System'

    name = fields.Char('Name')
    email = fields.Char('Email')
    contact=fields.Integer()
    author_books = fields.One2many('book.details','books_author','Authors')
    age=fields.Integer()
    biography=fields.Text('Biography')
