from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Order Approval", default=lambda self: self.env.company.so_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *", readonly=False)
    so_double_validation_amount = fields.Monetary( string="Minimum Amount", currency_field='company_currency_id', readonly=False)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            so_double_validation_amount=params.get_param('res_config_settings.so_double_validation_amount'),
        )
        return res
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('res_config_settings.so_double_validation_amount', self.so_double_validation_amount)

        so_lock = 'lock' if self.lock_confirmed_po else 'edit'
        so_double_validation = 'two_step' if self.so_order_approval else 'one_step'
        if self.po_lock != so_lock:
            self.po_lock = so_lock
        if self.so_double_validation != so_double_validation:
            self.so_double_validation = so_double_validation