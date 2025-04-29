from odoo import fields,models,api
from num2words import num2words

from odoo.api import depends, readonly, ValuesType, Self


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Inherit Sale Order"

    lead_reference=fields.Char(string="Lead Reference")
    amount_total_words = fields.Char(string="Total Amount in words",compute="convert_num_to_word")

    @api.depends('amount_total')
    def convert_num_to_word(self):
        for rec in self:
                rec.amount_total_words =num2words(rec.amount_total, lang='en_IN', to='currency',currency='USD').title()
        return rec

    # @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'payment_term_id','discount_amount')
    # def _compute_amounts(self):
    #     res=super(SaleOrder, self)._compute_amounts()
    #     for order in self:
    #         order.tax_totals = order.tax_totals - order.discount_amount
    #     return res

    # @api.onchange('extra_discount', 'order_line.product_uom_qty', 'pricelist_id')
    # def calculate_total_discount(self):
    #     for order in self:
    #         pricelist_discount = self.env['product.pricelist.item'].search([
    #             ('pricelist_id', '=', order.pricelist_id.id)], limit=1)
    #
    #         if pricelist_discount:
    #             total_discount = pricelist_discount.percent_price + order.extra_discount
    #         else:
    #             total_discount = order.extra_discount
    #
    #         order.discount_amount = total_discount
    #
    #         for line in order.order_line:
    #             line.discount = total_discount

    @api.model_create_multi
    def create(self, vals_list):
        partner_id = vals_list.get('partner_id')
        partner_details = self.env['res.partner'].browse(partner_id)
        if partner_details.use_customer_tc is True and partner_details.terms_and_conditions:
            vals_list['note'] = partner_details.terms_and_conditions
        return super(SaleOrder, self).create(vals_list)







