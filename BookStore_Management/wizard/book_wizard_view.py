from odoo import models, fields


class BookWizardView(models.TransientModel):
    _name = 'book.wizard.view'
    _description = 'Book Delivery Wizard'
    _rec_name = 'title'

    title = fields.Char('Title' ,required=True)
    price = fields.Float()
    isbn = fields.Integer()
    stock_qty = fields.Integer('Stock Quantity')
    rating=fields.Float('Rating')


