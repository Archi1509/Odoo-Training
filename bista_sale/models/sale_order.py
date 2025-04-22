import datetime

from odoo import fields,api,models
from datetime import date,timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_draft_quotation(self):
        today = date.today()
        expiry_date = int(self.env['ir.config_parameter'].sudo().get_param('res_config_settings.quote_notification_before_expiry', default=5 ))
        end_mail_date = today + timedelta(days = expiry_date)
        start_mail_date = today - timedelta(days = expiry_date)
        print(expiry_date)
        print(end_mail_date)
        print(start_mail_date)
        draft_quotations = self.env['sale.order'].search([('state', '=', 'draft'),('validity_date','<=',end_mail_date),('validity_date','>=',start_mail_date)], limit=5)
        print(draft_quotations)

        return draft_quotations

    def action_send_mail(self):

        template_id = self.env.ref('bista_sale.bista_sale_mail_template')
        template_id.send_mail(self.id, force_send=True)