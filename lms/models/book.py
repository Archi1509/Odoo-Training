from odoo import  fields,models,api

class Book(models.Model):
    _name = "library.book"
    _description = "Book Management"

    name=fields.Char(string="Name")
    author_id=fields.Many2one("library.author",string="Author")
    isbn=fields.Char(string="ISBN")
    category_id=fields.Many2one("library.category",string="Category")
    available_copies=fields.Integer(string="Number of available copies")



