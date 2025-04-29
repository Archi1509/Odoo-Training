from odoo import fields,api,models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        self.message_post(body=f"Record is Validated {self.env.user.name}.")
        return res
