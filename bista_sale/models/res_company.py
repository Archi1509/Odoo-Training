from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    quote_notification_before_expiry = fields.Char("Quote Notification before Expiry" ,help="Number of day before you want to be notified")
