from odoo import fields,models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to_approve', 'To Approve'),
        ('sale', 'Sale Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    date_approve = fields.Datetime(string="Approval Date", readonly=True)


    def action_approval(self):
        self.write({'state': 'sale', 'date_approve': fields.Datetime.now()})
        return True

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm
        for order in self:
            if order.amount_total > 5000:
                order.write({'state': 'to_approve'})
            else:
                order.action_approval()
        return res