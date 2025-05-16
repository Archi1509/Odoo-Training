from odoo import fields,api,models
from odoo.exceptions import ValidationError
from datetime import date

class RMAInvoice(models.TransientModel):
    _name = "rma.invoice.wizard"
    _description = " Create Invoice Wizard"

    rma_invoice_wizard_line = fields.One2many("rma.invoice.wizard.line","rma_invoice_wizard_id")

    def action_invoice_process(self):
        for wizard_line in self.rma_invoice_wizard_line:
            if wizard_line.to_invoice <= 0:
                continue
            if wizard_line.to_invoice > wizard_line.rma_line_id.qty_to_invoice:
                raise ValidationError(f"Invoice Quantity must be less than or equal to Qauntity to invoice for product {wizard_line.product_id.display_name} i.e. {wizard_line.rma_line_id.qty_to_invoice} ")
        self.action_create_invoice()


    def action_create_invoice(self):
        if not self.rma_invoice_wizard_line:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        invoice = self._prepare_invoice()
        create_invoice = self.env['account.move'].create(invoice)
        product_invoice_line = self.prepare_invoice_line_vals(create_invoice)
        line_ids = self.env['account.move.line'].create(product_invoice_line)
        print(create_invoice)
        return create_invoice

    def _prepare_invoice(self):
        invoice_type_id = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        active_id = self._context.get('active_id')
        value = {
            'move_type':'out_invoice',
            'partner_id': self.rma_invoice_wizard_line.rma_line_id.sale_rma_id.sale_order_id.partner_id.id,
            'partner_shipping_id': self.rma_invoice_wizard_line.rma_line_id.sale_rma_id.sale_order_id.partner_shipping_id.id,
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.user.company_id.id,
            'invoice_date': date.today(),
            'user_id': self.env.user.id,
            'sale_rma_invoice_id': active_id
        }
        return value

    def prepare_invoice_line_vals(self,create_invoice):
        line_vals_list = []
        for line in self.rma_invoice_wizard_line:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.to_invoice,
                'move_id': create_invoice.id,
                'rma_line_id': line.rma_line_id.id
            }
            line_vals_list.append(line_vals)
        return line_vals_list





class RMAInvoiceWizardLine(models.TransientModel):
    _name = "rma.invoice.wizard.line"
    _description = "Invoice Wizard Line"

    product_id = fields.Many2one('product.product', string='Product')
    rma_line_id = fields.Many2one('sale.rma.line', string="rma Line")
    sale_order_quantity = fields.Float(string='Ordered Quantity', readonly=True)
    to_invoice = fields.Float(string="To Invoice")
    rma_invoice_wizard_id = fields.Many2one("rma.invoice.wizard")

    @api.constrains('quantity')
    def check_to_receive(self):
        for line in self:
            current_to_invoice = line.rma_line_id.quantity - (line.rma_line_id.to_invoice + line.rma_line_id.received_qty)
            if line.quantity > line.rma_line_id.quantity  or line.quantity > current_to_invoice:
                raise ValidationError(f"You cant return more then {current_to_invoice}.")
