
from odoo import fields,models

class BookStore(models.Model):
    _name = "book.details"
    _description = 'BookStore Management System'
    _rec_name = 'title'

    title = fields.Char('Title')
    price = fields.Float()
    isbn = fields.Integer()
    publish_date = fields.Date('Publication Date')
    is_avail = fields.Selection([('available','Available'),('notavailable','Not Available')])
    description = fields.Text('Description')
    stock_qty = fields.Integer('Stock Quantity')
    books_author = fields.Many2one('author.details',string='Author')
    rating=fields.Float('Rating')
    books_genre=fields.Many2one('genre.details',string='Genre')
    books_publisher=fields.Many2one('publisher.details',string='Publisher')
    order_books = fields.One2many('orderliness.details', 'books_order', string='Orders')

    users_users=fields.Many2many('res.users','rel_user_user','user_id','user_name')

    def action_open_book_wizard(self):
        view_id = self.env.ref('BookStore_Management.book_wizard_wizard').id
        return {
            'name': 'Title',
            'view_mode': 'form',
            'res_model': 'book.wizard.view',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    

