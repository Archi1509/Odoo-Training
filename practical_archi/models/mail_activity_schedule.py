
from odoo import models,fields


class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    meaningful_connections = fields.Boolean("Meaningful Connections")