from email.policy import default

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quote_notification_before_expiry = fields.Char("Quote Notification before Expiry" ,help="Number of day before you want to be notified" ,default="5")
    notify_user = fields.Boolean("Notify User",default=True)

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     params = self.env['ir.config_parameter'].sudo()
    #     res.update(
    #         quote_notification_before_expiry=params.get_param('res_config_settings.quote_notification_before_expiry',
    #                                                           default='5'),
    #         notify_user=params.get_param('res_config_settings.notify_user', default='True') == 'True',
    #     )
    #     return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('res_config_settings.quote_notification_before_expiry', self.quote_notification_before_expiry)
        params.set_param('res_config_settings.notify_user', self.notify_user)