from odoo import fields,models,api


class Author(models.Model):
    _name = "library.author"
    _description = " Author Management"

    name=fields.Char(string="Author Name")
    age=fields.Date(string="Age")
    book_id=fields.One2many("library.book", "author_id", string="Books")

