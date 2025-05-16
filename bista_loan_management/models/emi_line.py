from odoo import fields, models


class EmiLine(models.Model):
    _name = 'emi.line'
    _description = 'Emi Line'

    principal_paid = fields.Float('Principal Paid')
    interest_charged = fields.Float('Interest Charged')
    total_payment = fields.Float('Total Payment')
    balance = fields.Float('Balance')
    date = fields.Date('Month')
    loan_id = fields.Many2one('bista.loan',string='Loan')
    state = fields.Selection([('pending','Pending'),('invoice generated','Invoice Generated'),('invoice_paid','Invoice Paid')]
                             ,default ='pending')
    invoice_id = fields.One2many('account.move','loan_id',string='Invoice')




