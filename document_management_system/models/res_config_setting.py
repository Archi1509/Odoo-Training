from email.policy import default

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allowed_update = fields.Boolean("Allow Update After Order Confirmed" ,help="Allow Update After Order Confirmed" ,default=True,related='company_id.allowed_update',readonly=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            allowed_update=params.get_param('res_config_settings.allowed_update'),
        )
        return res
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('res_config_settings.allowed_update', self.allowed_update)
