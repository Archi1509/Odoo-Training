from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_rma_invoice_id = fields.Many2one("sale.rma")