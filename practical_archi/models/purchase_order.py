from odoo import fields,api,models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        res = super().button_confirm()
        if self.partner_id and self.partner_id.email:
            template = self.env.ref('practical_archi.purchase_order_mail_template')
            template.send_mail(self.id, force_send=True)
        return res


