from odoo import fields,models,api
from datetime import date
from dateutil.relativedelta import relativedelta

class InterestRate(models.Model):
    _name = 'interest.rate'
    _description = 'Interest Rate'
    _rec_name = 'rate'

    rate = fields.Float('Interest Rate')
    interest_date = fields.Date('Interest Dated')
    is_active = fields.Boolean('Active')
    loan_id = fields.Many2one('bista.loan',string='Loan')

    def active_rate(self):
        #Activate is_active button and sets rate in main loan form page
        active_rates = self.env['interest.rate'].search([('is_active', '=', True),('loan_id', '=', self.loan_id.id)])
        # all_rates = self.env['interest.rate'].search([])
        # active_rates = all_rates.filtered(
        #     lambda rec: rec.is_active and rec.loan_id.id == self.loan_id.id
        # )
        active_rates.write({'is_active': False})
        self.is_active = True
        self.loan_id.rate = self.rate










