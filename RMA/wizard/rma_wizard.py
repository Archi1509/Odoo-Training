from odoo import fields,models,api

class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'Wizard View'

    product_id = fields.Many2one('sale.order.line',string='Product')
    sale_order_quantity = fields.Float(string='Ordered Quantity')
    quantity = fields.Float(string='Returned Quantity')

    def action_process(self):
        pass