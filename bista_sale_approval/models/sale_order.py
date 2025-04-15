from odoo import fields,models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection_add=[
            ('to_approve', 'To Approve'),
        ],
    )

    def action_approval(self):
        self.write({'state': 'sale'})
        return True

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm
        desired_group_name = self.env['res.groups'].search([('name','=','Sale Order User')])
        is_desired_group = self.env.user.id in desired_group_name.users.ids
        for order in self:
            if order.amount_total > 5000 and is_desired_group:
                order.write({'state': 'to_approve'})
            else:
                order.action_approval()
        return res