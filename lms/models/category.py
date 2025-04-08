from odoo import  fields,models,api

class Category(models.Model):
    _name = "library.category"
    _description = "Category"
    _rec_name = "type"

    type = fields.Char(string="Category Type")
    book_ids = fields.One2many("library.book","category_id",string="Category")