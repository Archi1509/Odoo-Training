from odoo import fields, models


class GenreMenu(models.Model):
    _name = "genre.details"
    _description = 'BookStore Management System'
    _rec_name = 'genre_name'

    genre_name = fields.Char('Genre Name')
    description=fields.Text('Description')
    genre_books=fields.One2many('book.details','books_genre','Genre')
