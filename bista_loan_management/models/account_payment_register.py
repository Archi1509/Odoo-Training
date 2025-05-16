from odoo import fields,models,api
from datetime import date

from odoo.exceptions import ValidationError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'


    def action_create_payments(self):
        today = date.today()
        res = super().action_create_payments()
        active_id = self._context.get('active_id')
        invoice_rec = self.env['account.move'].search([('id','=',active_id)])
        if invoice_rec.amount_total == self.amount:
            emi_record = invoice_rec.loan_id.emi_lines.filtered(lambda record:record.date == today)
            emi_record.state = 'invoice_paid'
        else:
            raise ValidationError('You Cant Change Payment Price')
        return res

