from odoo import fields,api,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    extra = fields.Char(string='extra')
    service_product = fields.Integer(string='Service Product',compute="_compute_service_product",store=True)
    state = fields.Selection(
        selection_add=[
            ('to_approve', 'To Approve'), ('sale', '')
        ],
    )

    def action_approval(self):
        self.with_context(approved=True).action_confirm()

    def _confirmation_error_message(self):
        """ Return whether order can be confirmed or not if not then returm error message. """
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'to_approve'}:
            return ("Some orders are not in a state requiring confirmation.")
        if any(
                not line.display_type
                and not line.is_downpayment
                and not line.product_id
                for line in self.order_line
        ):
            return ("A line on these orders missing a product, you cannot confirm it.")

        return False

    def action_confirm(self):
        if self._context.get('approved'):
            super(SaleOrder, self).action_confirm()

        else:
            for order in self:
                if order._approval_allowed():
                    order.action_approval()
                else:
                    order.write({'state': 'to_approve'})

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        params = int(self.env['ir.config_parameter'].sudo().get_param('res_config_settings.so_double_validation_amount'))
        print(params)
        return (
                self.company_id.so_double_validation == 'one_step'
                or (self.company_id.so_double_validation == 'two_step'
                    and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.so_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today()))
                or self.env.user.has_group('practical_archi.group_sale_approver'))

    def open_wizard(self):
        view_id = self.env.ref('practical_archi.custom_wizard_form').id
        return {
            'name': 'Add Products',
            'view_mode': 'form',
            'res_model': 'custom.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sale_order': self.id}
        }

    @api.depends('order_line.product_template_id')
    def _compute_service_product(self):
        for record in self:
            if record.order_line:
                record.service_product = self.env['sale.order.line'].search_count([('order_id','=',record.id),('product_template_id.type','=','service')])
            else:
                record.service_product = 0


